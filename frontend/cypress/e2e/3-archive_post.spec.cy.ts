describe('Archive post', () => {
  it('Entro con una cuenta existente, archivo y desarchivo un post', () => {
    cy.visit('/')
    cy.contains('Log in').click()
    // Rellena el formulario con los datos necesarios
    cy.get('input[id="usuari"]').type('mr50')
    cy.get('input[id="password"]').type('Mr345678')

    cy.wait(1000)

    // Haz clic en el boton de login
    cy.get('button[id="login-btn"]').click()

    cy.wait(1000)

    // Comprueba que se haya entrado correctamente
    cy.contains('Home')

    // Voy a la pagina de perfil
    cy.get('strong[id="user-menu"]').click()
    cy.contains('Profile').click()

    // Busco el post y lo archivo
    cy.get('div[id="archived-btn-mr50"]').click()

    // Compruebo que esté en la lista de archivados
    cy.contains('Archived posts').click()
    cy.get('div[id="post-mr50"]')
      .find('p').should('have.text', 'Hello World!')

    // Desarchivo el post
    cy.get('div[id="archived-btn-mr50"]').click()

    // Compruebo que esté en la lista de posts desarchivados
    cy.contains('Posts').click()
    cy.get('div[id="post-mr50"]')
      .find('p').should('have.text', 'Hello World!')
  })
})
