//UPDATE DATA DYNAMICALLY
function update_gear_data(){
    const query = document.getElementById('query').value;
    const sort_by = document.getElementById('sort-select').value;
    const reverse = document.getElementById('reverse-order').value;
    const regex = new RegExp(query, "i"); 
    //FETCH, INCLUDE BOTH USER-PROVIDED VALUES
    fetch(`/get_gear?query=${encodeURIComponent(query)}&sort_by=${sort_by}&reverse=${reverse}`)
    //PARSE FROM JSON TO JS-OBJECT
    .then(response => response.json())
    //PARSED DATA
    .then(data => {
        const card_container = document.querySelector(".card-container");
        card_container.innerHTML = '';
        const filtered_data = data.filter(item =>
            regex.test(item.model) || regex.test(item.brand)
        );
        //CREATE CARD TO EVERY ELEMENT IN OBJECT
        filtered_data.forEach(item => {
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
                    <td>[ soon ]</td>
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
    })
    .catch(error => console.error('Error fetching sorted gear:', error));
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
//LOOK FOR CHANGES
document.getElementById('query').addEventListener('input', update_gear_data)
document.getElementById('sort-select').addEventListener('change', update_gear_data);
document.getElementById('reverse-order').addEventListener('change', update_gear_data);