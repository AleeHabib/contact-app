const form = document.getElementById("delete-form")

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value;

    fetch("api/contacts", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name
        })
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message)
        })

})