function browse_file_bttn(){
    document.getElementById("file_to_upload").click();
}
function get_file_data(){
    var fileName = document.getElementById("file_to_upload").value;
    extension = fileName.substring(fileName.lastIndexOf('.') + 1);
    let FileType;
    if(extension == "pdf"){
        FileType = "pdf";
        filename = fileName.substring(fileName.lastIndexOf('\\')+1)
        document.getElementById("file_name").innerHTML = filename;
        document.querySelector('#file_type').value = FileType;
        enableUploadBttn()
    }
    else{
        alert("Only PDF file is permitted")
        document.querySelector("#upload_bbtn").disabled = true 
    }
}
function validateTAndC(tandc_checkbox){
    checkbox = tandc_checkbox.checked
    if(checkbox == true){
        enableUploadBttn()
    }
    else{
        document.getElementById("upload_bbtn").disabled = true;
        enableUploadBttn()
    }
}
function enableUploadBttn(){
    file_type = document.querySelector('#file_type').value;
    t_and_c_checkbox = document.querySelector('#tandc_checkbox');
    if(t_and_c_checkbox.checked==true && file_type == "pdf"){
        document.getElementById("upload_bbtn").disabled = false;
    }
    else{
        document.getElementById("upload_bbtn").disabled = true;
    }
}
function uploadAnimation(){
    document.getElementById("upload_bbtn").textContent= "Uploading.."
}