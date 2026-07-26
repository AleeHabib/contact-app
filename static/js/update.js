const form = document.getElementById("update-form")

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const number = document.getElementById("number").value;

    fetch("api/contacts", {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            number: number
        })
    })
        .then(res => res.json())
        .then(data => {
            alert(data.message)
        })

})