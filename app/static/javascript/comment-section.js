document.querySelector('.comment-content').addEventListener('click', async (e) => {
    e.preventDefault();

    if (e.target.id == "open-form") {
        e.target.classList.add("none")
        e.target.parentElement.parentElement.querySelector('.comment-form').classList.remove("none")
    }

    if (e.target.id == "cancel-button") {
        e.target.parentElement.parentElement.parentElement.querySelector('#open-form').classList.remove("none")
        e.target.parentElement.parentElement.classList.add("none");
    }

    if (e.target.id == "submit-button") {
        const comment_text = e.target.parentElement.querySelector('textarea[name="comment"]').value.trim();
        const parent_comment = e.target.closest('[data-id]').getAttribute('data-id');
    
        const response = await fetch('/api/reply', {
            method: 'POST',
            body: JSON.stringify({
                comment_text,
                parent_comment
            }),
            headers: { 'Content-Type': 'application/json' }
        })

        if (response.ok) {
            document.location.reload()
        } else {
            alert(response.statusText);
        }

    }
})

window.addEventListener('load', () => {
    let textarea = document.querySelector('textarea[name="comment-text"]');
    let replyTextarea = document.querySelectorAll('textarea[name="comment"]')
    replyTextarea.forEach(text => text.value = '')
    textarea.value = '';
})