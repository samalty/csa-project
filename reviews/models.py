from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg

class Accelerator(models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    bio = models.TextField()
    sector_focus = models.CharField(max_length=100)
    stage = models.CharField(max_length=100)
    deal = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    avg_rating = models.DecimalField(decimal_places=2, max_digits=3)
    avg_mentorship = models.DecimalField(decimal_places=2, max_digits=3)
    avg_hiring = models.DecimalField(decimal_places=2, max_digits=3)
    avg_community = models.DecimalField(decimal_places=2, max_digits=3)
    avg_fundraising = models.DecimalField(decimal_places=2, max_digits=3)
    avg_corporate = models.DecimalField(decimal_places=2, max_digits=3)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default='admin')
    logo = models.ImageField(upload_to='logos')

    def __str__(self):
        return self.name

    # Function to configure correct URL once new model instance has been created
    def get_absolute_url(self):
        return reverse('accelerator_detail', kwargs={'pk': self.pk})

    @property
    def avg_rating(self):
        quantity = Review.objects.filter(subject=self)
        overall_result = Review.objects.filter(subject=self).aggregate(avg_rating=Avg('overall'))['avg_rating']
        return overall_result if len(quantity) > 0 else float(0)
    
    @property
    def avg_mentorship(self):
        quantity = Review.objects.filter(subject=self)
        mentorship_result = Review.objects.filter(subject=self).aggregate(avg_mentorship=Avg('mentorship'))['avg_mentorship']
        return mentorship_result if len(quantity) > 0 else float(0)
    
    @property
    def avg_hiring(self):
        quantity = Review.objects.filter(subject=self)
        hiring_result = Review.objects.filter(subject=self).aggregate(avg_hiring=Avg('hiring'))['avg_hiring']
        return hiring_result if len(quantity) > 0 else float(0)
    
    @property
    def avg_community(self):
        quantity = Review.objects.filter(subject=self)
        community_result = Review.objects.filter(subject=self).aggregate(avg_community=Avg('community'))['avg_community']
        return community_result if len(quantity) > 0 else float(0)
    
    @property
    def avg_fundraising(self):
        quantity = Review.objects.filter(subject=self)
        fundraising_result = Review.objects.filter(subject=self).aggregate(avg_fundraising=Avg('fundraising'))['avg_fundraising']
        return fundraising_result if len(quantity) > 0 else float(0)
    
    @property
    def avg_corporate(self):
        quantity = Review.objects.filter(subject=self)
        corporate_result = Review.objects.filter(subject=self).aggregate(avg_corporate=Avg('corporate_dev'))['avg_corporate']
        return corporate_result if len(quantity) > 0 else float(0)

class Review(models.Model):
    RATINGS = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    subject = models.ForeignKey(Accelerator, on_delete=models.CASCADE, blank=False)
    title = models.CharField(max_length=200, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    feedback = models.TextField(blank=False)
    date_posted = models.DateTimeField(default=timezone.now)
    mentorship = models.IntegerField(choices=RATINGS, blank=False, default=1)
    hiring = models.IntegerField(choices=RATINGS, blank=False, default=1)
    community = models.IntegerField(choices=RATINGS, blank=False, default=1)
    fundraising = models.IntegerField(choices=RATINGS, blank=False, default=1)
    corporate_dev = models.IntegerField(choices=RATINGS, blank=False, default=1)
    overall = models.DecimalField(decimal_places=2, max_digits=3)

    def __str__(self):
        return self.subject
    
    def get_absolute_url(self):
        return reverse('review_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.overall = (int(self.mentorship) + int(self.hiring) + int(self.community) + \
            int(self.fundraising) + int(self.corporate_dev)) / 5
        super(Review, self).save(*args, **kwargs)