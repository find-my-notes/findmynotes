const user_mode_switch_container = document.querySelector(".user-mode-switch");
const user_mode_switch_options = user_mode_switch_container.querySelectorAll(".user-actions")

user_mode_switch_options.forEach((option) => {
    option.addEventListener("click", () => {
        user_mode_switch_options.forEach((option) => {
            option.classList.remove('user-actions-active')
        })
        option.classList.add('user-actions-active')
    });
});






const my_scans_button = document.getElementById("myscans_button");
const bookmarks_button = document.getElementById("bookmarks_button");
const more_button = document.getElementById("more_button");
const user_uploads = document.getElementsByClassName("user-uploads")[0];
const user_total_uploads = document.getElementsByClassName("user-total-uploads")[0];
const user_bookmarks_count = document.getElementsByClassName("user-bookmarks")[0];
const user_bio = document.getElementsByClassName("user-bio")[0];

my_scans_button.addEventListener("click", () => {
    user_uploads.classList.add('user-uploads-active');
    user_total_uploads.classList.remove('user-total-uploads-active');
    user_bookmarks_count.classList.remove('user-bookmarks-active');
    user_bio.classList.remove('user-bio-active');
});
bookmarks_button.addEventListener("click", () => {
    user_uploads.classList.remove('user-uploads-active');
    user_total_uploads.classList.remove('user-total-uploads-active');
    user_bookmarks_count.classList.remove('user-bookmarks-active');
    user_bio.classList.remove('user-bio-active');
});
more_button.addEventListener("click", () => {
    user_uploads.classList.remove('user-uploads-active');
    user_total_uploads.classList.add('user-total-uploads-active');
    user_bookmarks_count.classList.add('user-bookmarks-active');
    user_bio.classList.add('user-bio-active');
});



console.log(user_uploads.innerHTML)
