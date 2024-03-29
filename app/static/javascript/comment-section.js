document.querySelector('.comment-content').addEventListener('click', async (e) => {
    e.preventDefault();

    // anchor tags by default to not function properly, this is here to fix that
    if (e.target.href) {
        document.location = e.target.href;
    }

    if (e.target.id == "open-form") {
        e.target.classList.add("none")
        e.target.parentElement.parentElement.querySelector('.comment-form').classList.remove("none")
    }

    if (e.target.id == "open-edit-form") {
        e.target.classList.add("none")
        e.target.parentElement.querySelector('p').classList.add("none")
        e.target.parentElement.querySelector('#delete-comment').classList.add("none")
        e.target.parentElement.parentElement.querySelector('.edit-form').classList.remove("none")
    }

    if (e.target.id == "delete-comment") {
        const comment_id = e.target.closest('[data-id]').getAttribute('data-id');

        const response = await fetch(`/api/comment/${comment_id}`, {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' }
        })

        if (response.ok) {
            document.location.reload()
        } else {
            alert(response.statusText);
        }
    }

    if (e.target.id == "update-button") {
        const comment_id = e.target.closest('[data-id]').getAttribute('data-id');
        const comment_text = e.target.parentElement.querySelector('textarea[name="edit-comment"]').value.trim();

        const response = await fetch(`/api/comment/${comment_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                comment_text
            }),
            headers: { 'Content-Type': 'application/json' }
        })

        if (response.ok) {
            document.location.reload()
        } else {
            alert(response.statusText);
        }
    }

    if (e.target.id == "cancel-button") {
        e.target.parentElement.parentElement.parentElement.querySelector('#open-form').classList.remove("none")
        e.target.parentElement.parentElement.classList.add("none");
    }

    if (e.target.id == "cancel-edit-button") {
        e.target.parentElement.parentElement.parentElement.querySelector('p').classList.remove("none")
        e.target.parentElement.parentElement.parentElement.querySelector('#open-edit-form').classList.remove("none")
        e.target.parentElement.parentElement.parentElement.querySelector('#delete-comment').classList.remove("none")
        e.target.parentElement.parentElement.classList.add("none");
    }

    if (e.target.id == "submit-button") {
        const comment_text = e.target.parentElement.querySelector('textarea[name="comment"]').value.trim();
        const parent_comment = e.target.closest('[data-id]').getAttribute('data-id');
        const article_id = window.location.toString().split('/')[
            window.location.toString().split('/').length - 1
        ][0];

        const response = await fetch('/api/reply', {
            method: 'POST',
            body: JSON.stringify({
                comment_text,
                parent_comment,
                article_id
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
    if (textarea) {
        textarea.value = '';
    }
})