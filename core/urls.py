from django.urls import path

from . import views

# this code raises the following error although it is quite similar to the one below.
# Reverse for 'UpdateVote' with keyword arguments '{'movie_id': 2, 'pk': 2}' not found. 
# 1 pattern(s) tried: ['movie/<int:movie_id/vote/(?P<pk>[0-9]+)$']
# app_name = 'core'
# urlpatterns = [
#     path('movies', 
#         views.MovieList.as_view(), 
#         name='MovieList'),
#     path('movie/<int:pk>', 
#         views.MovieDetail.as_view(), 
#         name='MovieDetail'),
#     path('movie/<int:movie_id>/vote', 
#         views.CreateVote.as_view(), 
#         name='CreateVote'),
#     path('movie/<int:movie_id>/image/upload', 
#         views.MovieImageUpload.as_view(), 
#         name='MovieImageUpload'),
#     path('movie/<int:movie_id/vote/<int:pk>', 
#         views.UpdateVote.as_view(), 
#         name='UpdateVote'),
#     path('person/<int:pk>',
#          views.PersonDetail.as_view(),
#          name='PersonDetail'),
# ]

# this code works although it  is quite similar to the one above!
app_name = 'core'
urlpatterns = [
    path('movies',
         views.MovieList.as_view(),
         name='MovieList'),
    path('movie/<int:pk>',
         views.MovieDetail.as_view(),
         name='MovieDetail'),
    path('movie/<int:movie_id>/vote',
         views.CreateVote.as_view(),
         name='CreateVote'),
    path('movie/<int:movie_id>/image/upload',
         views.MovieImageUpload.as_view(),
         name='MovieImageUpload'),
    path('movie/<int:movie_id>/vote/<int:pk>',
         views.UpdateVote.as_view(),
         name='UpdateVote'),
    path('person/<int:pk>',
         views.PersonDetail.as_view(),
         name='PersonDetail'),
]
