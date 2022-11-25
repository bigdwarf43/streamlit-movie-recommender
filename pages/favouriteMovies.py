import streamlit as st
import pymongo
import config
from movieRecommender import fetch_poster

client = pymongo.MongoClient(st.secrets["connectionUri"])
db = client.movieDatabase
favCollection = db['favCollection']

colNum = 0

movieCollection = db.movieCollection
cursor = favCollection.find({})

i = 0
st.title("Your favourite movies")
placeholder = st.container()
successPlaceHolder=st.container()

placeHolderArr = []



if favCollection.count_documents({}) == 0:
	st.info("Your list is empty")


for document in cursor:
	cursor = movieCollection.find_one({'movie_id': '{0}'.format(document['movie_id'])})
	with placeholder:
		col001, col002 = st.columns([1,2])
		with col001:
			st.image(fetch_poster(document['movie_id']))
		with col002:
			st.header(cursor['title'])
			st.write('genres: '+cursor['genres'])
			st.write('cast: '+cursor['cast'])
			st.write('director: '+cursor['crew'])
			st.write('overview: '+cursor['overview'])
			if st.button("delete", key=i):
				favCollection.delete_one({'movie_id': '{0}'.format(document['movie_id'])})
				st.experimental_rerun()
	placeHolderArr.append(placeholder)
	i+=1

# cursor = movieCollection.find({'movie_id': '{0}'.format(movieId)})


# with placeholder:
# 	col001, col002 = st.columns([1,2])
# 	with col001:
# 		st.image(fetch_poster(movieId))
# 	with col002:
# 		st.header(cursor['title'])
# 		st.write('genres: '+cursor['genres'])
# 		st.write('cast: '+cursor['cast'])
# 		st.write('director: '+cursor['crew'])
# 		st.write('overview: '+cursor['overview'])
# 		st.write(cursor)