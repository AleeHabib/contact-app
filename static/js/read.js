fetch("/api/contacts")
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("contacts-body");

        if (data.length === 0) {
            list.innerHTML = `
                <tr>
                    <td colspan="3" class="text-center">
                        There are no contacts
                    </td>
                </tr>
            `;
            return;
        }
        list.innerHTML += `<thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Number</th>
                </tr>
            </thead>`;
        data.forEach((contact, index) => {
            list.innerHTML += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${contact.name}</td>
                    <td>${contact.number}</td>
                </tr>
            `;
        });
    });

console.log("Read API executed")
