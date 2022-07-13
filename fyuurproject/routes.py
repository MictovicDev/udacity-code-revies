from flask import (render_template,
      request, 
      Response,
      flash,
      redirect,
      url_for)
from fyuurproject import app
import sys
from fyuurproject import db
from fyuurproject.models import *
from datetime import datetime
from fyuurproject.forms import *
import dateutil.parser
import babel



def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime











@app.route('/')
def index():
  venues = Venue.query.order_by((Venue.created_date.desc())).limit(5).all()
  artists = Artist.query.order_by((Artist.created_date.desc())).limit(5).all()
  return render_template('pages/home.html', venues=venues, artists=artists)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  venues = Venue.query.all()

  return render_template('pages/venues.html', venues=venues)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  results = Venue.query.filter(Venue.name.ilike(search)).all()
  count = Venue.query.filter(Venue.name.ilike(search)).count()
  return render_template('pages/search_venues.html', results=results, search_term=request.form.get('search_term', ''), count=count)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  upcoming_shows = db.session.query(Show).join(Venue).filter_by(id=venue_id).filter(Show.start_time > time).all()
  past_shows = db.session.query(Show).join(Venue).filter_by(id=venue_id).filter(Show.start_time < time).all()
  venue = Venue.query.filter_by(id=venue_id).first()
  data={
    "id": venue.id,
    "name": venue.name,
    "genres": [venue.genres],
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
}
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(request.form)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate_on_submit():
    try:
      error = False
      form = VenueForm(request.form)

      name = form.name.data
      city = form.city.data
      state = form.state.data
      address = form.address.data 
      phone = form.phone.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_description = form.seeking_description.data
      seeking_talent = form.seeking_talent.data
      genres = request.form.getlist('genres')

      venue = Venue(name=name, 
      city=city,
      state=state,
      address=address,
      phone=phone,
      image_link=image_link,
      facebook_link=facebook_link,
      website_link=website_link,
      seeking_description=seeking_description,
      seeking_talent=seeking_talent,
      genres= genres)

      db.session.add(venue)
      db.session.commit()

    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
        db.session.close()
        if error:
          flash('Venue ' + request.form['name'] + ' was  not  successfully listed!')
          return render_template('forms/new_venue.html', form=form)
        if not error:
          flash('Venue ' + request.form['name'] + ' was successfully listed!') 
          return redirect(url_for('index'))
  return render_template('forms/new_venue.html', form=form)

  
      
    
    
@app.route('/venues/<venue_id>', methods=['POST'])
def delete_venue(venue_id):
  try:
    error = False
    venue = Venue.query.filter_by(id=venue_id).first()
    db.session.delete(venue)
    db.session.commit()
    flash('Venue deleted succesfully')
  except:
    db.session.rollback()
    error = True
  finally:
    db.session.close()
    if not error:
      return redirect(url_for('index'))
    if error:
      flash('venue could not be deleted')
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artist = Artist.query.all()
  return render_template('pages/artists.html', artists=artist)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  search = "%{}%".format(search_term)
  results = Artist.query.filter(Artist.name.ilike(search)).all()
  count = Artist.query.filter(Artist.name.ilike(search)).count()
  
  return render_template('pages/search_artists.html', results=results, search_term=request.form.get('search_term', ''), count=count)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  upcoming_shows = db.session.query(Show).join(Artist).filter_by(id=artist_id).filter(Show.start_time > time).all()
  past_shows = db.session.query(Show).join(Artist).filter_by(id=artist_id).filter(Show.start_time < time).all()
  artist= Artist.query.filter_by(id=artist_id).first()
  
  data={
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()

  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data= artist.phone
  form.image_link.data= artist.image_link
  form.facebook_link.data= artist.facebook_link
  form.genres.data = artist.genres
  form.website_link.data= artist.website_link
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()
  artist = Artist.query.filter_by(id=artist_id).first()
  if form.validate_on_submit():
    try:
      error= False


      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = form.genres.data
      artist.image_link = form.image_link.data
      artist.facebook_link = form.facebook_link.data
      artist.website_link = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data
      
      db.session.commit()

    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

    finally:
      db.session.close()
      if error:
        flash('Artist ' + request.form['name'] + ' was  not updated!')
        return render_template('forms/edit_venue.html', form=form)
      if not error:
        flash('Artist ' + request.form['name'] + ' was  updated!')
        return redirect(url_for('show_artist', artist_id=artist_id))
  return render_template('forms/edit_artist.html', form=form, artist=artist)



@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)

  venue = Venue.query.filter_by(id=venue_id).first()

  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.phone.data= venue.phone
  form.address.data = venue.address
  form.image_link.data= venue.image_link
  form.facebook_link.data= venue.facebook_link
  form.genres.data = venue.genres
  form.website_link.data= venue.website_link
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
 
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()
  venue = Venue.query.filter_by(id=venue_id).first()
  if form.validate_on_submit():
    try:
      error = False

      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.phone = form.phone.data
      venue.genres = form.genres.data
      venue.address= form.address.data
      venue.image_link = form.image_link.data
      venue.facebook_link = form.facebook_link.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data

      db.session.commit()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
        db.session.close()
        if error:
          flash('Venue ' + request.form['name'] + ' was  not updated!')
          return render_template('forms/edit_venue.html', form=form)
        if not error:
          flash('Venue ' + request.form['name'] + ' was updated!') 
          return redirect(url_for('show_venue', venue_id=venue_id))
  return render_template('forms/edit_venue.html', form=form, venue=venue)

  
  

    # if not error:
    #   return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  error = False
  if form.validate_on_submit():
    try:
      form = ArtistForm(request.form)

      name = form.name.data
      city = form.city.data
      state = form.state.data
      phone = form.phone.data
      image_link = form.image_link.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description= form.seeking_description.data
      genres = request.form.getlist('genres')

      artist = Artist(name=name, 
      city=city,
      state=state,
      phone=phone,
      image_link=image_link,
      facebook_link=facebook_link,
      website_link=website_link,
      seeking_venue=seeking_venue,
      seeking_description=seeking_description,
      genres = genres)

      db.session.add(artist)
      db.session.commit()
    
      
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())

    finally:
        db.session.close()
        if error:
          flash('Artist ' + request.form['name'] + ' was  not  successfully listed!')
        if not error:
          flash('Artist ' + request.form['name'] + ' was successfully listed!') 
          return redirect(url_for('index'))
  return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  shows = db.session.query(Show).join(Venue).join(Artist).all()
  data = []
  for show in shows:
    data.append({
    "venue_id": show.venue_id,
    "venue_name": show.venue.name,
    "artist_id": show.artist_id,
    "artist_name": show.artist.name,
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": format_datetime(str(show.start_time))
  })
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm(request.form)
  error = False
  if form.validate_on_submit():
    try:

      artist_id=int(form.artist_id.data)
      venue_id=int(form.venue_id.data)
      start_time=form.start_time.data.strftime('%Y-%m-%d %H:%S:%M')

      show=Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
      db.session.close()
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
        db.session.close()
    if not error:
      flash(' Your Show was listed successfully!') 
      return redirect(url_for('index'))
    if error:
      flash(' Your Show was not listed successfully!') 
      return render_template('forms/new_show.html', form=form)
  return render_template('forms/new_show.html', form=form)
  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(400)
def bad_request(error):
    return render_template('errors/404.html'), 400

@app.errorhandler(401)
def invalid_method(error):
    return render_template('errors/404.html'), 400
