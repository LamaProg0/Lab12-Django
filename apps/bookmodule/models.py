from django.db import models

#class Book(models.Model):
    #title = models.CharField(max_length = 50)
    #author = models.CharField(max_length = 50)
    #price = models.FloatField(default = 0.0)
    #edition = models.SmallIntegerField(default = 1)


class Address(models.Model):
    city = models.CharField(max_length=100) 
    def __str__(self):
        return self.city

class Student(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField() 
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Address2(models.Model):
    city = models.CharField(max_length=100) 
    def __str__(self):
        return self.city

class Student2(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField() 
    addresses = models.ManyToManyField(Address2)
    def __str__(self):
        return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)

class Author(models.Model):
    name = models.CharField(max_length=200)
    DOB = models.DateField(null=True)

class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=1)
    pubdate = models.DateTimeField(null=True, blank=True)
    rating = models.SmallIntegerField(default=1)
    publisher = models.ForeignKey(Publisher, null=True, on_delete=models.SET_NULL)
    author= models.ManyToManyField(Author)
    edition = models.SmallIntegerField(default = 1)


class Member(models.Model):
    name = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='members/')

    def __str__(self):
        return self.name
    