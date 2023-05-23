const deleteArticle = async (e) => {
    e.preventDefault();

    const id = window.location.toString().split('/')[
        window.location.toString().split('/').length - 1
    ][0];

    const response = await fetch(`/api/article/${id}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
        document.location.replace('/')
    } else {
        alert(response.statusText);
    }
}

const editArticle = async (e) => {
    e.preventDefault();

    const id = window.location.toString().split('/')[
        window.location.toString().split('/').length - 1
    ][0];

    const title = document.querySelector('#title-input').value.trim();
    const category = document.querySelector('#category-input').value.trim();
    const image_preview = document.querySelector('#image-input').value.trim();
    const article_path = document.querySelector('#article-input').value.trim();

    const response = await fetch(`/api/article/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            title: title,
            category: category,
            image_preview: image_preview,
            article_path: article_path
        }),
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
        document.location.replace(`/article/${id}`)
    } else {
        alert(response.statusText);
    }
}

document.querySelector('#edit-article').addEventListener('click', editArticle);
document.querySelector('#delete-article').addEventListener('click', deleteArticle);