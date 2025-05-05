from flask import Flask, render_template

app = Flask(__name__)

contacts = [
    {"name": "Ali Habib", "no": "03313568393"},
    {"name": "Maryam Hayat", "no": "03415947090"},
    {"name": "Habib Hussain", "no": "03212727914"},
]

# contacts = []


@app.route("/")
@app.route("/home")  # base route
def home():
    return render_template("home.html")


@app.route("/add")  # adds a new contact
def add_contact():
    return render_template("add.html")


@app.route("/read")  # display all contacts
def read_contacts():
    return render_template("read.html", contacts=contacts)


@app.route("/update")  # updates an existing contact
def update_contact():
    return render_template("update.html")


@app.route("/delete")  # deletes an existing contact
def delete_contact():
    return render_template("delete.html")


if __name__ == "__main__":
    app.run(debug=True, port=5500)
