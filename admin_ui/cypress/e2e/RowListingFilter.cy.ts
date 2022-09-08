/// <reference types="Cypress" />

context('Startup', () => {
    beforeEach(() => {
        cy.visit('/#/login?nextURL=%2F');
    });

    it('Open director table and made basic filtering and sorting', () => {

        // Fill the username
        cy.get('[name="username"]')
            .type('piccolo')
            .should('have.value', 'piccolo');

        // Fill the password
        cy.get('[name="password"]')
            .type('piccolo123')
            .should('have.value', 'piccolo123');

        // Locate and submit the form
        cy.get('form')
            .submit();

        // Verify the app redirected you to the admin page
        cy.location('pathname', { timeout: 10000 })
            .should('eq', '/');

        // Verify the page title is "Piccolo Admin"
        cy.title()
            .should('eq', 'Piccolo Admin');

        // Click Director link
        cy.contains('director')
            .click();

        cy.contains('Show filters')
            .click();

        // Clear name field
        cy.get('[name="name"]')
            .focus()
            .clear();

        // Fill the search value
        cy.get('[name="name"]')
            .type('Howard')
            .should('have.value', 'Howard');

        // Clear filters
        cy.contains('Clear filters')
            .click();

        cy.wait(2000);

        // Again fill the search value
        cy.get('[name="name"]')
            .type('Howard')
            .should('have.value', 'Howard');

        // Locate and submit the form
        cy.get('form')
            .submit();

        // Close filter sidebar
        cy.contains('Close')
            .click();

        cy.wait(2000);

        cy.contains('Show filters')
            .click();

        // Clear filters to get all rows
        cy.contains('Clear filters')
            .click();

        cy.contains('Close')
            .click();

        cy.wait(2000);

        // Sort ascending
        cy.contains('Sort')
            .click();

        cy.get('[name="ordering"]').select('ascending');

        cy.get('button').contains('Sort')
            .click();

        cy.wait(3000);

        // Sort descending
        cy.contains('Sort')
            .click();

        cy.get('[name="ordering"]').select('descending');

        cy.get('button').contains('Sort')
            .click();

    });

});