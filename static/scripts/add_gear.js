// VALIDATE USER'S INPUT
const form = document.getElementById("addForm");
form.addEventListener('submit', validate);
async function validate(event) {
    event.preventDefault();
    const errorMessage = document.getElementById("errorMessage");
    const model = document.getElementsByName("model")[0].value.trim();
    const price = document.getElementsByName("price")[0].value.trim();
    const brand = document.getElementsByName("brand")[0].value.trim();
    const formType = document.getElementsByName("formType")[0].value.trim();
    if ( model.length <= 0 || price.length <= 0 || brand.length <= 0) {
        errorMessage.innerHTML = "All fields must be filled";
        return false;
    }
    if (isNaN(price)) {
        errorMessage.innerHTML = "Incorrect price format";
        return false;
    }
    // CHECK IF PROVIDED PRODUCT EXISTS
    try {
        //ask server for data
        const response = await fetch(`/check_product?model=${encodeURIComponent(model)}&brand=${encodeURIComponent(brand)}`)
        const product = await response.json();
        const container = document.getElementById('card-container');
        // HANDLE ADD FORM
        if (formType === "Add") {
            if (product.doesExist !== "No") {
                errorMessage.innerHTML = "Record already exists!";
                const card = document.createElement('div');
                card.className = 'card';
                card.innerHTML = `
                <table>
                <tr>
                <td id="highlight">Type: </td>
                <td>${product.type}</td>
                </tr>
                <tr>
                <td id="highlight">Brand: </td>
                <td>${product.brand}</td>
                </tr>
                <tr>
                <td id="highlight">Model: </td>
                <td>${product.model}</td>
                </tr>
                <tr>
                <td id="highlight">Price: </td>
                <td>${product.price}</td>
                </tr>
                <tr>
                <td id="highlight">Rating: </td>
                <td>${product.score}</td>
                </tr>
                </table>
                `;
                container.appendChild(card);
                return false;
            } else {
                event.target.submit();
            }
        // HANDLE DELETE FORM
        } else if (formType === "Delete") {
            if (product.doesExist === "No") {
                errorMessage.innerHTML = "Record doesn't exist!";
                return false;
            } else {
                event.target.submit();
            }
        } 
    } catch (error) {
        console.error("NUH UH", error);
        return false;
        }
}