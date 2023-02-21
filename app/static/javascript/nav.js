const navigation = document.querySelector('#nav-wrapper')

document.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
        navigation.classList.add('nav-scroll')
    } else {
        navigation.classList.remove('nav-scroll')
    }
})