from flask import (
    Flask,
    session,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
)
from models import db, User, Contact
import bcrypt

app = Flask(__name__)

from configs import Config

app.config.from_object(Config)

db.init_app(app)


with app.app_context():
    db.create_all()


@app.route("/home")  # base route
def home():
    if "user_id" not in session:
        return render_template("login.html")
    return render_template("home.html", username=session.get("user_name"))


@app.route(
    "/api/contacts", methods=["GET", "POST", "DELETE", "PATCH"]
)  # display all contacts
def api_contacts():

    if request.method == "GET":
        user_id = session.get("user_id")
        contacts = Contact.query.filter_by(user_id=user_id).all()
        # filtered = [contact for contact in contacts if contact["user_id"] == user_id]
        return jsonify(
            [{"name": contact.name, "number": contact.number} for contact in contacts]
        )

    if request.method == "POST":
        data = request.get_json()

        name = data.get("name")
        number = data.get("number")

        contact = Contact(name=name, number=number, user_id=session.get("user_id"))
        db.session.add(contact)
        db.session.commit()

        return jsonify({"message": "contact added"}), 201

    if request.method == "DELETE":
        data = request.get_json()

        name = data.get("name")

        contact = Contact.query.filter_by(
            name=name, user_id=session.get("user_id")
        ).first()

        db.session.delete(contact)
        db.session.commit()

        return jsonify({"message": "contact deleted"}), 201

    if request.method == "PATCH":
        data = request.get_json()

        name = data.get("name")
        number = data.get("number")

        contact = Contact.query.filter_by(name=name).first()
        contact.number = number
        db.session.commit()

        return jsonify({"message": "contact updated"}), 201


@app.route("/add")
def add_contact():
    if "user_id" not in session:
        return render_template("login.html")
    return render_template("add.html")


@app.route("/read")
def read_contacts():
    if "user_id" not in session:
        return render_template("login.html")
    return render_template("read.html")


@app.route("/delete")  # deletes an existing contact
def delete_contact():
    if "user_id" not in session:
        return render_template("login.html")

    return render_template("delete.html")


@app.route("/update")
def update_contact():
    if "user_id" not in session:
        return render_template("login.html")

    return render_template("update.html")


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
            email = request.form["Email"].lower()
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Account already exists", "error")
                return redirect(url_for("register_account"))

            password = request.form["Password"]
            c_password = request.form["C_Password"]
            if password == c_password:
                name = request.form["Name"]
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
