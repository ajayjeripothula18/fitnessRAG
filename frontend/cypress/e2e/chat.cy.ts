describe('Chat Interface with Persistence', () => {
  beforeEach(() => {
    // Set up auth token and auth store
    cy.window().then((win) => {
      win.localStorage.setItem('access_token', 'mock_token');
      win.localStorage.setItem('auth-store', JSON.stringify({
        state: {
          user: { id: 1, email: 'test@example.com', first_name: 'Test', last_name: 'User' },
          isAuthenticated: true
        },
        version: 0
      }));
    });
    cy.visit('/chat');
    cy.injectAxe();
  });

  it('should pass accessibility tests', () => {
    // Wait for the main page to load rather than testing the Suspense skeleton
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').should('be.visible');

    cy.checkA11y(undefined, { includedImpacts: ['critical', 'serious', 'moderate', 'minor'] }, (violations) => {
      cy.task(
        'log',
        `${violations.length} accessibility violation${
          violations.length === 1 ? '' : 's'
        } ${violations.length === 1 ? 'was' : 'were'} detected`
      );

      const violationData = violations.map(
        ({ id, impact, description, nodes }) => ({
          id,
          impact,
          description,
          nodes: nodes.length,
          html: nodes[0]?.html
        })
      );

      cy.task('table', violationData);
    });
  });

  it('should allow sending a message and show AI response with citations', () => {
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('How should I workout?');
    cy.get('button[aria-label="Send message"]').click();

    // MSW mock response will provide the text
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Check for citations
    cy.get('a[href="https://example.com/fitness-fundamentals"]').should('be.visible').and('contain', '[1]');
    // Note: The second citation has no URL, so it's a span, let's just check for its text.
    cy.contains('[2]').should('be.visible');
  });

  it('should persist conversation ID and load history on refresh', () => {
    // Send a message to establish a conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Hello AI');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the AI response
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Check that conversation ID is persisted in localStorage
    cy.window().then((win) => {
      const convId = win.localStorage.getItem('conversation_id');
      expect(convId).to.not.equal(null);
      expect(convId).to.match(/^\d+$/); // should be a number string
    });

    // Now refresh the page
    cy.reload();

    // After reload, the chat should load the history
    // We expect to see the user message and AI response from before
    cy.contains('Hello AI').should('be.visible');
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Also, the conversation ID should still be in localStorage
    cy.window().then((win) => {
      const convId = win.localStorage.getItem('conversation_id');
      expect(convId).to.not.equal(null);
    });
  });

  it('should send conversation history with follow-up messages', () => {
    // First, establish a conversation by sending a message
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('First message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the AI response
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Now, intercept the next POST request to check its payload
    cy.intercept('POST', '**/api/v1/chat/message').as('sendMessage');

    // Send a second message
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Second message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the request to be sent
    cy.wait('@sendMessage').its('request.body').then((body) => {
      // Expect the payload to contain the conversation ID (should be 1 from our mock)
      expect(body.conversation_id).to.eq(1);
      // Expect the history to contain the first turn (user message and AI response)
      // Note: Our mock returns a fixed history, but we can check that the history array is present and has length 2
      // In our actual implementation, the history sent would be the messages from the state before adding the new user message.
      // Since we have one user message and one AI message in the state, we expect history length 2.
      expect(body.history).to.be.an('array').that.has.lengthOf(2);
      // Check the first history item is the user's first message
      expect(body.history[0]).to.deep.equal({ role: 'user', content: 'First message' });
      // Check the second history item is the AI's first response
      expect(body.history[1]).to.deep.equal({ role: 'assistant', content: 'Here is a mock response from the AI coach. Based on my sources, you should make sure to lift heavy and eat protein.' });
    });
  });

  it('should start a new conversation when New Chat is clicked', () => {
    // Send a message to establish a conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Hello AI');
    cy.get('button[aria-label="Send message"]').click();
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Click New Chat button
    cy.contains('button', 'New Chat').click();

    // The chat should be cleared (empty state shown)
    cy.get('.empty-state').should('be.visible');

    // Conversation ID should be cleared from localStorage
    cy.window().then((win) => {
      const convId = win.localStorage.getItem('conversation_id');
      expect(convId).to.equal(null);
    });

    // Sending a new message should start a fresh conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('New conversation');
    cy.get('button[aria-label="Send message"]').click();
    cy.contains('Here is a mock response from the AI coach').should('be.visible');
    // The previous messages should not be visible
    cy.contains('Hello AI').should('not.be.visible');
    cy.contains('Hello AI from previous').should('not.be.visible'); // just to be sure
  });

  it('should clear conversation ID on logout', () => {
    // Send a message to establish a conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Hello AI');
    cy.get('button[aria-label="Send message"]').click();
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Simulate logout by clearing auth token and auth store
    cy.window().then((win) => {
      win.localStorage.removeItem('access_token');
      win.localStorage.removeItem('auth-store');
      // Also trigger a storage event to update the auth store if needed
      win.localStorage.setItem('access_token', ''); // dummy change to trigger event
    });

    // The chat should reset (empty state shown) because user is logged out
    // Note: Our ChatContainer uses the auth store user to determine if logged in.
    // We cleared the auth store, so the user becomes undefined.
    cy.get('.empty-state').should('be.visible');

    // Conversation ID should be cleared from localStorage
    cy.window().then((win) => {
      const convId = win.localStorage.getItem('conversation_id');
      expect(convId).to.equal(null);
    });
  });

  it('should show error message when history loading fails', () => {
    // Set an invalid conversation ID in localStorage
    cy.window().then((win) => {
      win.localStorage.setItem('conversation_id', 'invalid-id');
    });
    cy.reload();

    // After reload, the chat should show an error message
    cy.contains('Failed to load conversation history').should('be.visible');
    // And provide a button to start a new chat
    cy.contains('button', 'Start New Chat').should('be.visible');

    // The conversation ID should still be in localStorage (we do not clear it on failure)
    cy.window().then((win) => {
      const convId = win.localStorage.getItem('conversation_id');
      expect(convId).to.eq('invalid-id');
    });

    // Clicking the button should clear the conversation ID and reset the chat
    cy.contains('button', 'Start New Chat').click();
    cy.get('.empty-state').should('be.visible');
    cy.window().then((win) => {
      const convId = win.localStorage.getItem('conversation_id');
      expect(convId).to.equal(null);
    });
  });

  it('should exclude UI-only error messages from conversation history', () => {
    // First, set up an intercept to fail the first POST request
    cy.intercept('POST', '**/api/v1/chat/message', { statusCode: 500 }).as('failMessage');

    // Send a first message (which will fail)
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('First message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the failed request
    cy.wait('@failMessage').its('response.statusCode').should('eq', 500);

    // Check that the error message is visible
    cy.contains('I could not reach the AI service right now. Please check that the backend is running and try again.').should('be.visible');

    // Now, set up an intercept for the next POST to succeed (we'll mock a successful response)
    cy.intercept('POST', '**/api/v1/chat/message', (req) => {
      // This will handle the next POST and any subsequent ones.
      // We'll return a successful mock response.
      req.reply({
        statusCode: 200,
        body: {
          conversation_id: 1,
          message_id: 2,
          response: 'This is a successful response.',
          citations: [],
          safety_tier: 'Safe',
        }
      });
    }).as('succeedMessage');

    // Send a second message
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Second message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the successful request
    cy.wait('@succeedMessage').its('request.body').then((body) => {
      // Expect the payload to contain the conversation ID (should be 1)
      expect(body.conversation_id).to.eq(1);
      // Expect the history to contain only the first user message (the error message should be filtered out)
      expect(body.history).to.be.an('array').that.has.lengthOf(1);
      // Check the history item is the user's first message
      expect(body.history[0]).to.deep.equal({ role: 'user', content: 'First message' });
    });
  });
});