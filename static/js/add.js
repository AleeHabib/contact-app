const form = document.getElementById("add-form")

form.addEventListener("submit", function (event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const number = document.getElementById("number").value;

    fetch("api/contacts", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            number
        })
    })

        .then(res => res.json())
        .then(data => {
            alert(data.message);
            form.reset();
        })

})