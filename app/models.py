from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from flask_sqlalchemy.model import Model
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login
from dataclasses import dataclass
from datetime import datetime, timezone


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String, index= True, unique=True)
    email: Mapped[str] = mapped_column(db.String, index=True, unique=True)
    password_hash: Mapped[str] = mapped_column(db.String)

    runs: Mapped[list['Run']] = relationship("Run", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Run(db.Model):
    __tablename__ = 'run'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    character: Mapped[str] = mapped_column(db.String(64), nullable=False)
    floor_reached: Mapped[int] = mapped_column(db.Integer, nullable=False)
    ascension_level: Mapped[int] = mapped_column(db.Integer, nullable=False)
    win: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    user_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('user.id'))
    user: Mapped["User"] = relationship(back_populates="runs")
    #Records the date of submission
    date_played: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=lambda: datetime.now(
        timezone.utc))
    #optional field
    notes: Mapped[str] = mapped_column(db.Text, nullable=True)
    # Many-to-many relation done via RunRelic and RunCard, the many has the ForeignKey
    run_relic: Mapped[list['RunRelic']] = relationship("RunRelic", back_populates="run")
    run_card: Mapped[list['RunCard']] = relationship("RunCard", back_populates="run")

class Card(db.Model):
    __tablename__ = 'card'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False)
    character: Mapped[str] = mapped_column(db.String(64), nullable=False)
    run_card: Mapped[list['RunCard']] = relationship("RunCard", back_populates="card")

class Relic(db.Model):
    __tablename__ = 'relic'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(db.String(64), nullable=False)
    character: Mapped[str] = mapped_column(db.String(64), nullable=False)
    run_relic: Mapped[list['RunRelic']] = relationship("RunRelic", back_populates="relic")

class RunRelic(db.Model):
    __tablename__ = 'run_relic'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    run_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('run.id'))
    run: Mapped["Run"] = relationship(back_populates="run_relic")
    relic_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('relic.id'))
    relic: Mapped["Relic"] = relationship(back_populates="run_relic")

class RunCard(db.Model):
    __tablename__ = 'run_card'
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    run_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('run.id'))
    run: Mapped["Run"] = relationship(back_populates="run_card")
    card_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey('card.id'))
    card: Mapped["Card"] = relationship(back_populates="run_card")
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False, default=1)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))