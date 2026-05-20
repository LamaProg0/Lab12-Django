from django.contrib import admin
from .models import Publisher, Author, Book
#from .models import Student, Address

#admin.site.register(Student)
#admin.site.register(Address)


admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(Book)
