from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from movie_rec import app
from movie_rec.forms import MovieTitleForm

from tmdbv3api import TMDb, Movie
import json
import requests

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
#from sklearn.metrics.pairwise import linear_kernel


######################
### functions ########
######################

# Function that takes in movie title as input and outputs recommended movies
def get_recommendations(title, cosine_sim):
	if title not in data['movie_title'].unique():
		return None
	else:
	    # Get the index of the movie that matches the title
	    idx = indices[title]
	    # Get the pairwsie similarity scores of all movies with that movie
	    sim_scores = list(enumerate(cosine_sim[idx]))
	    # Sort the movies based on the similarity scores
	    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
	    # Get the scores of the 10 most similar movies
	    sim_scores = sim_scores[1:13]
	    # Get the movie indices
	    movie_indices = [i[0] for i in sim_scores]
	    # Return the top 10 most similar movies
	    return data['movie_title'].iloc[movie_indices]

# Get trending movies with posters using themoviedb API
def get_trending_movies():
	tmdb = TMDb()
	tmdb_movie = Movie()
	response = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=23e48adb1f662882c97ada4b5569ff31&language=en-US&page=1')
	data_json = response.json()
	movies = []
	posters = []
	for i in range(0, 10):
		movies.append(data_json['results'][i]['title'])
		posters.append('https://image.tmdb.org/t/p/w500' + str(data_json['results'][i]['poster_path']))
	return movies, posters


#####################################################################################
# Load dataset and compute similarity matrix / Overview+Actors+Directors+Genres based
#####################################################################################
data = pd.read_csv("final_data.csv")

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(data['soup'])
cosine_sim_1 = cosine_similarity(count_matrix, count_matrix)

# data['overview'] = data['overview'].fillna('')
# tfidf = TfidfVectorizer(min_df=3,  max_features=None, strip_accents='unicode', 
# 	                analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1, 3), stop_words = 'english')
# tfidf_matrix = tfidf.fit_transform(data['overview'])
# cosine_sim_2 = linear_kernel(tfidf_matrix, tfidf_matrix)

data = data.reset_index(drop=True)
indices = pd.Series(data.index, index=data['movie_title'])


###################
### routes ########
###################

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
	# Get trending movies from IMDB using themoviedb API
	movies, posters = get_trending_movies()
	# Movie title form
	form = MovieTitleForm()
	if form.validate_on_submit():
		return redirect(url_for('recommend', movie_title=form.movie_title.data))
	return render_template('home.html', form=form, movies=movies, posters=posters)

@app.route("/recommend/<movie_title>", methods=['GET', 'POST'])
def recommend(movie_title):
	rec_movies = get_recommendations(movie_title.lower(), cosine_sim_1)
	#rec_movies_2 = get_recommendations(movie_title.lower(), cosine_sim_2)
	if rec_movies is None:
		flash('Sorry! This movie is not in our database. Please check the spelling or try with some other movies.', 'danger')
		return redirect(url_for('home'))
	rec_movies = rec_movies.tolist()
	#rec_movies_2 = rec_movies_2.tolist()
	#rec_movies = rec_movies_1 + rec_movies_2
	form = MovieTitleForm()
	if form.validate_on_submit():
		return redirect(url_for('recommend', movie_title=form.movie_title.data))
	return render_template('recommend.html', movie_title=movie_title, rec_movies=rec_movies, form=form)

@app.route("/trending")
def trending():
	tmdb = TMDb()
	tmdb_movie = Movie()
	response = requests.get('https://api.themoviedb.org/3/movie/popular?api_key=23e48adb1f662882c97ada4b5569ff31&language=en-US&page=1')
	data_json = response.json()
	movies = []
	posters = []
	for i in range(0, 10):
		movies.append(data_json['results'][i]['title'])
		posters.append('https://image.tmdb.org/t/p/w500' + str(data_json['results'][i]['poster_path']))
	return  str(posters)

@app.route("/login")
def login():
	  return render_template("login.html")

@app.route("/signup")
def signup():
	  return render_template("signup.html")




