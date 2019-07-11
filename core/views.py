from django.shortcuts import render, redirect
from .models import Movie, Person, Vote
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from core.forms import VoteForm, MovieImageForm
from django.core.exceptions import PermissionDenied



class MovieList(ListView):
    model = Movie


class MovieDetail(DetailView):

    # when MovieDetail uses get() on its query set, the Movie will have a score attribute.
    queryset = Movie.objects.all_with_related_persons_and_score()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_form'] = self.movie_image_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(movie=self.object, user=self.request.user)

            if vote.id:
                vote_form_url = reverse('core:UpdateVote', kwargs={'movie_id': vote.movie.id, 'pk': vote.id})
        
            else:
                vote_form_url = reverse('core:CreateVote', kwargs={'movie_id': self.object.id})
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
        return ctx


    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None



class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    # this function pre-populates a form with initial values before the form gets data values from the request.
    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    # this function is called by CreateView to return a response with the render template to the client,in this case though
    # it returns an HTTP redirect to MovieDetail.
    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    # Checks whether the vote is of the logged in user to prevent Vote tampering.
    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied("cannot change another user's vote")
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)


class MovieImageUpload(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial
    
    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail', kwargs={'pk': movie_id})
        return movie_detail_url

    
