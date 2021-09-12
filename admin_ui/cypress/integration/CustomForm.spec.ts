/// <reference types="Cypress" />

// to run test we have to setting up a Local SMTP Server
// python -m smtpd -c DebuggingServer -n localhost:1025

context('Startup', () => {
    beforeEach(() => {
        cy.visit('http://piccolo_admin/#/login?nextURL=%2F');
    });

    it('Fill custom forms', () => {

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

        cy.contains(' Business email form ')
            .click();

        cy.wait(2000);

        // Fill custom form
        cy.get('[name="email"]')
            .type('director@director.com')
            .should('have.value', 'director@director.com');

        cy.get('[name="title"]')
            .type('Hello')
            .should('have.value', 'Hello');

        cy.get('[name="content"]')
            .type('Hello from Piccolo Admin')
            .should('have.value', 'Hello from Piccolo Admin');

        // Locate and submit the form
        cy.get('form')
            .submit();

        cy.wait(2000);


        cy.contains(' Friends email form ')
            .click();

        cy.wait(2000);

        // Fill custom form
        cy.get('[name="email"]')
            .type('friend@friend.com')
            .should('have.value', 'friend@friend.com');

        cy.get('[name="title"]')
            .type('Hello friend')
            .should('have.value', 'Hello friend');

        cy.get('[name="content"]')
            .type('Hello from Piccolo Admin')
            .should('have.value', 'Hello from Piccolo Admin');

        // Locate and submit the form
        cy.get('form')
            .submit();

    });

});