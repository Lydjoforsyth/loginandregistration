from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['first_name']) < 1:
            errors['first_name'] = 'First name cannot be blank.'
        if len(postData['last_name']) < 1:
            errors['last_name'] = 'Last name cannot be blank.'
        if len(postData['email']) < 1:
            errors['email'] = 'Email cannot be blank.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email is not valid.'
        # if postData['bday'] == '':
        #     errors['beday'] = 'Birthdate must be filled in.'
        # date = datetime.strptime(postData['bday'], '%Y-%m-%d')
        # if date > datetime.now():
        #     errors['bday'] = 'Birthdate cannot be in the future.'

        result = User.objects.filter(email=postData['email'])
        if len(result) > 0:
            errors['email'] = 'Email address is already registered.'

        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
        elif len(postData['password']) != len(postData['confirm_password']):
            errors['password'] = 'Passwords do not match.'
        return errors
    
    def validator_edit(self, data, id):
        errors = self.validator(data)

        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

