from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(UserMixin, db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)

    opportunities = db.relationship(
        'Opportunity',
        backref='admin',
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, **kwargs):
        if 'email' in kwargs and kwargs['email']:
            kwargs['email'] = kwargs['email'].lower().strip()
        super().__init__(**kwargs)

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<Admin {self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email
        }

class Opportunity(db.Model):
    __tablename__ = 'opportunity'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(50), nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)

    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.Text, nullable=False)

    category = db.Column(db.String(50), nullable=False)
    future_opportunities = db.Column(db.Text, nullable=True)

    max_applicants = db.Column(db.Integer, nullable=False, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    admin_id = db.Column(
        db.Integer,
        db.ForeignKey('admin.id'),
        nullable=False,
        index=True
    )

    def __init__(self, **kwargs):
        if 'skills' in kwargs and kwargs['skills']:
            skills = [s.strip() for s in kwargs['skills'].split(",") if s.strip()]
            kwargs['skills'] = ",".join(sorted(set(skills)))

        if 'max_applicants' in kwargs:
            kwargs['max_applicants'] = max(0, int(kwargs['max_applicants'] or 0))

        super().__init__(**kwargs)

    def get_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(",") if s.strip()]

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "start_date": self.start_date.strftime("%Y-%m-%d") if self.start_date else None,
            "end_date": self.end_date.strftime("%Y-%m-%d") if self.end_date else None,
            "description": self.description,
            "skills": self.skills,
            "skills_list": self.get_skills_list(),
            "category": self.category,
            "future_opportunities": self.future_opportunities,
            "max_applicants": self.max_applicants,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else None,
            "updated_at": self.updated_at.strftime("%Y-%m-%d %H:%M") if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Opportunity {self.title}>"