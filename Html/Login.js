document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
  
    loginForm.addEventListener('submit', (e) => {
      e.preventDefault();
  
      const nome = document.getElementById('nome').value;
      const senha = document.getElementById('senha').value;
      const email = document.getElementById('email').value;
  
      // Here you can add your login logic
      console.log('Form submitted:', { nome, senha, email });
    });
  });