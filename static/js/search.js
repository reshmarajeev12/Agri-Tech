document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const resultsContainer = document.getElementById('results-container');

    // Replace this with your actual product data
    const products = [
        { name: 'Product 1', description: 'Description of Product 1' },
        { name: 'Product 2', description: 'Description of Product 2' },
        // Add more products
    ];

    function displayResults(searchTerm) {
        resultsContainer.innerHTML = '';

        products.forEach(product => {
            const productElement = document.createElement('div');
            productElement.className = 'product';
            const highlightedName = product.name.replace(new RegExp(searchTerm, 'gi'), match => `<span class="highlight">${match}</span>`);
            productElement.innerHTML = `
                <h3>${highlightedName}</h3>
                <p>${product.description}</p>
            `;
            resultsContainer.appendChild(productElement);
        });
    }

    searchButton.addEventListener('click', function() {
        const searchTerm = searchInput.value;
        displayResults(searchTerm);
    });

    searchInput.addEventListener('input', function() {
        const searchTerm = searchInput.value;
        displayResults(searchTerm);
    });
});