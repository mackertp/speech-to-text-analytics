"""
Using flask to create a clean looking interface for the speech to text application created

was helped by using the following page to learn about building a flask app
https://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

@author Preston Mackert
"""

# ---------------------------------------------------------------------------------------------------- #
# imports 
# ---------------------------------------------------------------------------------------------------- #

import os
import ast
from flask import Flask, render_template
import helper_functions as helper

# ---------------------------------------------------------------------------------------------------- #
# main
# ---------------------------------------------------------------------------------------------------- #

# initialize the app
app = Flask(__name__)


# the home screen
@app.route("/")
def main():
	return render_template("mainmenu.html")


# ---------------------------------------------------------------------------------------------------- #
# main navigation pages
# ---------------------------------------------------------------------------------------------------- #

@app.route("/sendfiles")
def send_files():
	helper.send_batch("audio_files")
	return render_template("index.html")


# ---------------------------------------------------------------------------------------------------- #

@app.route("/transcripts")
def transcripts():
	# set up the selections for 
	transcriptions = []
	for json_file in os.listdir(os.getcwd()):
		if json_file.endswith(".json"):
			transcriptions.append(json_file)

	return render_template("transcripts.html", transcripts=transcriptions)


# ---------------------------------------------------------------------------------------------------- #

@app.route("/analytics/<transcript>")
def analytics(transcript):
	"""for each of the different analytic functions, we need to pass the desired outputs, because all 
	data structures get converted to strings""" 

	# get the dictionary from json data
	converted_json = helper.convert_json_to_data(transcript)

	# transcript already a string
	transcript = converted_json.get("transcript")

	# format total confidence
	percent = round(float(converted_json.get("confidence"))*100, 2)

	# format the word confidence levels
	word_conf = converted_json.get("words")

	# render the template!
	return render_template("analytics.html", text=transcript, percent=percent, words=word_conf)


# ---------------------------------------------------------------------------------------------------- #
# analytics pages
# ---------------------------------------------------------------------------------------------------- #

@app.route("/printtranscript/<text>")
def print_transcript(text):
	return render_template("printtranscript.html", text=text)


# ---------------------------------------------------------------------------------------------------- #

@app.route("/totalconfidence/<percent>")
def total_confidence(percent):
	percent = float(percent)
	return render_template("totalconfidence.html", percent=percent)


# ---------------------------------------------------------------------------------------------------- #

@app.route("/wordconfidence/<words>")
def word_confidence(words):
	words = ast.literal_eval(words)
	new_words = []
	for word in words:
		percent = round(word[1]*100, 2)
		new_words.append([word[0], percent])
	return render_template("wordconfidence.html", words=new_words)


# ---------------------------------------------------------------------------------------------------- #

@app.route("/analyzetone/<text>")
def analyze_tone(text):
	try:
		tones = helper.analyze_tone(text)
		for tone in tones:
			tones[tone] = float(round(tones[tone]*100,2))
		return render_template("analyzetone.html", text=tones)
	except:
		return render_template("nopersonality.html")


# ---------------------------------------------------------------------------------------------------- #

@app.route("/personalityinsights/<text>")
def personality_menu(text):
	try:
		personality = helper.analyze_personality(text)
		return render_template("personalitymenu.html", personality=personality)
	except:
		return render_template("nopersonality.html")


# ---------------------------------------------------------------------------------------------------- #
# call main
# ---------------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
	app.run(debug=True)
