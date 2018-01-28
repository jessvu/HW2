## SI 364
## Winter 2018
## HW 2 - Part 1

## This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

## Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

## As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, redirect, url_for, flash
import requests
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################




####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


@app.route('/artistform')
def artist_form():
	return render_template('artistform.html')


@app.route('/artistinfo')
def artist_info():
	if request.method == 'GET':
		result = request.args
		params = {}
		params['term'] = result.get('artist')
		resp = requests.get('https://itunes.apple.com/search?', params=params)
		data = json.loads(resp.text)
		return render_template('artist_info.html', objects=data['results'])

@app.route('/artistlinks')
def artist_links():
	return render_template('artist_links.html')

@app.route('/specific/song/<artist>')
def specific_artists(artist):
		params = {}
		params['term'] = artist
		params['entity'] = 'song'
		params['limit'] = 3
		resp = requests.get('https://itunes.apple.com/search?', params=params)
		data = json.loads(resp.text)
		# return json.dumps(data)
		return render_template('specific_artist.html', results=data['results'])

class AlbumEntryForm(FlaskForm):
	name = StringField('Enter the name of the album: ', validators=[Required()])
	rating = RadioField('How much do you like this album?', choices=[('1', '1'),('2', '2'),('3', '3')], validators=[Required()])
	submit = SubmitField('Submit')

@app.route('/album_entry')
def album():
	form = AlbumEntryForm()
	return render_template('album_entry.html', form=form)

@app.route('/album_result', methods=['GET', 'POST'])
def album_entry():
	form = AlbumEntryForm(request.form)
	if request.method == 'POST' and form.validate_on_submit():
		name = form.name.data
		rating = form.rating.data
		return render_template('album_data.html', form=form, name=name, rating=rating)
	flash('All fields are required!')
	return redirect(url_for('album'))

if __name__ == '__main__':
    app.run(use_reloader=True,debug=True) 
