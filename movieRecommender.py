import streamlit as st
import pandas as pd
import pickle
import pymongo
import requests
import streamlit as st
import config

client = pymongo.MongoClient(st.secrets["connectionUri"])

db = client.movieDatabase
movieCollection = db.movieCollection
favCollection = db['favCollection']

movies_dict = pickle.load(open('dataset/movies_dict.pk1', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('dataset/similarity.pk1', 'rb'))
clicked = []

def fetch_poster(movie_id):
	response = requests.get('https://api.themoviedb.org/3/movie/{0}?api_key={1}&language=en-US'.format(movie_id, st.secrets["api_key"]))
	data = response.json()
	return "https://image.tmdb.org/t/p/w500/"+data['poster_path']



def btnClicked(movieId):
	cursor = movieCollection.find_one({'movie_id': '{0}'.format(movieId)})
	with placeholder:
		col001, col002 = st.columns([1,2])
		with col001:
			st.image(fetch_poster(movieId))
		with col002:
			st.header(cursor['title'])
			st.write('genres: '+cursor['genres'])
			st.write('cast: '+cursor['cast'])
			st.write('director: '+cursor['crew'])
			st.write('overview: '+cursor['overview'])



def recommend(movie):
	movie_index = movies[movies['title'] == movie].index[0]
	distances = similarity[movie_index]
	movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
	recommend_movies = []
	recommend_movies_posters = []
	recommend_movies_id=[]
	for i in movies_list:
		movie_id = movies.iloc[i[0]].movie_id
		recommend_movies.append(movies.iloc[i[0]].title)
		recommend_movies_id.append(movie_id)
		recommend_movies_posters.append((fetch_poster(movie_id)))

	return recommend_movies, recommend_movies_posters, recommend_movies_id


# st.title('Jha Aparnas movie recommender system')
st.header('Jha Aparna\'s movie recommender system')
selected_movie = st.selectbox('Enter the movie', movies['title'].values)

col1, col2, col3, col4, col5 = st.columns(5)
placeholder = st.container()
errorPlaceHolder = st.container()


def addRecord(movieId):
	try:
		cursor1 = movieCollection.find_one({'movie_id': '{0}'.format(movieId)})
		favCollection.insert_one(cursor1)
		errorPlaceHolder.success("movie added")
	except:
		errorPlaceHolder.error("alrady exists")


if selected_movie:
	names, posters, moviesId = recommend(selected_movie)
	with col1:
		st.text(names[0])
		st.image(posters[0])
		if st.button("Details", key=0):
			btnClicked(moviesId[0])
		if st.button("add to fav", key=5):
			addRecord(moviesId[0])

	with col2:
		st.text(names[1])
		st.image(posters[1])
		if st.button("Details", key=1):
			btnClicked(moviesId[1])
		if st.button("add to fav", key=6):
			addRecord(moviesId[1])

	with col3:
		st.text(names[2])
		st.image(posters[2])
		if st.button("Details", key=2):
			btnClicked(moviesId[2])
		if st.button("add to fav", key=7):
			addRecord(moviesId[2])

	with col4:
		st.text(names[3])
		st.image(posters[3])
		if st.button("Details", key=3):
			btnClicked(moviesId[3])
		if st.button("add to fav", key=8):
			addRecord(moviesId[3])

	with col5:
		st.text(names[4])
		st.image(posters[4])
		if st.button("Details", key=4):
			btnClicked(moviesId[4])
		if st.button("add to fav", key=9):
			addRecord(moviesId[4])








# app = MultiApp()
# app.add_app("mainPage", mainPage)
# app.run()