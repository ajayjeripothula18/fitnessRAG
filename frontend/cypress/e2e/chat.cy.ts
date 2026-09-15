describe('Chat Interface', () => {
  beforeEach(() => {
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
});
