// Test script to verify TodoList add button functionality
console.log('Testing TodoList add button functionality...');

// Function to test the add button
function testAddButton() {
    // Wait for page to load
    setTimeout(() => {
        console.log('Looking for add button...');
        
        // Find the add button
        const addButton = document.getElementById('add-todo-button');
        if (addButton) {
            console.log('Add button found:', addButton);
            
            // Simulate click
            console.log('Simulating click on add button...');
            addButton.click();
            
            // Check if modal opened
            setTimeout(() => {
                const modal = document.querySelector('[role="dialog"]');
                if (modal) {
                    console.log('✅ Success: Modal opened after clicking add button');
                } else {
                    console.log('❌ Error: Modal did not open');
                }
            }, 500);
        } else {
            console.log('❌ Error: Add button not found');
        }
    }, 2000);
}

// Run test when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', testAddButton);
} else {
    testAddButton();
}
