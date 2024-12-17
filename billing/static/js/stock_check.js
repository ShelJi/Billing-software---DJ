const stockFieldValidate = document.getElementById("stockField");
const stockCountValidate = document.getElementById("stockCount");

stockFieldValidate.addEventListener("click", () => {
    stockFieldValidate.value = "";
});

stockCountValidate.addEventListener("input", () => {
    let stock = Number(stockFieldValidate.value);
    let count = Number(stockCountValidate.value);

    if (isNaN(stock)) stock = 0;
    if (isNaN(count)) count = 0;

    if (stock > 0 && count > stock) {
        stockCountValidate.value = stock;
    } else if (count < 0) {
        stockCountValidate.value = 0; 
    }
});
