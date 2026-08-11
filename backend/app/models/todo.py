from datetime import date, datetime, timezone
from app.extensions import db


class Todo(db.Model):
    __tablename__ = "todos"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(
        db.Integer(),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(), nullable=True, default="")
    priority = db.Column(db.String(16), nullable=False, default="medium")
    due_date = db.Column(db.Date(), nullable=True)
    is_completed = db.Column(db.Boolean(), nullable=False, default=False, index=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = db.relationship(
        "User",
        backref=db.backref("todos", lazy="dynamic", cascade="all, delete-orphan"),
    )

    @property
    def is_overdue(self) -> bool:
        if self.is_completed or not self.due_date:
            return False
        return self.due_date < date.today()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description or "",
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "is_completed": self.is_completed,
            "is_overdue": self.is_overdue,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
