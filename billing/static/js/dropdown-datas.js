document.addEventListener("DOMContentLoaded", function () {
	let query = "";
	let products = [];

	document.getElementById("productSearch").addEventListener("input", function (event) {
		query = event.target.value;
		if (query.length > 0) {
			get_xhr_datas(query);
		} else {
			clearDropdown();
		}
	});

	document.getElementById("dropdown").addEventListener("click", function (event) {
		if (event.target && event.target.matches(".dropdown-item")) {
			let selectedProduct = event.target.textContent;

			let product = products.find((p) => p.product_name === selectedProduct);
			if (product) {
				document.getElementById("priceField").value = product.price;
			}
			clearDropdown();
		}
	});

	function get_xhr_datas(query) {
		fetch(`/stocksearch/?query=${query}`, {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		})
			.then((response) => response.json())
			.then((data) => {
				products = data;
				showDropdown(products);
			});
	}

	function showDropdown(products) {
		const dropdown = document.getElementById("dropdown");
		dropdown.innerHTML = "";

		products.forEach((product) => {
			const item = document.createElement("div");
			item.classList.add("dropdown-item");
			item.textContent = product.product_name;
			dropdown.appendChild(item);
		});
	}

	function clearDropdown() {
		const dropdown = document.getElementById("dropdown");
		dropdown.innerHTML = "";
	}
});
