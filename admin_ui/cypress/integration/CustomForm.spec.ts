/// <reference types="Cypress" />

// The custom form sends emails - if you want to see these, set up a
// Local SMTP Server:
// python -m smtpd -c DebuggingServer -n localhost:1025

context('Startup', () => {
    beforeEach(() => {
        cy.visit('/#/login?nextURL=%2F')
    })

    it('Fill custom forms', () => {
        // Fill the username
        cy.get('[name="username"]')
            .type('piccolo')
            .should('have.value', 'piccolo')

        // Fill the password
        cy.get('[name="password"]')
            .type('piccolo123')
            .should('have.value', 'piccolo123')

        // Locate and submit the form
        cy.get('form').submit()

        // Verify the app redirected to the admin page
        cy.location('pathname', { timeout: 2000 }).should('eq', '/')

        // Verify the page title is "Piccolo Admin"
        cy.title().should('eq', 'Piccolo Admin')

        cy.wait(2000)

        cy.contains('Business email form').click()

        cy.wait(2000)

        // Fill custom form
        cy.get('[name="email"]')
            .type('director@director.com')
            .should('have.value', 'director@director.com')

        cy.get('[name="title"]')
            .clear()
            .type('Hello')
            .should('have.value', 'Hello')

        cy.get('[name="content"]')
            .type('Hello from Piccolo Admin')
            .should('have.value', 'Hello from Piccolo Admin')

        // Locate and submit the form
        cy.get('form').submit()

        cy.wait(2000)

        cy.contains('Back').click()

        cy.contains('Booking form').click()

        cy.wait(2000)

        // Fill custom form
        cy.get('[name="email"]')
            .type('customer@customer.com')
            .should('have.value', 'customer@customer.com')

        cy.get('[name="name"]')
            .type('Bob')
            .should('have.value', 'Bob')

        cy.get('[name="notes"]')
            .clear()
            .type('Star Wars please')
            .should('have.value', 'Star Wars please')

        // Locate and submit the form
        cy.get('form').submit()
    })
})
