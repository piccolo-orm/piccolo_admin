/// <reference types="Cypress" />

context('Startup', () => {
    beforeEach(() => {
        cy.visit('/#/login?nextURL=%2F')
    })

    it('Bulk update data', () => {
        // Fill the username
        cy.get('[name="username"]')
            .type('piccolo')
            .should('have.value', 'piccolo')

        // Fill the password
        cy.get('[name="password"]')
            .type('piccolo123')
            .should('have.value', 'piccolo123')

        // Locate and submit the form
        cy.get('form').submit();

        // Verify the app redirected you to the admin page
        cy.location('pathname', { timeout: 10000 })
            .should('eq', '/');

        // Verify the page title is "Piccolo Admin"
        cy.title()
            .should('eq', 'Piccolo Admin');

        cy.contains('director').click();

        // Update record in bulk
        cy.get('input[type="checkbox"]')
            .check({ force: true })
            .should('be.checked');

        cy.contains('Update 8 rows')
            .click();

        cy.wait(1000);

        // Choose from selects
        cy.get('select[name=property]')
            .select('gender');

        cy.get('select[name=gender]')
            .select('f');

        // Locate and submit the form
        cy.get('form').submit();

    });

});