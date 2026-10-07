/// <reference types="cypress" />
/// <reference types="cypress-axe" />

describe('Profile Management', () => {
  beforeEach(() => {
    // Set up mock authentication state
    cy.window().then((win) => {
      win.localStorage.setItem('access_token', 'mock_token');
      win.localStorage.setItem('auth-store', JSON.stringify({
        state: {
          user: { id: 1, email: 'test@example.com', full_name: 'Test User' },
          isAuthenticated: true
        },
        version: 0
      }));
    });
    cy.visit('/settings');
    cy.injectAxe();
  });

  it('should pass accessibility tests', () => {
    // Wait for the profile form to load
    cy.get('input[id="profile-name"]').should('be.visible');

    // Check accessibility with axe
    cy.checkA11y(undefined, { includedImpacts: ['critical', 'serious', 'moderate', 'minor'] }, (violations: any[]) => {
      cy.task(
        'log',
        `${violations.length} accessibility violation${
          violations.length === 1 ? '' : 's'
        } ${violations.length === 1 ? 'was' : 'were'} detected`
      );

      const violationData = violations.map(
        (violation: any) => ({
          id: violation.id,
          impact: violation.impact,
          description: violation.description,
          nodes: violation.nodes.length,
          html: violation.nodes[0]?.html
        })
      );

      cy.task('table', violationData);
    });
  });

  it('should load existing profile data and display in form', () => {
    // Check that form fields are populated with mock data
    cy.get('input[id="profile-name"]').should('have.value', 'Test User');
    cy.get('input[id="profile-age-range"]').should('have.value', '25-34');
    cy.get('select[id="profile-sex"]').should('have.value', 'male');
    cy.get('input[id="profile-height"]').should('have.value', '180');
    cy.get('input[id="profile-weight"]').should('have.value', '75');
    cy.get('select[id="profile-fitness-level"]').should('have.value', 'intermediate');
    cy.get('input[id="profile-primary-goal"]').should('have.value', 'muscle_gain');
    cy.get('input[id="profile-dietary-preference"]').should('have.value', 'omnivore');
    cy.get('textarea[id="profile-allergies"]').should('have.value', 'none');
    cy.get('textarea[id="profile-available-equipment"]').should('have.value', 'dumbbells, yoga mat');
    cy.get('select[id="profile-workout-location"]').should('have.value', 'home');
    cy.get('input[id="profile-days-per-week"]').should('have.value', '3');
    cy.get('input[id="profile-session-duration"]').should('have.value', '45');
    cy.get('textarea[id="profile-food-preferences"]').should('have.value', 'high protein');
    cy.get('textarea[id="profile-food-dislikes"]').should('have.value', 'none');
    cy.get('textarea[id="profile-experience-exercises"]').should('have.value', 'squats, push-ups, running');
  });

  it('should allow editing profile fields and submit successfully', () => {
    // Override the MSW handler for this test to delay the PUT request so we can observe the saving state
    cy.window().then((win) => {
      // @ts-ignore: __MSW__ is attached to window in main.tsx when Cypress is present
      const { worker, http, HttpResponse } = win.__MSW__;
      worker.use(
        http.put('http://localhost:8000/api/v1/users/me/profile', async ({ request }: { request: any }) => {
          // Delay the response by 100ms to observe the saving state
          await new Promise(resolve => setTimeout(resolve, 100));
          const profileUpdate = await request.json();
          return HttpResponse.json(profileUpdate);
        })
      );
    });

    // Clear and update a few fields
    cy.get('input[id="profile-name"]').clear().type('Updated Name');
    cy.get('input[id="profile-weight"]').clear().type('80');
    cy.get('select[id="profile-fitness-level"]').select('advanced');

    // Submit the form
    cy.get('button[id="profile-save-btn"]').click();

    // Should show saving state then success message
    cy.get('button[id="profile-save-btn"]').should('contain', 'Saving…');
    cy.get('div[role="status"]').should('contain', 'Profile saved successfully!');

    // Verify the updated values are reflected in the form
    cy.get('input[id="profile-name"]').should('have.value', 'Updated Name');
    cy.get('input[id="profile-weight"]').should('have.value', '80');
    cy.get('select[id="profile-fitness-level"]').should('have.value', 'advanced');
  });

  it('should handle GET error when profile cannot be loaded', () => {
    // Override the MSW handler for this test to return an error
    cy.window().then((win) => {
      // @ts-ignore: __MSW__ is attached to window in main.tsx when Cypress is present
      const { worker, http, HttpResponse } = win.__MSW__;
      worker.use(
        http.get('http://localhost:8000/api/v1/users/me/profile', () => {
          return HttpResponse.json({ detail: 'Profile not found' }, { status: 404 });
        })
      );
    });

    // Invalidate the profile query to trigger a refetch with the overridden handler
    cy.window().then((win) => {
      // @ts-ignore: __QUERY_CLIENT__ is attached to window in App.tsx when Cypress is present
      const queryClient = win.__QUERY_CLIENT__;
      queryClient.invalidateQueries({ queryKey: ['profile'] });
    });

    // Should show error message
    cy.get('h2').should('contain', 'Failed to load profile');
    cy.get('p').should('contain', 'Profile not found');
    cy.get('button').should('contain', 'Retry');
  });

  it('should handle PUT error when profile cannot be saved', () => {
    // Override the MSW handler for this test to return an error
    cy.window().then((win) => {
      // @ts-ignore: __MSW__ is attached to window in main.tsx when Cypress is present
      const { worker, http, HttpResponse } = win.__MSW__;
      worker.use(
        http.put('http://localhost:8000/api/v1/users/me/profile', () => {
          return HttpResponse.json({ detail: 'Internal server error' }, { status: 500 });
        })
      );
    });

    // Try to update a field
    cy.get('input[id="profile-weight"]').clear().type('90');

    // Submit the form
    cy.get('button[id="profile-save-btn"]').click();

    // Should show error message
    cy.get('div[role="alert"]').should('contain', 'Internal server error');
    cy.get('div[role="status"]').should('not.exist');

    // User-entered value should be maintained (not reverted)
    cy.get('input[id="profile-weight"]').should('have.value', '90');
  });

  it('should show client-side validation error for invalid input', () => {
    // Try to update a field with invalid data (negative weight)
    cy.get('input[id="profile-weight"]').clear().type('-5');

    // Submit the form - should trigger client-side validation
    cy.get('button[id="profile-save-btn"]').click();

    // Should show client-side validation error, not success
    cy.get('div[role="alert"]').should('not.exist'); // No save error yet
    cy.get('div[role="status"]').should('not.exist'); // No success message
    cy.get('input[id="profile-weight"]').should('have.class', 'border-[var(--color-error)]');
    cy.get('span[id="profile-weight-error"]').should('be.visible')
      .and('contain', 'Number must be greater than 0');
  });

  it('should handle PUT error when profile cannot be saved (different field)', () => {
    // Override the MSW handler for this test to return an error
    cy.window().then((win) => {
      // @ts-ignore: __MSW__ is attached to window in main.tsx when Cypress is present
      const { worker, http, HttpResponse } = win.__MSW__;
      worker.use(
        http.put('http://localhost:8000/api/v1/users/me/profile', () => {
          return HttpResponse.json({ detail: 'Internal server error' }, { status: 500 });
        })
      );
    });

    // Try to update a different field
    cy.get('input[id="profile-height"]').clear().type('175');

    // Submit the form
    cy.get('button[id="profile-save-btn"]').click();

    // Should show error message
    cy.get('div[role="alert"]').should('contain', 'Internal server error');
    cy.get('div[role="status"]').should('not.exist');

    // User-entered value should be maintained (not reverted)
    cy.get('input[id="profile-height"]').should('have.value', '175');
  });
});