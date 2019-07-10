from django.shortcuts import render
from .models import Movie, Person
from django.views.generic import ListView, DetailView


class MovieList(ListView):
    model = Movie


class MovieDetail(DetailView):
    queryset = Movie.objects.all_with_related_persons()


class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()