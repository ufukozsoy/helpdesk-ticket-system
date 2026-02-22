from flask import Flask, render_template, request, redirect, url_for, session
from db import db
from models import Ticket

app = Flask(__name__)
app.secret_key = "change-this-in-real-project"
ADMIN_PASSWORD = "powercoders"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///helpdesk.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form["password"]
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin"))
        return render_template("admin_login.html", error="Wrong password")

    return render_template("admin_login.html", error=None)

@app.route("/admin/logout")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("index"))

@app.route("/tickets")
def tickets():
    all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template("tickets.html", tickets=all_tickets)

@app.route("/tickets/new", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        t = Ticket(
            name=request.form["name"],
            email=request.form["email"],
            title=request.form["title"],
            priority=request.form["priority"],
            description=request.form["description"],
        )
        db.session.add(t)
        db.session.commit()
        return redirect(url_for("tickets"))

    return render_template("new_ticket.html")

@app.route("/tickets/<int:ticket_id>")
def ticket_detail(ticket_id):
    t = Ticket.query.get_or_404(ticket_id)
    return render_template("ticket_detail.html", ticket=t)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("is_admin"):
        return redirect(url_for("admin_login"))
    if request.method == "POST":
        ticket_id = request.form["ticket_id"]
        new_status = request.form["status"]
        t = Ticket.query.get_or_404(ticket_id)
        t.status = new_status
        db.session.commit()
        return redirect(url_for("admin"))

    status_filter = request.args.get("status")

    q = Ticket.query
    if status_filter:
        q = q.filter_by(status=status_filter)

    all_tickets = q.order_by(Ticket.created_at.desc()).all()
    return render_template("admin.html", tickets=all_tickets)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
