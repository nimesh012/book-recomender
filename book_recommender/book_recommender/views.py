from django.http import HttpResponse
from django.shortcuts import render
import pickle
import pandas as pd
import requests
from random import sample

popular_df = pd.read_csv('book_recommender\popular.csv')




def popular(df):
    li = []
    for i in range(0, df.shape[0]):
        data = {'name': df['Book-Title'][i], 'author': df['Book-Author'][i], 'rating': round(df['Avg-rating'][i], 2),
                'img': df['Image-URL-L'][i]}
        li.append(data)

    return li


def index(request):
    return render(request, 'index.html')


def top(request):
    top_data = popular(popular_df)
    params = {'data': top_data}
    return render(request, 'top.html', params)
