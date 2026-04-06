from flask import Flask, session, render_template, request, redirect, url_for, flash
from models import db, User, Contact
import bcrypt

app = Flask(__name__)

from configs import Config

app.config.from_object(Config)

db.init_app(app)

contacts = []

with app.app_context():
    db.create_all()


@app.route("/home")  # base route
def home():
    if "user_id" not in session:
        return render_template("login.html")
    return render_template("home.html", username=session.get("user_name"))


@app.route("/add", methods=["GET", "POST"])
def add_contact():
    if "user_id" not in session:
        return render_template("login.html")
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        if not number.isdigit() or len(number) != 11:
            flash(
                "Invalid number: must be 11 digits only",
                "error",
            )
            return redirect(url_for("add_contact"))
        contact = Contact(name=name, number=number, user_id=session.get("user_id"))
        db.session.add(contact)
        db.session.commit()
        # contacts.append(
        #     {"user_id": session.get("user_id"), "name": name, "number": number}
        # )
        flash("Contact added successfully", "success")
        return redirect(
            url_for("read_contacts")
        )  # user will be redirected to the contacts page
    return render_template("add.html", username=session.get("user_name"))


@app.route("/read")  # display all contacts
def read_contacts():
    if "user_id" not in session:
        return render_template("login.html")
    user_id = session.get("user_id")
    contacts = Contact.query.filter_by(user_id=user_id)
    # filtered = [contact for contact in contacts if contact["user_id"] == user_id]
    return render_template("read.html", contacts=contacts)


@app.route("/update", methods=["GET", "POST"])
def update_contact():
    if "user_id" not in session:
        return render_template("login.html")
    if request.method == "POST":
        name = request.form["name"]
        number = request.form["number"]
        if not number.isdigit() or len(number) != 11:
            flash(
                "Invalid number: must be 11 digits only",
                "error",
            )
            return redirect(url_for("update_contact"))
        user_id = session.get("user_id")
        contacts = Contact.query.filter_by(user_id=user_id)
        for contact in contacts:
            if name == contact.name:
                contact.number = number
                db.session.commit()
                flash("Contact successfully updated", "success")
                return redirect(url_for("read_contacts"))

        flash("Contact not found", "error")
        return redirect(url_for("update_contact"))

    # This handles GET requests safely
    return render_template("update.html")


@app.route("/delete", methods=["GET", "POST"])  # deletes an existing contact
def delete_contact():
    if "user_id" not in session:
        return render_template("login.html")
    if request.method == "POST":
        name = request.form["name"]
        user_id = session.get("user_id")
        contacts = Contact.query.filter_by(user_id=user_id)
        for contact in contacts:
            if name == contact.name:
                db.session.delete(contact)
                db.session.commit()
                flash("Contact deleted successfully", "success")
                return redirect(url_for("read_contacts"))
        flash("Contact does not exist", "error")
        return redirect(url_for("delete_contact"))

    return render_template("delete.html")


@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def login_account():
    if "user_id" not in session:
        if request.method == "POST":
            email = request.form["Email"]
            password = request.form["Password"]
            user = User.query.filter_by(email=email).first()
            if user:
                if bcrypt.checkpw(password.encode("utf-8"), user.password):
                    session["user_id"] = user.id
                    session["user_name"] = user.name
                    flash(f"Welcome {user.name}", "success")
                    return redirect(url_for("home"))
                else:
                    flash("Invalid username or password", "error")
                    return redirect(url_for("login_account"))
            flash("User does not exist", "error")
            return redirect(url_for("login_account"))
    else:
        return render_template("home.html")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register_account():
    if "user_id" not in session:
        if request.method == "POST":
            password = request.form["Password"]
            c_password = request.form["C_Password"]
            if password == c_password:
                name = request.form["Name"]
                email = (request.form["Email"]).lower()
                hashed_password = bcrypt.hashpw(
                    (request.form["Password"]).encode("utf-8"), bcrypt.gensalt()
                )
                user = User(name=name, email=email, password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash("Account created!", "success")
                return redirect(url_for("login_account"))
            else:
                flash("Passwords do no match", "error")
                return redirect(url_for("register_account"))
    else:
        return render_template("home.html")
    return render_template("register.html")


@app.route("/logout", methods=["GET", "POST"])
def logout_account():
    if "user_id" in session:
        session.clear()
        return render_template("login.html")
    return render_template("login.html")
