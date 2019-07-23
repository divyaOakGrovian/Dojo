from __future__ import unicode_literals
from django.db import models
from django.utils.dateparse import parse_date
from datetime import date, datetime
import bcrypt
import re

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,20}$')
   
        firstname = postData['firstname']
        lastname = postData['lastname']
        email = postData['email']
        password = postData['password']
        cnfmpassword = postData['cnfmpassword']

        if (not firstname):
            errors['firstname_notExists'] = 'First Name is a required field! Please enter a value.'

        if len(firstname) < 3:
            errors['firstname_minLength'] = 'First Name should be at least 3 characters long!'
        
        if len(firstname) > 50:
            errors['firstname_maxLength'] = 'First Name should be no longer than 50 characters!'

        if not firstname.isalpha():
            errors['firstname_format'] = 'First Name should only have alphanumeric characters!'

        if (not lastname):
            errors['lastname_notExists'] = 'Last Name is a required field! Please enter a value.'

        if len(lastname) < 3:
            errors['lastname_minLength'] = 'Last Name should be at least 3 characters long!'
        
        if len(lastname) > 50:
            errors['lastname_maxLength'] = 'Last Name should be no longer than 50 characters!'

        if not lastname.isalpha():
            errors['lastname_format'] = 'Last Name should only have alphanumeric characters!'

        if (not email):
            errors['rm_notExists'] = 'Email is a required field! Please enter a value.'

        if len(email) < 7:
            errors['rm_minLength'] = "An email address should be at least 7 characters long!"

        if not EMAIL_REGEX.match(email):
            errors['rm_format'] = "Invalid format of email address. It should look like xyz@<domain>.<tag>!"

        if User.objects.filter(email=email):
            errors['rm_duplication'] = "Email already exists!"

        if (not password):
            errors['password_notExists'] = 'Password is a required field! Please enter a value.'

        if len(password) < 8:
            errors['password_minLength'] = 'Password should be at least 8 characters long!'
        
        if len(password) > 20:
            errors['password_maxLength'] = 'Password should be no longer than 20 characters!'

        if not PASSWORD_REGEX.match(password):
            errors['password_format'] = "Invalid format of Password! A password should be 8-20 characters long, contain at least 1 Uppercase, 1 Lowercase, 1 Special character, and 1 Number."

        if password != cnfmpassword:
            errors['cnfmpassword'] = 'Password and Confirm-Password fields do not match. Please re-enter!'

        return errors


    def login_validator(self, postData):
        errors = {}

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')    

        email = postData['loginemail'].strip()
        password = postData['loginpassword'].strip() if len(postData['loginpassword'].strip()) else ""
        
       
        user = User.objects.filter(email = email)
        print(f'in login_validator - User = {user}')

        if (not email):
            errors['notExists_email'] = 'Email is a required field! Please enter a value.'

        if len(email) < 7:
            errors['minLength_email'] = "An email address should be at least 7 characters long!"

        if not EMAIL_REGEX.match(email):
            errors['format_email'] = "Invalid format of email address. It should look like xyz@<domain>.<tag>!"
        elif not user:
            errors['user_notExists'] = 'No User with this email-address exists!'
            
        if not (user and bcrypt.checkpw(password.encode(), user[0].password.encode())):
             errors["loginPwd"] = 'Password is invalid!'
             print('Performed the password check')
        return errors    

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors = {}   
        jobTitle = postData['title'].strip()
        jobDescription = postData['desc'].strip()
        jobLocation = postData['location'].strip()
                
        if (not jobTitle):
            errors['jobTitle_notExists'] = 'Job Title is a required field! Please input a value.'
            print("Errtitle1")

        if len(jobTitle) < 3:
            errors['jobTitle_minLength'] = 'Job Title should be at least 3 characters long!'
            print("Errtitle2")

        if (not jobDescription):
            errors['jobDescription_notExists'] = 'Job Description is a required field! Please input a value.'
            print("Errdesc1")
        
        if len(jobDescription) < 3:
            errors['jobDescription_minLength'] = 'Job Description should be at least 3 characters long!'
            print("Errdesc2")

        if (not jobLocation):
            errors['jobLocation_notExists'] = 'Job Location is a required field! Please input a value.'
            print("Errloc1")
        
        if len(jobLocation) < 3:
            errors['jobLocation_minLength'] = 'Job Location should be at least 3 characters long!'
            print("Errloc2")  
              
        return errors

class CategoryManager(models.Manager):
    def category_validator(self, postData):
        errors = {}   
        jobCategory = postData['category'].strip()
    
        if (not jobCategory):
            errors['jobCategory_notExists'] = 'Job Category is a required field! Please select a value.'
            print("Errcategory1") 
        return errors


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)   
    email = models.CharField(max_length=255)
    password = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    creator = models.ForeignKey(User, related_name="creates")
    add = models.ManyToManyField(User, related_name="jobs")      
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = JobManager()

class Category(models.Model):
    title = models.CharField(max_length=255)
    job = models.ManyToManyField(Job, related_name="categories")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = CategoryManager()


