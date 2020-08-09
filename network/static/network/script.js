document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.like-link').forEach(link => {
        link.onclick = () => {
            let id = link.dataset.id
            let likeE = document.querySelector('#num-likes-' + id)
            fetch("/like", {
                method: "POST",
                body: JSON.stringify({
                    id
                })
            })
            .then(response => response.json())
            .then(json => likeE.innerHTML = json['likes'])
        }
    })
})