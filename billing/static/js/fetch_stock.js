document.addEventListener("DOMContentLoaded", () => {
	const productSearch = document.getElementById("productSearch");

    // getting datas by XHR
	function get_xhr_datas(query) {
		fetch(`/stocksearch/?query=${query}`, {
			headers: {
				"X-Requested-With": "XMLHttpRequest",
			},
		})
			.then((response) => {
                if (!response.ok){
                    throw new Error("error");
                }
                return response.json();
            })
			.then((datas) => console.log(datas))
			.catch((e) => console.error("Error fetching data"));
	}

    // getting query
	productSearch.addEventListener("focus", () => {
		productSearch.value.length > 0 ? null : get_xhr_datas((query = ""));
	});

	productSearch.addEventListener("input", () => {
		get_xhr_datas(productSearch.value);
	});

    // creating dropdown
    function createDropDown(){
        const dropdown = document.getElementById("dropdown");
        dropdown.innerHTML = "";
    }

});
