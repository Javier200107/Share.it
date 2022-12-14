describe('Remind credentials', () => {

  it('Deberia poder hacer login recordando las credenciales, cerrar sesion y comprobar que se hayan recordado', () => {
    cy.visit('/login')
    // Rellena el formulario con los datos necesarios
    cy.get('input[id="usuari"]').type('mr50');
    cy.get('input[id="password"]').type('Mr345678');

    // click en el boton de recordar credenciales
    cy.get('input[id="flexCheckDefault"]').click();

    // Haz clic en el boton de login
    cy.get('button[id="login-btn"]').click();

    // Comprueba que se haya enviado correctamente
    cy.contains('Home');

    // cerramos sesion
    cy.get('strong[id="user-menu"]').click();
    cy.contains('Sign out').click();

    // comprobamos que se recuerden
    cy.get('a[id="login"]').click();
    cy.get('input[id="usuari"]').should('have.value', 'mr50');
    cy.get('input[id="password"]').should('have.value', 'Mr345678');

  })

})
