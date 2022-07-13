from flask import(Flask,
      render_template,
      request, Response,
      flash,
      redirect,
      url_for)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from fyuurproject import db


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable = True,
    default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60")

    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    seeking_talent = db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='venue', lazy=True, passive_deletes=True)
  

    def __repr__(self):
      return f'<Venue {self.id} {self.name}>'


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500),nullable=True,
    default="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",)

    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_venue= db.Column(db.Boolean())
    seeking_description = db.Column(db.String(120))
    created_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    shows = db.relationship('Show', backref='artist', lazy=True, passive_deletes=True)

    def __repr__(self):
      return f'<Artist {self.id} {self.name}>'

class Show(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
      return f'<Show {self.id} {self.start_time}>'

