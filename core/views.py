from django.shortcuts import render
from .models import Movie
from django.views.generic import ListView

class MovieList(ListView):
    model = Movie
