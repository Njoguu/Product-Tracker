async function fetchSearchTexts() {
    const response = await fetch('unique-search-texts/');
    const data = await response.json();

    const searchTextContainer = document.getElementById('searchTextContainer');
    const ul = document.createElement('ul'); // Create the <ul> element

    data.search_text.forEach(searchText => {
        const li = document.createElement('li'); // Create an <li> element

        const button = document.createElement('button'); // Create a button element
        button.textContent = searchText;
        button.addEventListener('click', () => {
            fetchDataAndPopulateTable(searchText);
        });

        li.appendChild(button); // Add the button to the <li>
        ul.appendChild(li); // Add the <li> to the <ul>
    });

    searchTextContainer.appendChild(ul); // Add the <ul> to the container
}


async function fetchTrackedProducts() {
    const response = await fetch('tracked-products/');
    const data = await response.json();

    const trackedProductsContainer = document.getElementById('trackedProductsContainer');
    const ul = document.createElement('ul'); // Create the <ul> element

    data.products.forEach(trackedProduct => {
        const li = document.createElement('li'); // Create an <li> element

        const label = document.createElement('label'); // Create a label element
        const textNode = document.createTextNode(trackedProduct.name);
        label.appendChild(textNode);

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = trackedProduct.name;
        if (trackedProduct.tracked == true) {
            checkbox.checked = true
        }

        li.appendChild(label); // Add the label to the <li> element
        li.appendChild(checkbox); // Add the checkbox to the <li> element
        ul.appendChild(li); // Add the <li> to the <ul>
    });

    trackedProductsContainer.appendChild(ul); // Add the <ul> to the container
}


async function fetchDataAndPopulateTable(searchText){
    const response = await fetch(`results?search_text=${searchText}`);
    const data = await response.json();

    // Get the table body element
    const tableBody = document.querySelector('#data-table tbody');

    // Clear the existing table rows
    tableBody.innerHTML = '';

    // Loop through the data and create table rows
    data.forEach(product => {
        const row = document.createElement('tr');
        row.classList.add("clickable-row");
        row.setAttribute("data-href", product.name);
        // Create a new Date object from the datetime string
        const dateTime = new Date(product.created_at);

        // Define the date and time options for formatting
        const options = {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
            timeZoneName: 'short',
        };

        // Get the formatted date and time string
        const formattedDateTime = new Intl.DateTimeFormat('en-US', options).format(dateTime); 
        row.innerHTML = `
          <td>${formattedDateTime}</td>
          <td>${product.name}</td>
          <td>Ksh ${product.priceHistory[0].price}</td>
          <td>+0%</td>
        `;
        tableBody.appendChild(row);
      });
}

function searchProducts() {
    const searchBar = document.getElementById('searchBar');
    const searchText = searchBar.value;

    if (searchText.trim() === '') {
        // If the search box is empty, do nothing
        return;
    }

    const data = {
        url: "https://jumia.co.ke",
        search_text: searchText
    };

    // Send the data as a parameter in a POST request
    fetch('start-scraper/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}

// Add tracked product
function addTrackedProduct(){
    const addTrackedProduct = document.getElementById('addTrackedProduct');
    const productName = addTrackedProduct.value;

    if (productName.trim() === '') {
        // If the search box is empty, do nothing
        return;
    }

    const data = {
        name: productName
    };

    // Send the data as a parameter in a POST request
    fetch('add-tracked-product/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    window.location.reload();
}
let priceChart; // Declare the variable here
document.addEventListener('DOMContentLoaded', (event) => {
    const table = document.getElementById('data-table');
    const productModal = document.getElementById('productModal');
    const productModalName = document.getElementById('productModalName');
    const modalImage = document.getElementById('modalImage');
    const modalUrl = document.getElementById('modalUrl');
    const modalPrice = document.getElementById('modalPrice');
    const priceHistoryChart = document.getElementById('priceHistoryChart');
    

    // Add event listener to the table
    table.addEventListener('click', (event) => {
        const clickedRow = event.target.closest('tr');
        if (!clickedRow || !clickedRow.classList.contains('clickable-row')) return; // Make sure a clickable row was clicked

        const productName = clickedRow.dataset.href;
        console.log(`Selected Product Name: ${productName}`);

        fetch(`/product?name=${productName}`)
            .then(response => response.json())
            .then(data => {
                // Update the modal content with the fetched data
                productModalName.textContent = data.name;
                modalImage.src = data.img;
                modalUrl.textContent = `Product Url: ${data.url}`;
                modalPrice.textContent = `Current price: ${data.price}`;

                // Optionally, create and update the price history chart using Chart.js
                // For example:
                const priceHistory = data.priceHistory;
                const dates = priceHistory.map(entry => entry.date);
                const prices = priceHistory.map(entry => entry.price);

                priceChart = new Chart(priceHistoryChart, {
                    type: 'line',
                    data: {
                        labels: dates,
                        datasets: [{
                            label: 'Price History',
                            data: prices,
                            borderColor: 'blue',
                            fill: false
                        }]
                    },
                    options: {
                        responsive: true
                    }
                });

                // Show the modal
                productModal.style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching product details:', error);
            });
    });
});


// Function to close the modal
function closeModal() {
    priceChart.destroy();
    document.getElementById('productModal').style.display = 'none';
}