function showReportPopup(file_id,user_reported_issue,user_posted){
    document.getElementById("report_form_overlay").style.display="flex";
    document.getElementById("reporting_file_id").value = file_id;
    document.getElementById("user_reported_issue").value = user_reported_issue;
    document.getElementById("user_posted").value = user_posted;
    document.body.style.overflow = "hidden";
}

function closeReportPopup(){
    document.getElementById("report_form_overlay").style.display="none"
    document.body.style.overflow = "";

    document.getElementById("reason_to_report").value = "" ;

}
function showDescription(that){
    var description = that.querySelector("#file_description")
    description.classList.remove("truncate-line-1")
}
function hideDescription(that){
    var description = that.querySelector("#file_description")
    description.classList.add("truncate-line-1")
}