document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    document.getElementById('topping-selections').style.display = 'none'; 
    document.getElementById('topping-title').style.display = 'none'; 
    document.getElementById('1').style.display = 'none'; 
    document.getElementById('topping1').style.display = 'none';
    document.getElementById('size-selections').style.display = 'none';
    document.getElementById('extra-selections').style.display = 'none'; 
    document.getElementById('sizes').style.display = 'none'; 
    document.getElementById('size').style.display = 'none'; 
    document.getElementById('count').style.display = 'none'; 
    document.getElementById('extraCheese').style.display = 'none'; 
    document.getElementById('extraMushroom').style.display = 'none'; 
    document.getElementById('extraPepper').style.display = 'none'; 
    document.getElementById('extraOnion').style.display = 'none'; 
    document.querySelector('#addtocart').disabled = true;

});

// Set page up to add selections for the correct number of toppings, once selected.
function GetSelectedValue (subType) {
    // ensure value is selected
    const sub_type = subType.value;
    var selectedText = subType.options[subType.selectedIndex].innerHTML;
    
    if (selectedText.includes("Small"))
        var size = "Small";
    else
        var size = "Large";

    if (sub_type)
        load_page(sub_type, size);

    return false;
}

function removeMessages () {
    // clear out any existing topping dropdowns on screen except for first hidden
    var ul = document.getElementById('topping-selections');
    var count = 0;
    var index = 2;

    if (ul)
        count = ul.childElementCount;

    for (var i = index; i < count; i++) {
            ul.removeChild(ul.children[index]);
    }

    // remove toppings with price from list
    var topping1 = document.getElementById('topping1');
    var total_toppings = document.getElementById('count').value;
    count = topping1.childElementCount;
    index = total_toppings+1;

    for (var i = index; i < count; i++) {
        topping1.removeChild(topping1.children[index]);
    }
    document.getElementById('extraCheese').style.display = 'none'; 
    document.getElementById('extraMushroom').style.display = 'none'; 
    document.getElementById('extraPepper').style.display = 'none'; 
    document.getElementById('extraOnion').style.display = 'none'; 
    document.getElementById('extra-selections').style.display = 'none'; 
}

// Renders contents of new page in main view.
function load_page (sub_type, size) {

    document.querySelector('#addtocart').disabled = false;
    removeMessages();

    // set size option with selection, but keep hidden
    var size_selection = document.getElementById('size');
    if (size_selection.options[0].innerHTML == size)
        size_selection.selectedIndex = 0;
    else
        size_selection.selectedIndex = 1; 

    var total_toppings = document.getElementById('count').value;
    
    // display all toppings avail and allow user to select all
    document.getElementById('topping-selections').style.display = 'block'; 
    document.getElementById('topping-title').style.display = 'block'; 
    document.getElementById('1').style.display = 'block'; 
    document.getElementById('topping1').style.display = 'inline-block'; 

    // set toppings based on pizza order selections
    var ul = document.getElementById('topping-selections');
    var topping1 = document.getElementById('topping1');

    // create selection for each additional sub toppings
    for (var i = 1; i < total_toppings; i++) { 

        var new_dropdown = topping1.cloneNode(true);
        new_dropdown.name = "topping" + (i+1);
        new_dropdown.id = "topping" + (i+1);

        var li = document.createElement("li");
        li.id = (i+1);
        li.appendChild(new_dropdown);
        ul.appendChild(li);
        ul.style.display = 'inline-block'; 
    }


    var el_id = sub_type + "Xcheese";
    var elmt = document.getElementById(el_id);
    if (elmt) {
        var desc = elmt.value;
        var el_id = "Extra Cheese";
        create_dropdown(el_id, desc, 7);
    }

    var el_id = sub_type + "Mushrooms";
    var elmt = document.getElementById(el_id);
    if (elmt) {
        var desc = elmt.value;
        var el_id = "Mushrooms";
        create_dropdown(el_id, desc, 8);
    }

    var el_id = sub_type + "Peppers";
    var elmt = document.getElementById(el_id);
    if (elmt) {
        var desc = elmt.value;
        var el_id = "Green Peppers";
        create_dropdown(el_id, desc, 9);
    }

    var el_id = sub_type + "Onions";
    var elmt = document.getElementById(el_id);
    if (elmt) {
        var desc = elmt.value;
        var el_id = "Onions";
        create_dropdown(el_id, desc, 10);
    }
}

function create_dropdown (el_id, desc, count) {
    var ul = document.getElementById('topping-selections');
    var new_dropdown = document.createElement("select");
    new_dropdown.name = "topping" + count;
    new_dropdown.id = "topping" + count;

    var option1 = document.createElement("option");
    option1.value = "Please Select";
    option1.text = "Please Select";
    new_dropdown.add(option1);
    var option2 = document.createElement("option");
    option2.value = el_id;
    option2.text = desc;
    new_dropdown.add(option2);

    var li = document.createElement("li");
    li.id = count;
    li.appendChild(new_dropdown);
    ul.appendChild(li);
}