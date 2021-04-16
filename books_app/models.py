from django.db import models
import re


class Showmanager(models.Manager):
    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        return errors

    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"
        if len(postData['username']) < 2:
            errors["username"] = "Username should be at least 2 characters"
        if len(postData['password']) < 6:
            
        if postData['password'] != postData['c_password']:
                errors['c_password'] = "passwords do not match"
                errors["password"] = "Password should be at least 6 characters"
        # else:
        #     repeatUsername = User.objects.filter(username=postData['username'])
        #     if len(repeatUsername) > 0:
        #         errors['invalid_username'] = "username already taken"
        

        try:
            User.objects.get(email=postData['email'])
            print("hello!")
            errors['email_unique'] = 'That email address is already in use'
        except:
            pass
        try:
            User.objects.get(username = postData['username'])
            errors['username_unique'] = 'That username is already in use'
        except:
            pass
        return errors


class User(models.Model):
    username = models.CharField(max_length=55, default="NewUser")
    firstn = models.CharField(max_length=55, default="first name")
    namesuf = models.CharField(max_length=55, default="last name")
    email = models.EmailField(default="email")
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Showmanager()


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)