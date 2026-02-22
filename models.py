from datetime import datetime
from db import db

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)

    status = db.Column(db.String(50), default="Open")
    priority = db.Column(db.String(20), default="Medium")  # Low, Medium, High
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
