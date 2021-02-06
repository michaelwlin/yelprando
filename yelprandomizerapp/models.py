from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self,postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "Please enter a name."
        return errors
    def email_validator(self,postData):
        errors = {}
        if len(postData['email']) > 1:
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(postData['email']):           
                errors['email'] = "Please enter a valid email address."
        return errors
    def location_validator(self,postData):
        errors = {}
        if len(postData['location']) < 1:
            errors['location'] = "Please enter a location."
        return errors
    def term_validator(self,postData):
        errors = {}
        if len(postData['term']) < 1:
            errors['term'] = "Please enter a term."
        return errors
        
class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255,default=None,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

