// Add event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
  // Get all menu buttons
  const menuButtons = document.querySelectorAll('.menu-item');
  const sidebar = document.querySelector('.sidebar');
  const mainContent = document.querySelector('.main-content');
  const toggleBtn = document.querySelector('.toggle-btn');
  
  // Add click event listeners to menu buttons
  menuButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Remove active class from all buttons
      menuButtons.forEach(btn => btn.classList.remove('active'));
      // Add active class to clicked button
      button.classList.add('active');
    });
  });

  // Add click event listener to toggle button
  toggleBtn.addEventListener('click', () => {
    sidebar.classList.toggle('retracted');
    mainContent.classList.toggle('expanded');
  });

  // Get logout button
  const logoutButton = document.querySelector('.logout-btn');
  
  // Add click event listener to logout button
  logoutButton.addEventListener('click', () => {
    // Handle logout logic here
    console.log('Logout clicked');
  });
});