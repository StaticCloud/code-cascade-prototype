const bioButton = document.querySelector(".bio")
const savesButton = document.querySelector(".saves")
const likesButton = document.querySelector(".likes")
const commentsButton = document.querySelector(".comments")

const profileNav = document.querySelector('.profile-nav')

profileNav.addEventListener("click", (e) => {
    let element = e.target;

    if (element.nodeName == "IMG") {
        element = element.parentNode
    }

    Array.from(profileNav.children).forEach(child => {
        child.classList.remove('highlighted')
    })

    element.classList.add('highlighted')

    Array.from(document.querySelector(".profile-body").children).forEach(child => {
        child.classList.add('none')
    })

    document.querySelector(`[data-content=${element.classList[0]}]`).classList.remove('none')
})