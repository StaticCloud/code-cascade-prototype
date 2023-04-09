const addLike = async () => {

    // obtain the id from the URL
    const id = window.location.toString().split('/')[
        window.location.toString().split('/').length - 1
    ][0];

    const response = await fetch('/api/article/like', {
        method: 'POST',
        body: JSON.stringify({
            article_id: id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })

    if (response.ok) {
        document.location.reload();
    } else {
        alert(response.statusText);
    }
}

const removeLike = async () => {

}

if (document.querySelector('.add-like')) {
    document.querySelector('.add-like').addEventListener('click', addLike)
}

if (document.querySelector('.remove-like')) {
    document.querySelector('.remove-like').addEventListener('click', removeLike)
}
