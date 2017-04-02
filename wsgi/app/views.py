'''
	library / scripts imports
'''
from app import app
from app import simple
#from app import database
from simple import polynomial
#from database import get_all_collections
#from database import get_db_methods_and_attributes
#from database import get_collection_methods_and_attributes
from flask import render_template, request, Flask, flash, redirect, session, abort
from flask_navigation import Navigation
import unirest
from forms import MessageForm
import urllib2
import json

# initialise Navigation Bar
nav = Navigation(app)
nav.init_app(app)

# adding templates to the navbar
nav.Bar('top', [
	nav.Item('Home','home'),
	nav.Item('Emotion App','emotion_post'),
	nav.Item('Visualization App','visualization'),
	nav.Item('Exchange Rates App','exchange_rates'),
])

# the default home template rendering
@app.route('/')
def home():
	return render_template("index.html")

# visualization from bokeh rendering
@app.route('/visualization/')
def visualization():
    plot_snippet = polynomial()
    return plot_snippet	

# emotion API form rendering
@app.route('/emotion/')
def emotion():
	return render_template("my_form.html",mood='happy',form=MessageForm())

# request to the emotion API to analyse user's input
@app.route('/emotion/', methods=['POST'])
def emotion_post():
	msg = request.form['message']
	response = unirest.post("https://community-sentiment.p.mashape.com/text/",
	  headers={
	    "X-Mashape-Key": "6VWQcE5umumsh9oLsHfFlOseFGbDp1caaUKjsnj6PJRqxZKslv",
	    "Content-Type": "application/x-www-form-urlencoded",
    	"Accept": "application/json"
    	},
  		params={
    	"txt": msg
  		}
	)
	return render_template("my_form.html",mood=response.body['result']['sentiment'],form=MessageForm())
'''
# renders collections in the db
@app.route('/database/collections')
def db_rah():
	show_databases = get_all_collections()
	return show_databases
@app.route('/database/methods')
def db_methods():
	get_methods_atts_db = get_db_methods_and_attributes()
	return get_methods_atts_db

@app.route('/database/London/methods')
def db_collection_methods():
	get_methods_atts_collection = get_collection_methods_and_attributes()
	return get_methods_atts_collection
'''
def getExchangeRates():
    rates = []
    response = urllib2.urlopen('http://api.fixer.io/latest')
    data = response.read()
    rdata = json.loads(data, parse_float=float)
 
    rates.append( rdata['rates']['USD'] )
    rates.append( rdata['rates']['GBP'] )
    rates.append( rdata['rates']['HKD'] )
    rates.append( rdata['rates']['AUD'] )
    return rates

@app.route("/exchange_rates/")
def exchange_rates():
    rates = getExchangeRates()
    return render_template('google.html',**locals()) 