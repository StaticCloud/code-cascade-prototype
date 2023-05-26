const addArticle = async (e) => {
    e.preventDefault();

    const title = document.querySelector('#title-input').value.trim();
    const category = document.querySelector('#category-input').value.trim();
    const image_preview = document.querySelector('#image-input').value.trim();
    const article_path = document.querySelector('#article-input').value.trim();
    const description = document.querySelector('#description-input').value.trim();

    console.log(description);

    const response = await fetch('/api/article/', {
        method: 'POST',
        body: JSON.stringify({
            title: title,
            category: category,
            image_preview: image_preview,
            article_path: article_path,
            description: description
        }),
        headers: { 'Content-Type': 'application/json' }
    })

    if (response.ok) {
        document.location.replace('/')
    } else {
        alert(response.statusText);
    }
}

document.querySelector('#add-article').addEventListener('click', addArticle);