from django.db import models
from django.conf import settings



class MovieManager(models.Manager):

    def all_with_related_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')
        qs = qs.prefetch_related('writers', 'actors')
        return qs


class Movie(models.Model):
    objects = MovieManager()
    # An inner class to provide ordering for the year and title on a page in 
    # descending order due to the (-) prefix.
    class Meta:
        ordering = ('-year', 'title')

    # Attributes to provide rating choices of the movies.
    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3
    RATINGS = (
        (NOT_RATED, 'NR - Not Rated'),
        (RATED_G, 'G - General Audiences'),
        (RATED_PG, 'PG - Parental Guidance'
        'Suggested'),
        (RATED_R, 'R - Restricted'),
    )

    title = models.CharField(max_length = 140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(
        choices=RATINGS,
        default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(
        to='Person', 
        on_delete=models.SET_NULL, 
        related_name='directed', 
        null=True, 
        blank=True)
    writers = models.ManyToManyField(
        to='Person', 
        related_name='writing_credits', 
        blank=True)
    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True)



    def __str__(self):
        return '{} ({})'.format(self.title, self.year)




class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related('directed', 'writing_credits', 'role_set_movies')


class Person(models.Model):
    objects = PersonManager()
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    born = models.DateField()
    died = models.DateField(null=True, blank=True)
    

    class Meta:
        ordering = ('last_name', 'first_name')
    

    def __str__(self):
        if self.died:
            return '{}, {} ({}-{})'.format(self.last_name, self.first_name, self.born, self.died)
        return  '{}, {} ({})'.format(self.last_name, self.first_name, self.born)


# An intermediary class to describe the many-to-many relationship between the Movie and Person classes.
class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return '{} {} {}'.format(self.movie_id, self.person_id, self.name)

    class Meta:
        unique_together = ('movie', 'person', 'name')


class Vote(models.Model):
    UP = 1
    DOWN = -1
    VALUE_CHOICES = ((UP, 'thumb up',),(DOWN, 'thumb down',),)

    value = models.SmallIntegerField(choices=VALUE_CHOICES,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
