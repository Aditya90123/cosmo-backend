from flask import Flask, render_template, request, redirect, jsonify
from flask_cors import CORS
from models import db, Contact, Product

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ================= API =================

@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.json
    msg = Contact(
        name=data["name"],
        email=data["email"],
        message=data["message"]
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"status": "saved"})

@app.route("/api/products")
def api_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "description": p.description,
            "pdf": p.pdf
        } for p in products
    ])

# ================= ADMIN =================

@app.route("/admin")
def admin():
    products = Product.query.all()
    messages = Contact.query.all()
    return render_template(
        "admin.html",
        products=products,
        messages=messages
    )

@app.route("/admin/add", methods=["POST"])
def add_product():
    p = Product(
        name=request.form["name"],
        category=request.form["category"],
        pdf=request.form["pdf"],
        description=request.form["description"]
    )
    db.session.add(p)
    db.session.commit()
    return redirect("/admin")

# ================= START =================

if __name__ == "__main__":
    app.run()
