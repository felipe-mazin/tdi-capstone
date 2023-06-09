import os
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
import pandas as pd
import seaborn as sns
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn import base
from sklearn.feature_extraction import DictVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.neighbors import NearestNeighbors
from sklearn.linear_model import RidgeCV, LinearRegression, SGDRegressor, Ridge
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer

def remove_multistrings(cur_string, replace_list):
    for cur_word in replace_list:
        cur_string = cur_string.replace(cur_word, '')
    return cur_string


def get_fragrecs(all_inputs):
    
    
    gender = all_inputs['gender']
    age = all_inputs['age']
    weather = all_inputs['weather']
    time_of_day = all_inputs['time_of_day']
    occasion = all_inputs['occasion']
    popularity = all_inputs['popularity']
    comments = all_inputs['comments']
    similar_frags = all_inputs['similar_frags']
    rarity = all_inputs['rarity']
#     min_price = 
#     max_price = 
    
    if rarity == True:
        floor_count = 10
    else:
        floor_count = 100

    # Imports the .parquet file with the fragrance database
    df = pd.read_parquet('Fragrance_database.parquet')
    df = df[(df['count_ratings'] > floor_count)]
    df = df.astype({'fragrance':'string'})

    # Joins all summaries for a fragrance in only one string and removes the fragrance's name and brand
    df['summary_reviews'] = df['pros'].apply(lambda x: ' '.join(x) if x.size > 0 else '') + df['cons'].apply(lambda x: ' '.join(x) if x.size > 0 else '')
    df['summary_reviews'] = df.apply(lambda x: x.summary_reviews.lower() if x.summary_reviews != '' else math.nan, axis = 1)

    # Joins all comments for a fragrance in only one string and removes the fragrance's name and brand
    df['joined_comments'] = df['comments'].apply(lambda x: ' '.join(x) if x.size > 0 else '')
    df['joined_comments'] = df.apply(lambda x: remove_multistrings(x.joined_comments.lower(), x[0].lower().split() + x.brand.lower().split()) if x.joined_comments != '' else math.nan, axis = 1)

#     df['joined_comments'] = df['comments'].apply(lambda x: ' '.join(x) if x.size > 0 else '')
#     df['joined_comments'] = df.apply(lambda x: x.comments.lower() if x.comments != '' else math.nan, axis = 1)
    
    extra_comments = ""
    
    # GENDER
    if gender == "Female":
        cond_gender = df['masculine'] < 2.5
    elif gender == "Male":
        cond_gender = df['masculine'] > 3.5
    else:
        cond_gender = (df['masculine'] > 2) & (df['masculine'] < 4)
        
    # AGE RANGE
#     if age == "14-18":
        
    
    # WEATHER
    if weather == "Hot":
        cond_weather = df['votes_summer'] > df['votes_winter']
    elif weather == "Cold":
        cond_weather = df['votes_summer'] < df['votes_winter']
    elif weather == "Year-Round":
        cond_weather = (df['votes_summer'] > 0.4) & (df['votes_winter'] > 0.4)
    
        
    # TIME OF DAY
    if time_of_day == "Day":
        cond_day = df['votes_day'] > df['votes_night'] - 0.2
    elif time_of_day == "Night":
        cond_day = df['votes_day'] - 0.2 < df['votes_night']
    else:
        cond_day = (df['votes_day'] > 0.4) & (df['votes_night'] > 0.4)
    
    # OCCASION
    
    cond_occ = True
    if occasion == "Office":
        cond_occ = df['sillage'] < 3
    elif (occasion == "Date") or (occasion == "Any"):
        cond_occ = df['sillage'] < 3.5
    elif occasion == "Bar or Club":
        cond_occ = df['sillage'] > 3.5
    elif occasion == "Special Occasion":
        extra_comments = "Distinguished, Sophisticated fragrance, classy fragrance, elegant fragrance for special occasions such as weddings, formal events, black tie parties, upscale events."
        
    
    
    df_filtered = df[cond_gender & cond_weather & cond_day & cond_occ] #  
    
    vectorizer = TfidfVectorizer(min_df = 0.01, max_df = 0.6, ngram_range=(1,4), stop_words='english') #max_features=4000
    
    X = vectorizer.fit_transform(df_filtered.dropna(subset = ['joined_comments']))
    
    nn = NearestNeighbors(n_neighbors=20)
    nn.fit(X)
    
    vec_input = vectorizer.transform(list(all_inputs['comments'] + " " + extra_comments))
    dists, indices = nn.kneighbors(vec_input)
    recs = df_filtered.iloc[indices[0]][['fragrance','brand','year','rating']].sort_values('rating', ascending = False)
    #.astype({'year':'int'})
    
    return recs