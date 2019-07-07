from django.db import models


class Movie(models.Model):

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
    rating = models.IntegerField(choices=RATINGS, default=NOT_RATED)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)
    director = models.ForeignKey(to='Person', on_delete=models.SET_NULL, related_name='directed', null=True, blank=True)
    writers = models.ManyToManyField(to='Person', related_name='writing_credits', blank=True)



    def __str__(self):
        return '{} ({})'.format(self.title, self.year)


class Person(models.Model):
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
