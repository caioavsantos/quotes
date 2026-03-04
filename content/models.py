from django.db import models
from django.core import validators
from django.contrib.auth.models import User
from django.conf import settings



class Thinker (models.Model):
    name = models.CharField(
        max_length=50, help_text="- Thinker name", validators=[validators.MinLengthValidator(1, "Please enter at least one character")])
    #photo = see how to put a photo in the db, null = True
    works = models.ManyToManyField("Work", blank=True)
    picture = models.ImageField (null=True, blank=True, upload_to="pictures/")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Work (models.Model):
    name = models.CharField(
        max_length=50, help_text="Work name", validators=[validators.MinLengthValidator(1, "Please enter at least one character")])
    thinkers = models.ManyToManyField("Thinker", blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.name
    
class Authorship(models.Model):
    Thinker = models.ForeignKey("Thinker", on_delete=models.CASCADE)
    Work = models.ForeignKey("Work", on_delete=models.CASCADE)


class Quote(models.Model):
    quote = models.TextField(
        max_length=2000, validators=[validators.MinLengthValidator(10, "Please enter at least ten characters"), validators.MaxLengthValidator(2000,"Too many characters!")])
    thinker = models.ForeignKey("Thinker", on_delete=models.CASCADE, null=True, blank=True)
    reference = models.CharField(
        max_length=100, help_text="- Which work is this quote from?", validators=[
            validators.MinLengthValidator(1, "Please enter at least one character"), validators.MaxLengthValidator(100,"Too many characters!")],
              null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    explanation = models.TextField(help_text="- Please explain this quote", validators=[validators.MinLengthValidator(10, "Please enter at least ten characters")], null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_quotes", blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    @property
    def snippet(self):
        if not self.quote:
            return ""
        words = self.quote.split()
        snippet = " ".join(words[:10])
        return f"{snippet}..." if len(words) > 10 else snippet
    
    def __str__(self):
        """String for representing the Model object"""
        return self.snippet

class DailyQuote(models.Model):
    date = models.DateField(unique=True)
    quote = models.ForeignKey("Quote", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date}, {self.quote.id}"
    
class Picture(models.Model):
    title = models.CharField(
        max_length=20, help_text="Picture name", validators=[validators.MinLengthValidator(1, "Please enter at least one character")], null=True, blank=True)

    picture = models.ImageField (null=True, blank=True, upload_to="pictures/")
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text="File type")

    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        """String for representing the Model object"""
        return self.title

# reference as a filed in quote instead of works model?

"""class Comment (models.Model):
    set many to many field with user"""

