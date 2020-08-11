document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#edit-form').addEventListener('submit', (event) => {
        event.preventDefault();
        let composeArea = document.querySelector('#compose-area');
        let id = composeArea.dataset.id
        let post = document.querySelector('#the-post')
        fetch("/edit/"+id, {
            method: "POST",
            body: JSON.stringify({
                id: id,
                post: composeArea.value
            })
        })
        .then(response => response.json())
        .then(json => post.innerHTML = json['edited_post'])
    })
})