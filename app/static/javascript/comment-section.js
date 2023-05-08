

document.querySelector('.comment-content').addEventListener('click', (e) => {
    e.preventDefault();

    if (e.target.id == "open-form") {
        e.target.classList.add("none")
        e.target.parentElement.querySelector('.comment-form').classList.remove("none")
    }

    if (e.target.id == "cancel-button") {
        e.target.parentElement.parentElement.querySelector('#open-form').classList.remove("none")
        e.target.parentElement.classList.add("none");
    }
})