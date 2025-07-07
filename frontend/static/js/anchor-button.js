/**
 * Anchor Button Transformation
 *
 * This script handles the transformation of the Anchor button to a Back button
 * when on the Anchor page, and ensures proper navigation between pages.
 */

document.addEventListener('DOMContentLoaded', function() {
  let lastWorkspacePage = '/doing';

  // Function to handle clicks on the anchor button
  function handleAnchorButtonClick(event) {
    const anchorButton = event.target.closest('#anchor-button');
    if (!anchorButton) return;

    const currentPath = window.location.pathname;
    const isInAnchorPage = currentPath.startsWith('/anchor');

    if (isInAnchorPage) {
      // We're on the anchor page and clicking the back button
      event.preventDefault();

      // Get the destination from session storage or default to /doing
      const destination = sessionStorage.getItem('lastWorkspacePage') || '/doing';

      // Navigate to the destination
      window.location.href = destination;
    } else {
      // We're not on the anchor page and clicking the anchor button
      event.preventDefault();

      // Store the current page as the last workspace page
      // Make sure we're storing a valid workspace page path
      const validWorkspacePages = ['/doing', '/done', '/plan'];
      const pathToStore = validWorkspacePages.includes(currentPath) ? currentPath : '/doing';

      sessionStorage.setItem('lastWorkspacePage', pathToStore);

      // Navigate to the anchor page
      window.location.href = '/anchor';
    }
  }

  // Add click event listener to the anchor button
  document.addEventListener('click', function(event) {
    const anchorButton = event.target.closest('#anchor-button');
    if (anchorButton) {
      handleAnchorButtonClick(event);
    }
  });
});
