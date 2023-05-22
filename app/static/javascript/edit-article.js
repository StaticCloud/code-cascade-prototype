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

document.querySelector('#delete-article').addEventListener('click', deleteArticle);