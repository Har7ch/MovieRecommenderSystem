import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

movies_df = pd.read_csv('movies.csv')
title_list = movies_df['title'].tolist()
movies_df['genres'] = movies_df['genres'].apply(lambda x: np.nan if x == '\\N' else x)
movies_df = movies_df[movies_df['genres'].notna()]
movies_df.reset_index(drop=True,inplace=True)
cv = CountVectorizer(dtype=np.uint8)
dtm = cv.fit_transform(movies_df['genres']).toarray()

new_matrix = np.concatenate((dtm, np.array(movies_df['vote_average']).reshape(-1,1)),axis=1)
MMS = MinMaxScaler()
numVotes = np.array(movies_df['vote_count'])
numVotes = numVotes.reshape(-1,1)
numVotes = MMS.fit_transform(numVotes)
new_matrix = np.concatenate((new_matrix,numVotes),axis=1)

similarities = cosine_similarity(new_matrix,dense_output=False)

movies_df.reset_index()

import difflib
# movie_name = input(' Enter your favourite movie name : ')
def recommendation_list(title):
    list_of_all_titles = movies_df['title'].tolist()
    find_close_match = difflib.get_close_matches(title, list_of_all_titles)
    close_match = find_close_match[0]
    #print(close_match)
    index_of_the_movie = movies_df[movies_df['title']==close_match].index.values
    #print(index_of_the_movie[0])
    similarity_score = list(enumerate(similarities[index_of_the_movie[0]]))
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True)
    #print('Movies suggested for you : \n')
    i = 1
    mov = []
    for movie in sorted_similar_movies:
      index = movie[0]
      title_from_index = movies_df[movies_df.index==index]['title'].values[0]
      if (i<12):
        mov.append(title_from_index)
        i+=1
    return mov

def recommend(title):
    try:
        ans = []
        mov = recommendation_list(title)
        for i in range(11):
            ans.append(mov[i])
        return ans
    except:
        return None

def get_movies_data():
    return title_list
