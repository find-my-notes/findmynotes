function browse_file_bttn(){
    document.getElementById("file_to_upload").click();
}
function get_file_data(){
    var fileName = document.getElementById("file_to_upload").value;
    // document.getElementById("file_name").innerHTML = fileName;
    extension = fileName.substring(fileName.lastIndexOf('.') + 1);
    let FileType;
    if(extension == "pdf"){
        FileType = "pdf"
    }
    else{
        alert("Only PDF file is permitted")
        document.querySelector("#upload_bbtn").disabled = true 
    }
    document.querySelector('#file_type').value = FileType;
}
function validateTAndC(tandc_checkbox){
    checkbox = tandc_checkbox.checked
    if(checkbox == true){
        document.getElementById("upload_bbtn").disabled = false
    }
    else{
        document.getElementById("upload_bbtn").disabled = true
    }
}