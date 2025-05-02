let form = document.getElementById("form")

form.addEventListener("submit", evt=> {
    evt.preventDefault()
    let query = document.getElementById('secound').value
    console.log("fuck this"+ query)
    fetch("https://api.tvmaze.com/search/shows?q=" + query)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
})