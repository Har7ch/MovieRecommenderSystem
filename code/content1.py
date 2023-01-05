from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import difflib
import pandas as pd
import numpy as np

df = pd.read_csv('movies_metadata.csv',low_memory=False)
df1 = pd.read_csv('credits.csv')
df2 = pd.read_csv('keywords.csv')
df3 = pd.read_csv('links_small.csv')
df4 = pd.read_csv('ratings_small.csv')
df_mod = df


df_mod.dropna(subset=['imdb_id','runtime','title','release_date'],inplace=True)
df_mod['id'] = [int(s) for s in df_mod['id']]
import ast
# s = (df['genres'].iloc[0])
def gen(s):
    ls = ast.literal_eval(s)
    h = ''
    for ele in ls:
        if h == '':
            h = h + ele['name']
        else:
            h = h + ' ' + ele['name']
    return h


df_mod['genres'] = [gen(s) for s in df_mod['genres']]
df_mod['adult'] = [0 if s == 'False' else 1 for s in df_mod['adult']]
df_mod['release_date'] = [int(s[:4]) for s in df_mod['release_date']]
df_mod = df_mod.rename(columns={'release_date':'release_year'})

df_mod = df_mod.merge(df1,on='id')
def director(s):
    ls = ast.literal_eval(s)
    for i in ls:
        if i['job'] == 'Director':
            return i['name']
    return None
df_mod['Director'] = [director(s) for s in df_mod['crew']]

def allCast(s):
    ls = ast.literal_eval(s)
#     return ls
    h = ''
    for i in ls:
        p = i['name']
        if h == '': 
            h = h + p
        else:
            h = h + ' ' + p
    return h
df_mod['cast'] = [allCast(s) for s in df_mod['cast']]

df_mod = df_mod.drop(['crew'],axis=1)
df_mod = df_mod.merge(df2,on='id')

def getKeys(s):
    ls = ast.literal_eval(s)
#     return ls
    h = ''
    for i in ls:
        p = i['name']
        if h == '': 
            h = h + p
        else:
            h = h + ' ' + p
    return h
df_mod['keywords'] = [getKeys(s) for s in df_mod['keywords']]
dff =df_mod
dff['popularity'] = [float(s) for s in dff['popularity']]
dff = dff[dff['popularity'] >= 2.9]
dff = dff[dff['release_year'] >= 1960]
dff = dff[dff['vote_average'] >= 6.1]
dff.reset_index(inplace=True)
dff = dff.drop(['index'],axis = 1)

selected_features = ['genres','keywords','tagline','cast','Director']
for feature in selected_features:
    dff[feature] = dff[feature].fillna('')


combined_features = dff['genres']+' '+ dff['keywords']+' '+dff['tagline']+' '+dff['cast']+' '+dff['Director']
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

similarity = cosine_similarity(feature_vectors)
list_of_all_titles = dff['title'].tolist()

def get_recommendation(title):
    find_close_match = difflib.get_close_matches(title, list_of_all_titles)
    close_match = find_close_match[0]
    index_of_the_movie = dff[dff.title == close_match].index.values[0]
    similarity_score = list(enumerate(similarity[index_of_the_movie]))
    sorted_similar_movies = sorted(similarity_score, key = lambda x:x[1], reverse = True) 

    final_ls = []
    i = 1
    for movie in sorted_similar_movies:
        index = movie[0]
        title_from_index = dff[dff.index==index]['title'].values[0]
        if(i == 1):
            i+=1
            continue
        if (i<=11):
            # print(i - 1, '.',title_from_index)
            final_ls.append(title_from_index)
            i+=1  
         
    return final_ls

# print(get_recommendation('Avatar'))
