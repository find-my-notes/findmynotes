function searchQuery(search_query_value) {
    let search_query = document.getElementById(search_query_value).value;
    let token = document.getElementById("csrftoken").value

    if(search_query != '') {
        try {
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if(this.readyState == 4 && this.status == 200){
                        console.log("searched",search_query_value)
                }             
            }
            file_url = '/search_store?searched_query='+search_query
            xhttp.open('POST',file_url,true);
            xhttp.setRequestHeader("X-CSRFToken",token)
            xhttp.send();
        } 
        catch (err) {
            alert("Error: " + err)
        }
        window.open("/searchPage/1/"+search_query, "_self")
    }
}
function triggerEnter(search_query_value){
    if (event.keyCode == 13) {
        searchQuery(search_query_value)
    }
}

function toggleDropdownLinks(){
    var Dropdown_links = document.getElementById("dropdown_links")
    var angle_down_arrow = document.getElementById("Dropdown_angle_down");
    angle_down_arrow.classList.toggle('Dropdown_angle_rotate')
    Dropdown_links.classList.toggle('height-0')
}