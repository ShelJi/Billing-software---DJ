const phone_no = document.getElementById("phone_no");
const username = document.getElementById("username");
const email = document.getElementById("email");
const address = document.getElementById("address");
const dateField = document.getElementById("dateField");
const dropdownuser = document.getElementById("dropdownuser");

let usersData = [];

document.addEventListener("DOMContentLoaded", () => {
	// get query
	phone_no.addEventListener("input", () => {
		get_xhr_customer(phone_no.value.trim());
	});

	// get xhr user datas
	function get_xhr_customer(query) {
		fetch(`/customersearch/?query=${query}`, {
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
				usersData = datas;
				createDropdownUser(usersData);
			})
			.catch((e) => console.error("error fetching data", e));
	}

	// create dropdown
	function createDropdownUser(datas) {
		dropdownuser.innerHTML = "";
		datas.forEach((user) => {
			const child = document.createElement("div");
			child.textContent = `${user.phone_no} - ${user.username}`;
			child.dataset.phoneNo = user.phone_no;
			dropdownuser.appendChild(child);
		});
		dropdownuser.style.display = "block";
	}

	// select dropdown
	dropdownuser.addEventListener("click", (event) => {
		let selectedProduct = event.target.dataset.phoneNo;
		if (selectedProduct) {
			const user = usersData.find((p) => p.phone_no === selectedProduct);
			dropdownuser.innerHTML = "";
			phone_no.value = user.phone_no;
			username.value = user.username;
			email.value = user.email;
			address.value = user.address;
			dropdownuser.innerHTML = "";
			dropdownuser.style.display = "none";
		}
	});

	// Hide dropdown when clicking outside
	document.addEventListener("click", (event) => {
		if (!dropdownuser.contains(event.target) && event.target !== phone_no) {
			dropdownuser.innerHTML = "";
			dropdownuser.style.display = "none";
		}
	});
});
