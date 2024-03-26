// JS to search through archive page and retrieve specific one

function search_archive() {
    let searchDate = document.getElementById("searchInput").value.trim();
    let archives = document.querySelector('.archives');

    for (let i = 0; i < archives.children.length; i++) {
        if (archives.children[i].textContent.includes(searchDate)) {
            archives.children[i].style.display = "block";
        }
        else {
            archives.children[i].style.display = "none"; 
        }
    }
}

function handleKeyPress(event) {
    if (event.keyCode == 13) {
        search_archive();
    }
}