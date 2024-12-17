const productSearch = document.getElementById("productSearch");
const dropdown = document.getElementById("dropdown");
const priceField = document.getElementById("priceField");
const stockField = document.getElementById("stockField");
const stockCount = document.getElementById("stockCount");
const productID = document.getElementById("productID");
const table = document.getElementById("table");
const checkout = document.getElementById("checkout");
const date = document.getElementById("dateField");

const tableHead = `
<table id="cartTable">
    <thead>
        <tr>
            <th>Product Name</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Total</th>
            <th>Remove</th>
        </tr>
    </thead>
    <tbody>
        
    </tbody>
</table>`;

let products = [];
let cart = [];

const today = new Date();
const formattedDate = today.toISOString().split("T")[0];
date.value = formattedDate;

document.addEventListener("DOMContentLoaded", () => {
	// getting query
	productSearch.addEventListener("focus", () => {
		productSearch.value.length > 0 ? null : get_xhr_datas((query = ""));
	});

	productSearch.addEventListener("input", () => {
		get_xhr_datas(productSearch.value.trim());
	});

	// getting datas by XHR
	function get_xhr_datas(query) {
		fetch(`/stocksearch/?query=${query}`, {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		})
			.then((response) => {
				if (!response.ok) {
					throw new Error("error");
				}
				return response.json();
			})
			.then((datas) => {
				products = datas;
				createDropDown(products);
			})
			.catch((e) => console.error("Error fetching data"));
	}

	// creating dropdown
	function createDropDown(products) {
		dropdown.innerHTML = "";
		products.forEach((product) => {
			const item = document.createElement("div");
			let productName = capitalize(product.product_name);
			item.textContent = productName;
			dropdown.appendChild(item);
		});
		dropdown.style.display = "block";
	}

	// selection dropdown
	dropdown.addEventListener("click", (event) => {
		let selectedProduct = event.target.textContent;
		if (selectedProduct) {
			const product = products.find(
				(p) => p.product_name.toLowerCase() === selectedProduct.toLowerCase()
			);
			dropdown.innerHTML = "";
			productSearch.value = selectedProduct;
			priceField.value = product.product_prize;
			stockField.value = product.product_stock;
			productID.value = product.id;
			dropdown.innerHTML = "";
		}
		dropdown.style.display = "none";
	});

	// Hide dropdown when clicking outside
	document.addEventListener("click", (event) => {
		if (!dropdown.contains(event.target) && event.target !== productSearch) {
			dropdown.innerHTML = "";
			dropdown.style.display = "none";
		}
	});
});

// add item
function addItem() {
	if (
		productSearch.value.trim().length > 0 &&
		priceField.value.trim().length > 0 &&
		stockCount.value.trim().length > 0
	) {
		let productName = capitalize(productSearch.value.trim());
		cart.push({
			productID: productID.value.trim(),
			product_name: productName,
			price: priceField.value.trim(),
			quantity: stockCount.value.trim(),
		});
		clearFields();
		refreshTable();
	} else {
		console.log("Fill all fields");
	}
}

// clear inputs
function clearFields() {
	productID.value = "";
	productSearch.value = "";
	priceField.value = "";
	stockField.value = "";
	stockCount.value = "";
}

// capitalize name
function capitalize(name) {
	name = name.trim();
	return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
}

// create table
function refreshTable() {
	if (!document.getElementById("cartTable") && cart.length !== 0) {
		table.innerHTML = tableHead;
		checkout.style.display = "block";
	} else if (cart.length === 0) {
		table.innerHTML = "";
		checkout.style.display = "none";
		return;
	}

	const cartTableBody = document.querySelector("#cartTable tbody");
	cartTableBody.innerHTML = "";

	cart.forEach((item) => {
		const row = document.createElement("tr");

		// Product Name
		const nameCell = document.createElement("td");
		nameCell.textContent = item.product_name;
		row.appendChild(nameCell);

		// Price
		const priceCell = document.createElement("td");
		priceCell.textContent = `Rs ${item.price}`;
		row.appendChild(priceCell);

		// Quantity
		const quantityCell = document.createElement("td");
		quantityCell.textContent = item.quantity;
		row.appendChild(quantityCell);

		// Total (Price * Quantity)
		const totalCell = document.createElement("td");
		totalCell.textContent = `Rs ${item.price * item.quantity}`;
		row.appendChild(totalCell);

		// remove
		const removeCell = document.createElement("td");
		const removeButton = document.createElement("button");
		removeButton.textContent = "Remove";
		removeButton.addEventListener("click", () => {
			cart.splice(index, 1);
			refreshTable();
		});
		removeCell.appendChild(removeButton);
		row.appendChild(removeCell);	

		// Append the row to the table
		cartTableBody.appendChild(row);
	});
}