document.querySelector('#add-article-comment').addEventListener('click', async (e) => {
    e.preventDefault();

    if (e.target.id == "add-comment") {
        const comment_text = document.querySelector('[name=comment-text]').value.trim()
        const article_id = window.location.toString().split('/')[
            window.location.toString().split('/').length - 1
        ][0];

        if (comment_text) {
            const response = await fetch('/api/comment', {
                method: 'POST',
                body: JSON.stringify({
                    comment_text,
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
    }
})