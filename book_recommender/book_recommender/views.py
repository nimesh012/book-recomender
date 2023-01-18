from django.http import HttpResponse
from django.shortcuts import render
import pickle
import pandas as pd
import numpy as np
import requests
from random import sample

popular_df = pd.read_csv('book_recommender\\popular.csv')
books = pd.read_csv('book_recommender\\books.csv')
pt = pickle.load(open('pt.pkl', 'rb'))
cs = pickle.load(open('cs.pkl', 'rb'))


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


def recommend(request):
    return render(request, 'recommend.html')


def recommend_book(book_name):
    pointer = False

    book_d = []
    if book_name not in pt.index:
        for i in range(0, popular_df.shape[0]):
            data = {'title': popular_df['Book-Title'][i], 'author': popular_df['Book-Author'][i], 'year': round(popular_df['Avg-rating'][i], 2),
                    'Image': popular_df['Image-URL-L'][i]}
            book_d.append(data)
        return book_d, pointer

    else:
        pointer = True
        book_data = []
        index_t = np.where(pt.index == book_name)[0][0]
        similar = sorted(list(enumerate(cs[index_t])), key=lambda x: x[1], reverse=True)[1:7]
        for i in similar:
            data = {'title': list(books[books['Book-Title'] == pt.index[i[0]]]['Book-Title'].values)[0],
                    'author': list(books[books['Book-Title'] == pt.index[i[0]]]['Book-Author'].values)[0],
                    'Year': list(books[books['Book-Title'] == pt.index[i[0]]]['Year-Of-Publication'].values)[0],
                    'Image': list(books[books['Book-Title'] == pt.index[i[0]]]['Image-URL-L'].values)[0]}
            book_data.append(data)
        return book_data, pointer




def recommendation(request):
    book_recommended = request.GET.get('book', 'default')
    book_list, pointer = recommend_book(book_recommended)
    params = {'books_list': book_list, 'pointer': pointer}
    return render(request, 'recommendation.html', params)
