/// <reference types="Cypress" />

context('Startup', () => {
    beforeEach(() => {
        cy.visit('/#/login?nextURL=%2F')
    })

    it('File upload', () => {
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

        // Update record
        cy.wait(2000);

        cy.get('a[href*="#/director/8"]')
            .click();

        cy.contains('h1', 'Edit director');

        // Select file to upload
        cy.get('input[type=file]').selectFile({
            contents: 'cypress/fixtures/piccolo.jpg',
            mimeType: 'image/png'
        })

        cy.wait(3000);

        // Locate and submit the form
        cy.get('form').submit();

        // Go back to directors page
        cy.contains('a', 'Back').click();

        cy.wait(2000);

        // View the uploaded file
        cy.contains('table tr td span a', '.jpg')
            .click();

        cy.wait(3000);

        // Close preview of uploaded file
        cy.get('div#media_viewer div.top_bar p.close a')
            .click();

    });

});