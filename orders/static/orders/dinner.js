document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    document.getElementById('size-selections').style.display = 'none'; 
    document.getElementById('sizes').style.display = 'none'; 
    document.getElementById('size').style.display = 'none'; 
    document.querySelector('#addtocart').disabled = true;

});

// Set page up to add selections for the size, once item is selected.
function GetSaladValue (saladType) {
    // ensure value is selected
    const dinner_type = saladType.value;
    var selectedText = saladType.options[saladType.selectedIndex].innerHTML;
    pastaType.selectedIndex = 0;
    if (selectedText.includes("Small"))
        var size = "Small";
    else
        var size = "Large";

    if (dinner_type)
        load_page(size);

    return false;
}

// Set page up to add selections for the size, once item is selected.
function GetPastaValue (pastaType) {
    // ensure value is selected
    const dinner_type = pastaType.value;
    var selectedText = pastaType.options[pastaType.selectedIndex].innerHTML;
    saladType.selectedIndex = 0;
    if (selectedText.includes("Small"))
        var size = "Small";
    else
        var size = "Large";

    if (dinner_type)
        load_page(size);

    return false;
}

// Renders contents of new page in main view.
function load_page (size) {

    document.querySelector('#addtocart').disabled = false;

    // set size option with selection, but keep hidden
    var size_selection = document.getElementById('size');
    if (size_selection.options[0].innerHTML == size)
        size_selection.selectedIndex = 0;
    else
        size_selection.selectedIndex = 1; 

}
