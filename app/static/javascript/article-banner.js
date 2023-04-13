// obtain ID from URL
const id = window.location.toString().split('/')[
    window.location.toString().split('/').length - 1
][0];

const addLike = async () => {
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
    const response = await fetch('/api/article/removeLike', {
        method: 'DELETE',
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

const saveArticle = async () => {
    const response = await fetch('/api/article/save', {
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

const unsaveArticle = async () => {
    const response = await fetch('/api/article/unsave', {
        method: 'DELETE',
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

if (document.querySelector('.add-like')) {
    document.querySelector('.add-like').addEventListener('click', addLike)
}

if (document.querySelector('.remove-like')) {
    document.querySelector('.remove-like').addEventListener('click', removeLike)
}

if (document.querySelector('.save-article')) {
    document.querySelector('.save-article').addEventListener('click', saveArticle)
}

if (document.querySelector('.unsave-article')) {
    document.querySelector('.unsave-article').addEventListener('click', unsaveArticle)
}
