document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    document.getElementById('topping-selections').style.display = 'none'; 
    document.getElementById('topping-title').style.display = 'none'; 
    document.getElementById('1').style.display = 'none'; 
    document.getElementById('topping1').style.display = 'none';
    document.getElementById('size-selections').style.display = 'none'; 
    document.getElementById('sizes').style.display = 'none'; 
    document.getElementById('size').style.display = 'none'; 
    document.querySelector('#addtocart').disabled = true;

});

// Set page up to add selections for the correct number of toppings, once selected.
function GetSelectedValue (numToppings) {
    // ensure value is selected
    const num_toppings = numToppings.value;
    var selectedText = numToppings.options[numToppings.selectedIndex].innerHTML;
    if (selectedText.includes("Small"))
        var size = "Small";
    else
        var size = "Large";

    if (num_toppings)
        load_page(num_toppings, size);

    return false;
}

function removeMessages () {
    // clear out any existing topping dropdowns on screen
    var ul = document.getElementById('topping-selections');
    var count = 0;
    var index = 2;

    if (ul)
        count = ul.childElementCount;

    for (var i = index; i < count; i++) {
            ul.removeChild(ul.children[index]);
    }
}

// Renders contents of new page in main view.
function load_page (num_toppings, size) {

    document.querySelector('#addtocart').disabled = false;
    removeMessages();

    // set size option with selection, but keep hidden
    var size_selection = document.getElementById('size');
    if (size_selection.options[0].innerHTML == size)
        size_selection.selectedIndex = 0;
    else
        size_selection.selectedIndex = 1; 

    var count_toppings = 0;

    // only display toppings if pizza type selection is not cheese
    if (count_toppings < num_toppings) {

        // show topping options for customer to select and submit
        document.getElementById('topping-selections').style.display = 'block'; 
        document.getElementById('topping-title').style.display = 'block'; 
        document.getElementById('1').style.display = 'block'; 
        document.getElementById('topping1').style.display = 'inline-block'; 

        // set toppings based on pizza order selections
        var ul = document.getElementById('topping-selections');
        var topping1 = document.getElementById('topping1');
        var item = [];
        
        // if special, get items included
        if (num_toppings == 4) {
            for (var i = 0; i < topping1.length; i++) {
                if (topping1.options[i].text.includes("*")) {
                    item[count_toppings++] = topping1.options[i].value;
                }
            }
            num_toppings = count_toppings;
        }

        // create selection for each additional topping in pizza type
        for (var i = 1; i < num_toppings; i++) { 

            var new_dropdown = topping1.cloneNode(true);
            new_dropdown.name = "topping" + (i+1);
            new_dropdown.id = "topping" + (i+1);

            var li = document.createElement("li");
            li.id = (i+1);
            li.appendChild(new_dropdown);
            ul.appendChild(li);
            ul.style.display = 'inline-block'; 
        }
    }
    else {
        document.getElementById('topping-selections').style.display = 'none'; 
        document.getElementById('topping-title').style.display = 'none'; 
        document.getElementById('1').style.display = 'none'; 
        document.getElementById('topping1').style.display = 'none';
    }

    // if special, set selection to next included
    if (num_toppings > 3) {
        for (var i = 0; i < item.length; i++){
            var t = 0;
            var found = false;
            while ((t < topping1.length) && (!found)) { 
                if (topping1.options[t].value == item[i]) {
                    var el_id = "topping" + (i+1);
                    var el = document.getElementById(el_id)
                    el.selectedIndex = t;
                    found = true;
                }
                t++;
            }
        }
    }
}
