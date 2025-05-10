from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

app.secret_key = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

contacts = []


@app.route("/")
@app.route("/home")  # base route
def home():
    return render_template("home.html")


@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        contacts.append({"name": name, "no": number})
        flash("Contact added successfully", "success")
        return redirect(
            url_for("read_contacts")
        )  # user will be redirected to the contacts page
    return render_template("add.html")


@app.route("/read")  # display all contacts
def read_contacts():
    return render_template("read.html", contacts=contacts)


@app.route("/update")  # updates an existing contact
def update_contact():
    return render_template("update.html")


@app.route("/delete", methods=["GET", "POST"])  # deletes an existing contact
def delete_contact():
    if request.method == "POST":
        name = request.form["name"]
        for contact in contacts:
            if name == contact["name"]:
                contacts.remove(contact)
                flash("Contact deleted successfully", "success")
                return redirect(url_for("read_contacts"))
        flash("Contact does not exist", "error")
        return redirect(url_for("delete_contact"))
    return render_template("delete.html")


if __name__ == "__main__":
    app.run(debug=True, port=5500)
