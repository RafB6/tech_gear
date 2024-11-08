//initialize gearData variable
let gearData;
//FETCH FULL DATA SET
fetch("/get_gear")
.then(response => response.json())
.then(data => {
    gearData = data;
})
.catch(error => console.error("error fetching data", error));
//FUNCTION 'UpdateGearData' UPDATES DATA BY SORTING AND FILTERING
//ACCORDING TO USER's INPUT
updateGearData = (event) => 
{
    subData = gearData
    //check for type error
    if (typeof(event) !== "string") {
        throw new TypeError("Expected event to be a string.");
    }
    
    // check if filtering is needed
    if (event === "query"){
        if (query !== "") {
            const query = document.getElementById('query').value;
            const sort_by = document.getElementById('sort-select').value;
            const reverse = document.getElementById('reverse-order').value;
            if (typeof(sort_by) !== "string" || typeof(reverse) !== "string") {
                throw new TypeError("Wrong data type for sort_by / reverse");
            }
            subData = reverseData(sortData(filterData(subData, query), sort_by), reverse);
        }
    }
    // if not, just sort
    else {
        const sort_by = document.getElementById('sort-select').value;
        const reverse = document.getElementById('reverse-order').value;            
        if (typeof(sort_by) !== "string" || typeof(reverse) !== "string") {
            throw new TypeError("Wrong data type for sort_by / reverse");
        }
        subData = reverseData(sortData(subData, sort_by), reverse);
    }
    
    const cardContainer = document.querySelector(".card-container");
    cardContainer.innerHTML = "";
    subData.forEach(element => {
        const card = document.createElement('div');
        card.className = "card";
        card.innerHTML = `
        <table>
            <tr>
                <td id="highlight">Type: </td>
            <td> ${element.type} </td>
            </tr>
            <tr>
                <td id="highlight">Model: </td>
                <td> ${element.model}</td>
            </tr>
            <tr>
                <td id="highlight">Price: </td>
                <td> ${element.price}</td>
            </tr>
            <tr>
                <td id="highlight">Rating: </td>
                <td> ${element.rating}</td>
            </tr>
            <tr>
                <td id="highlight">Brand: </td>
                <td> ${element.brand} </td>
    </table>
        `;
        cardContainer.appendChild(card);
    });
}
//FILTER DATA
filterData = (sub, subquery) => {
    if (typeof(subquery) !== "string"){
        throw new TypeError("Expected a string for subquery");
    }
    
    const regex = new RegExp(subquery, "i");
    filteredSubData = sub.filter(item =>
        regex.test(item.model) || regex.test(item.brand)
    );
    return filteredSubData;
}
sortData = (sub, category) => {
    if (typeof(category) !== "string"){
        throw new TypeError("Expected string for category");
    }
    sub.sort((a,b) => {
        const aVal = a[category];
        const bVal = b[category];
        
        if (category === "type"){
            const aType = aVal || "";
            const bType = bVal || "";
            return aType.localeCompare(bType);
        } else {
            const aInt = typeof aVal === "number" ? aVal : 0;
            const bInt = typeof bVal === "number" ? bVal : 0;
            return aInt - bInt; 
        }
    });
    return sub;
}
reverseData = (sub, mess) => {
    if (typeof(mess) !== "string") {
        throw new TypeError("Expected string for reverse message");
    }
    if (mess === "normal"){
        return sub;
    } else {
        return sub.reverse();
    }
}
    //TODO:
    /*
    QUERY OPTIMALIZATION
    LOGGING SYSTEM -> SQLite
    Restrict access based on authentication
    */
//LOOK FOR CHANGES
document.getElementById('query').addEventListener('input', () => updateGearData("query"))
document.getElementById('sort-select').addEventListener('change', () => updateGearData("sort"));
document.getElementById('reverse-order').addEventListener('change', () => updateGearData("reverse"));