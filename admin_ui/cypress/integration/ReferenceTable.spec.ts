/// <reference types="Cypress" />

Cypress.on('uncaught:exception', (err, runnable) => {
    // returning false here prevents Cypress from
    // failing the test
    return false
})

context('Startup', () => {
    beforeEach(() => {
        cy.visit('http://piccolo_admin/#/login?nextURL=/');
    });

    it('Open reference table in new window', () => {

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

        // Click Director link
        cy.contains('director')
            .click();

        cy.get('a[href*="#/director/8"]')
            .click()

        cy.contains('Show Referencing Tables')
            .click();

        cy.contains(' with a matching')
            .click();
        // make shure that rowID of FK works
        cy.visit('http://piccolo_admin/#/movie/?director=8');

        cy.visit("http://piccolo_admin/#/movie/10/");

        cy.contains('Back ')
            .click();

        cy.wait(2000);

        cy.visit("http://piccolo_admin/#/director/8/");

        cy.wait(2000);

        // Click Back link
        cy.contains('Back ')
            .click();

        cy.wait(2000);

        cy.visit("http://piccolo_admin/#/movie/10/");

        cy.wait(2000);

        // Click Back link
        cy.contains('Back ')
            .click();

        cy.wait(2000);

        cy.visit("http://piccolo_admin/#/director/8/");

        cy.wait(2000);

        // Click Back link
        cy.contains('Back ')
            .click();
    });

});