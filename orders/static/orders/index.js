document.addEventListener('DOMContentLoaded', () => {

    const user_name = document.getElementById('user-name');

    if (user_name)
        document.getElementById('loginTab').style.backgroundColor = "lightgrey";
    else 
        document.getElementById('logoutTab').style.backgroundColor = "lightgrey";

    // Start by setting top of page.
    load_page('top');

    // Set links up to scroll to parts of the current page.
    document.querySelectorAll('.nav-link').forEach(link => {
        link.onclick = () => {
            const page = link.dataset.page;
            load_page(page);
            return false;
        };
    });
});

// Update text on popping state.
window.onpopstate = e => {
    const data = e.state;
    if (data.text && (data.text != "/")) {
        var elmnt = document.getElementById(data.text);
        elmnt.scrollIntoView({behavior: "smooth"});
    }
    else 
     window.scrollTo(0,0);
};

// Renders contents of new page in main view.
function load_page(name) {
    var elmnt = document.getElementById(name);
    elmnt.scrollIntoView({behavior: "smooth"});

    if (name == "top") 
        name = "/";

    var title = document.title;
    history.pushState({'title': title, 'text': name}, name, name);
}

// Set menu tab highlight to indicated page.
function format_selected_tab(e_th, e_link) {
    e_th.style.textDecoration = "none";
    e_link.style.color = "white";
    e_th.style.backgroundColor = "darkblue";
    e_th.style.borderBottomColor = "darkblue";
}

// Set previously selected menu tab back to defaults.
function format_old_tab(e_th, e_link) {
    e_th.style.textDecoration = "none";
    e_link.style.color = "darkblue";
    e_th.style.backgroundColor = "white";
    e_th.style.borderBottomColor = "black";
}