from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Accelerator(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    bio = models.TextField()
    sector_focus = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)
    deal = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    overall_rating = models.DecimalField(decimal_places=2, max_digits=3)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='admin')
    logo = models.ImageField(default='default.jpg', upload_to='logos')

    def __str__(self):
        return self.name

    # Function to configure correct URL once new model instance has been created
    def get_absolute_url(self):
        return reverse('accelerator_detail', kwargs={'pk': self.pk})

# Accelerator.objects.filter(name='')

class Review(models.Model):
    RATINGS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    subject = models.ForeignKey(Accelerator, on_delete=models.CASCADE, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, default='admin')
    feedback = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    mentorship = models.CharField(choices=RATINGS, blank=False, max_length=1)
    hiring = models.CharField(choices=RATINGS, blank=False, max_length=1)
    community = models.CharField(choices=RATINGS, blank=False, max_length=1)
    fundraising = models.CharField(choices=RATINGS, blank=False, max_length=1)
    corporate_dev = models.CharField(choices=RATINGS, blank=False, max_length=1)
    overall = models.DecimalField(decimal_places=2, max_digits=3)

    def __str__(self):
        return self.subject
    
    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.pk})

    def save(self):
        self.overall = (int(self.mentorship) + int(self.hiring) + int(self.community) + \
            int(self.fundraising) + int(self.corporate_dev)) / 5

        super(Review, self).save()