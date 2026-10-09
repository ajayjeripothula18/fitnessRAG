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

    // Wait for AI response to appear (accounting for animation/timing)
    cy.contains('Here is a mock response from the AI coach').should('be.visible');

    // Check for citations
    cy.get('a[href="https://example.com/fitness-fundamentals"]').should('be.visible').and('contain', '[1]');
    // Note: The second citation has no URL, so it's a span, let's just check for its text.
    cy.contains('[2]').should('be.visible');
  });

  it('should persist conversation ID and load history on refresh', () => {
    // Send a message to establish a conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Hello, AI!');
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
    // Wait for content to stabilize after reload (animation/timing)
    cy.contains('Hello, AI!').should('be.visible');
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

    // Set up MSW handler override to capture the second request's body
    let callCount = 0;
    let capturedRequestBody = null;

    cy.window().then(() => {
      if (window.__MSW__) {
        // Override with our capturing handler
        window.__MSW__.worker.use(
          window.__MSW__.http.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/chat/message`, async ({ request }) => {
            callCount++;
            const body = await request.json();

            // Store body for verification (from the request we want to check)
            if (callCount === 2) {
              capturedRequestBody = body;
            }

            // Delegate to original handler to get normal response
            return originalResolver({ request });
          })
        );
      }
    });

    // Send a second message
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Second message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the response to appear
    cy.contains('This is a successful response.').should('be.visible');

    // Verify that the request contains correct conversation ID and history
    cy.wait(50); // Small delay to ensure capture is complete
    cy.window().then(() => {
      // Verify we captured the second request
      expect(callCount).to.eq(2);
      expect(capturedRequestBody).to.not.be.null;
      expect(capturedRequestBody.conversation_id).to.eq(1);
      // Expect the history to contain the first turn (user message and AI response)
      expect(capturedRequestBody.history).to.be.an('array').that.has.lengthOf(2);
      // Check the first history item is the user's first message
      expect(capturedRequestBody.history[0]).to.deep.equal({ role: 'user', content: 'First message' });
      // Check the second history item is the AI's first response
      expect(capturedRequestBody.history[1]).to.deep.equal({ role: 'assistant', content: 'Here is a mock response from the AI coach. Based on my sources, you should make sure to lift heavy and eat protein.' });
    });
  });

  it('should start a new conversation when New Chat is clicked', () => {
    // Send a message to establish a conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Hello, AI!');
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
    cy.contains('Hello, AI!').should('not.exist');
    cy.contains('Hello, AI! from previous').should('not.exist'); // just to be sure
  });

  it('should clear conversation ID on logout', () => {
    // Send a message to establish a conversation
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Hello, AI!');
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
    cy.contains('I could not load your previous conversation history. Please try refreshing.').should('be.visible');
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
    // Spy on the request body to verify history excludes UI-only errors
    let callCount = 0;
    let capturedRequestBody = null;

    // Override MSW handler to capture request and respond appropriately
    cy.window().then(() => {
      if (window.__MSW__) {
        // Override with our capturing handler
        window.__MSW__.worker.use(
          window.__MSW__.http.post(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/v1/chat/message`, async ({ request }) => {
            callCount++;
            const body = await request.json();

            // Store body for later verification (from second call)
            if (callCount === 2) {
              capturedRequestBody = body;
            }

            // Simulate network failure on first call, success on second
            if (callCount === 1) {
              // First call - simulate network error
              return new __MSW__.HttpResponse(
                JSON.stringify({ error: 'Network error' }),
                { status: 500, headers: { 'Content-Type': 'application/json' } }
              );
            } else {
              // Second call - return success
              return new __MSW__.HttpResponse(
                JSON.stringify({
                  conversation_id: 1,
                  message_id: 2,
                  response: 'This is a successful response.',
                  citations: [],
                  safety_tier: 'Safe',
                }),
                { status: 200, headers: { 'Content-Type': 'application/json' } }
              );
            }
          })
        );
      }
    });

    // Send a first message (which will fail due to our override)
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('First message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the error message to appear
    cy.contains('I could not reach the AI service right now. Please check that the backend is running and try again.').should('be.visible');

    // Send a second message
    cy.get('textarea[placeholder*="Ask your AI fitness coach"]').type('Second message');
    cy.get('button[aria-label="Send message"]').click();

    // Wait for the successful response
    cy.contains('This is a successful response.').should('be.visible');

    // Verify that the second request's history excludes the UI-only error message
    cy.wait(50); // Small delay to ensure capture is complete
    cy.window().then((win) => {
      // Verify we captured the second request
      expect(callCount).to.eq(2);
      expect(capturedRequestBody).to.not.be.null;
      expect(capturedRequestBody.conversation_id).to.eq(1);
      // The history should contain only the first user message (not the error message)
      expect(capturedRequestBody.history).to.be.an('array').that.has.lengthOf(1);
      expect(capturedRequestBody.history[0]).to.deep.equal({ role: 'user', content: 'First message' });
    });
  });
});