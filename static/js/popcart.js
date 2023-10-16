document.addEventListener('DOMContentLoaded', function() {
    // Your existing code

    const cartButton = document.querySelector('.add-to-cart');
    const popupModal = document.getElementById('popup-modal');
    const closeBtn = document.getElementById('close-modal');
    const popupMessage = document.getElementById('popup-message');

    cartButton.addEventListener('click', function() {
        // Add the product to the cart logic

        // Show the popup message
        popupMessage.textContent = 'Product added to cart!';
        popupModal.style.display = 'block';
    });

    closeBtn.addEventListener('click', function() {
        // Hide the popup modal
        popupModal.style.display = 'none';
    });

    // Close the modal if the user clicks outside the modal content
    window.addEventListener('click', function(event) {
        if (event.target === popupModal) {
            popupModal.style.display = 'none';
        }
    });
});
