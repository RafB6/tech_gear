// STORING FETCHED DATA
let full_data = []
getData()

async function getData() {
    const response = await fetch("/get_gear");
    const full_gear_data = await response.json();
    full_data = full_gear_data;
    display_data(full_data)
}
// DISPLAYING INITIAL DATA
window.addEventListener('load', getData);


//UPDATE DATA DYNAMICALLY
function update_gear_data(){
    const key = document.getElementById('sort-select').value;
    const reverse = document.getElementById('reverse-order').value;
    const query = document.getElementById('query').value;

    const sorted_data = sort_data(query, key, reverse);
    //CHECK FOR EXISTING DATA, DISPLAY IT ACCORDINGLY
    if (sorted_data) display_data(sorted_data);
    else {
        document.getElementById("error_message").innerHTML = "No products found";
    }
}

function rate(event, form){ 
    event.preventDefault();
    const formData = new FormData(form);
    fetch(`/add_rating`, {
        method: "POST",
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.issuccess) {
            alert("Thanks for your feedback");
        } else {
            alert("Failed to submit rating");
        }
    })
}


// Update on-select
document.getElementById('sort-select').addEventListener('change', update_gear_data);
document.getElementById('reverse-order').addEventListener('change', update_gear_data);
document.getElementById('query').addEventListener('input', update_gear_data);

function doesInclude(element, query) {
    const q = query.toLowerCase();
    return ((element.model.toLowerCase().includes(q)) || (element.type.toLowerCase().includes(q)));
}
// (sorting in JavaScript is the goofiest thing I've ever seen)
function sort_data(query, key, reverse) {
    let sorted_data = full_data.filter((element) => doesInclude(element, query));

    switch(key) {
        case "id":
            sorted_data.sort((a,b) => a.id - b.id);
            break;
        case "type":
            sorted_data.sort((a,b) => {
                const aType = a.type.toUpperCase();
                const bType = b.type.toUpperCase();
                if (aType < bType) return -1;
                if (aType > bType) return 1;
                return 0;
            })
            break;
        case "price":
            sorted_data.sort((a,b) => parseFloat(a.price) - parseFloat(b.price));
            break;
        case "rating":
            sorted_data.sort((a,b) => parseFloat(a.score) - parseFloat(b.score));
            break;
        default:
            break;
        };
        // REVERSING
    return (reverse === "reverse") ? sorted_data.reverse() : sorted_data;
}

function display_data(full_data) {
    const card_container = document.querySelector(".card-container");
    card_container.innerHTML = '';
    full_data.forEach(item => {
        const card = document.createElement('div');
        card.className = 'card';
        card.style = 'width: 200px;';
        card.innerHTML = `
        <table>
            <tr>
                <td id="highlight">Type: </td>
                <td>${item.type}</td>
            </tr>
            <tr>
                <td id="highlight">Brand: </td>
                <td>${item.brand}</td>
            </tr>
            <tr>
                <td id="highlight">Model: </td>
                <td>${item.model}</td>
            </tr>
            <tr>
                <td id="highlight">Price: </td>
                <td>${item.price}</td>
            </tr>
            <tr>
                <td id="highlight">Rating: </td>
                <td>${item.score}</td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class='rating-form'>
                    <form id='myForm' method='POST' action='/add_rating'; onsubmit='return rate(event, this)'>
                        <p>WHAT DO YOU THINK ABOUT THE PRODUCT? LET US KNOW!</p>
                        Overall: <select class='rating' name='rating' required>
                            <option value='5'>GREAT</option>
                            <option value='4'>DECENT</option>
                            <option value='3'>MID</option>
                            <option value='2'>POOR</option>
                            <option value='1'>HORRIBLE</option>
                        </select>
                        <input class='id' name='id' type='hidden' value="${item.id}">
                        <input type='text' class='comment' name='comment' placeholder='Share your experience'>
                        <input type='submit' value='Rate'>
                    </form>
                    </div>
                </td>
            </tr>
        </table>
        `;
        card_container.appendChild(card);
    })
}