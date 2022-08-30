/// <reference types="Cypress" />

context('Startup', () => {
    beforeEach(() => {
        cy.visit('http://piccolo_admin/#/login?nextURL=%2F');
    });

    it('Open director table and made basic crud operations', () => {

        // Fill the username
        cy.get('[name="username"]')
            .type('piccolo')
            .should('have.value', 'piccolo');

        // Fill the password
        cy.get('[name="password"]')
            .type('piccolo123')
            .should('have.value', 'piccolo123');

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
            .click()

        cy.contains('h1', 'Edit director');

        // Clear name field
        cy.get('[name="name"]')
            .focus()
            .clear();

        // Fill field with new value
        cy.get('[name="name"]')
            .type('Ronald William Howard')
            .should('have.value', 'Ronald William Howard');

        cy.get('form')
            .submit();

        // Back to directors main page
        cy.contains('Back')
            .click();

        // Create record

        cy.wait(2000);

        cy.get('a[href*="#/director/add"]')
            .click();

        cy.contains('h1', 'Add director');

        // Fill field with new name value
        cy.get('[name="name"]')
            .type('Emerald Fennell')
            .should('have.value', 'Emerald Fennell');

        // Fill field with new years nominated value
        cy.get('a[href*="#"]')
            .contains('Add ')
            .click();

        cy.get('[id="choice"]')
            .type('2020')
            .should('have.value', '2020');

        // Fill field with new gender value
        cy.get('select')
            .select('f');

        cy.get('button')
            .contains('Create')
            .click();

        cy.contains('Back')
            .click();

        cy.wait(3000);

        // Delete single selected row 
        cy.get('input[type="checkbox"]').check('5')
            .check({ force: true })
            .should('be.checked')

        cy.wait(2000);

        cy.contains('Delete 1 rows')
            .click();

        cy.wait(3000);

        // Delete all selected rows 
        cy.get('input[type="checkbox"]')
            .check({ force: true })
            .should('be.checked')

        cy.contains('Delete 8 rows')
            .click();

        cy.wait(1000);

    });

});