/// <reference types="Cypress" />

context('Startup', () => {
    beforeEach(() => {
        cy.visit('http://piccolo_admin/#/login?nextURL=%2F');
    });

    it('Fill login form and redirect to admin page and then logout', () => {

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

        // Verify the app redirected to the admin page
        cy.location('pathname', { timeout: 2000 })
            .should('eq', '/');

        // Verify the page title is "Piccolo Admin"
        cy.title()
            .should('eq', 'Piccolo Admin');

        cy.wait(2000);

        cy.contains('piccolo')
            .click();

        // Logout and redirected to the login page
        cy.contains('Log out')
            .click();

        // Verify the app redirected to the login page
        cy.location('pathname', { timeout: 2000 }).
            should('eq', '/');

    });

});