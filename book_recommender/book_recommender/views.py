from django.http import HttpResponse
from django.shortcuts import render
import pickle
import pandas as pd
import requests
from random import sample




def index(request):
    return render(request, 'index.html')
