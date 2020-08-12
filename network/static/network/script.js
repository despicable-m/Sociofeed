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
            .then(json => color(json['likes'], likeE, id))

        }
    })

    function color (value, likeE, id) {
        console.log(value - likeE.innerHTML)
        if ((value - likeE.innerHTML) < 0) {
            document.querySelector('#b-' + id).setAttribute("fill", "grey")
            likeE.innerHTML = value
        } else {
            document.querySelector('#b-' + id).setAttribute("fill", "red")
            likeE.innerHTML = value
        }
    }
})