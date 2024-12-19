const stockFieldValue = document.getElementById("stockField");
const stockQuantityValue = document.getElementById("stockCount");
const actualAmount = document.getElementById("actualAmount");
const gstRate = document.getElementById("gstRate");
const total = document.getElementById("total");
const priceFieldValue = document.getElementById("priceField");
const gst = document.getElementById("gst");

document.addEventListener("DOMContentLoaded", () => {
	gst.value = 18;
});

stockFieldValue.addEventListener("click", () => {
	stockFieldValue.value = "";
});

stockQuantityValue.addEventListener("input", () => {
	let stock = Number(stockFieldValue.value);
	let quantity = Number(stockQuantityValue.value);

	if (isNaN(stock)) stock = 0;
	if (isNaN(quantity)) quantity = 0;

	if (stock > 0 && quantity > stock) {
		stockQuantityValue.value = stock;
	} else if (quantity < 0) {
		stockQuantityValue.value = 0;
	}
});

stockQuantityValue.addEventListener("blur", () => {
	calcAmounts();
});

gst.addEventListener("blur", () => {
	calcAmounts();
});

priceFieldValue.addEventListener("blur", () => {
	calcAmounts();
});

function calcAmounts() {
	let quantity = Number(stockQuantityValue.value);
	let price = Number(priceFieldValue.value);
	let gstRateAmt = Number(gst.value);

	let actualAmountRS = Number((quantity * price).toFixed(2));
	let gstAmountRS = Number((actualAmountRS * gstRateAmt / 100).toFixed(2));

	actualAmount.value = actualAmountRS;
	gstRate.value = gstAmountRS;

	total.value = gstAmountRS + actualAmountRS;
}