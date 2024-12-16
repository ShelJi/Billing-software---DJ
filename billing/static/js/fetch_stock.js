document.addEventListener("DOMContentLoaded", () => {
	const productSearch = document.getElementById("productSearch");
	const dropdown = document.getElementById("dropdown");
	const priceField = document.getElementById("priceField");
	const stockField = document.getElementById("stockField");
	let products = [];
	let cart = [];

	// getting query
	productSearch.addEventListener("focus", () => {
		productSearch.value.length > 0 ? null : get_xhr_datas((query = ""));
	});

	productSearch.addEventListener("input", () => {
		get_xhr_datas(productSearch.value);
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
			productName =
				product.product_name.charAt(0).toUpperCase() +
				product.product_name.slice(1).toLowerCase();
			item.textContent = productName;
			dropdown.appendChild(item);
		});
	}

	// selection dropdown
	dropdown.addEventListener("click", (event) => {
		let selectedProduct = event.target.textContent;
		if (selectedProduct) {
			const product = products.find(
				(p) => p.product_name.toLowerCase() === selectedProduct.toLowerCase()
			);
			cart.push(product);
			dropdown.innerHTML = "";
		}
	});

	// show cart products
	function cartProducts() {
		console.log(cart);
	}

	cartProducts();
});

// document.addEventListener("DOMContentLoaded", () => {
// 	const productSearch = document.getElementById("productSearch");
// 	const dropdown = document.getElementById("dropdown");
// 	const priceField = document.getElementById("priceField");
// 	const stockField = document.getElementById("stockField");
// 	let products = [];

// 	// getting query
// 	productSearch.addEventListener("focus", () => {
// 		productSearch.value.length > 0 ? null : get_xhr_datas((query = ""));
// 	});

// 	productSearch.addEventListener("input", () => {
// 		get_xhr_datas(productSearch.value);
// 	});

// 	// getting datas by XHR
// 	function get_xhr_datas(query) {
// 		fetch(`/stocksearch/?query=${query}`, {
// 			headers: {
// 				"X-Requested-With": "XMLHttpRequest",
// 			},
// 		})
// 			.then((response) => {
// 				if (!response.ok) {
// 					throw new Error("error");
// 				}
// 				return response.json();
// 			})
// 			.then((datas) => {
// 				products = datas;
// 				createDropDown(products);
// 			})
// 			.catch((e) => console.error("Error fetching data"));
// 	}

// 	// creating dropdown
// 	function createDropDown(products) {
// 		dropdown.innerHTML = "";
// 		products.forEach((product) => {
// 			const item = document.createElement("div");
// 			productName =
// 				product.product_name.charAt(0).toUpperCase() +
// 				product.product_name.slice(1).toLowerCase();
// 			item.textContent = productName;
// 			dropdown.appendChild(item);
// 		});
// 	}

// 	// selection dropdown
// 	dropdown.addEventListener("click", (event) => {
// 		let selectedProduct = event.target.textContent;
// 		if (selectedProduct) {
// 			const product = products.find(
// 				(p) => p.product_name.toLowerCase() === selectedProduct.toLowerCase()
// 			);
// 			dropdown.innerHTML = "";
//             productSearch.value = selectedProduct;
//             priceField.value = product.product_prize;
//             stockField.value = product.product_stock;
// 		}
// 	});
// });
