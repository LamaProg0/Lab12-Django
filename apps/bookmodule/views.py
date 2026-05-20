from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.db.models import Q
from django.db.models import Count, Sum, Avg, Max, Min, F, FloatField, ExpressionWrapper
from django.db.models import Count
from .models import Publisher, Author, Book
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BookForm
from .models import Address, Student, Student2
from .forms import StudentForm, Student2Form
from .models import Member
from .forms import MemberForm
from django.contrib.auth.forms import UserCreationForm



def index(request):
    return render(request, "bookmodule/index.html")
 
def list_books(request):
    return render(request, 'bookmodule/list_books.html')
 
def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')
 
def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def links_view(request):
    return render(request, 'bookmodule/links.html')

def formatting_view(request):
    return render(request, 'bookmodule/formatting.html')

def listing_view(request):
    return render(request, 'bookmodule/listing.html')

def tables_view(request):
    return render(request, 'bookmodule/tables.html')

def search_view(request):
    if request.method == "POST":
        string = request.POST.get('keyword').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        # now filter
        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower(): contained = True
            if not contained and isAuthor and string in item['author'].lower():contained = True
            
            if contained: newBooks.append(item)
        return render(request, 'bookmodule/bookList.html', {'books':newBooks})
    return render(request, 'bookmodule/search.html')
 

def __getBooksList():
    book1 = {'id':12344321, 'title':'Continuous Delivery', 'author':'J.Humble and D. Farley'}
    book2 = {'id':56788765,'title':'Reversing: Secrets of Reverse Engineering', 'author':'E. Eilam'}
    book3 = {'id':43211234, 'title':'The Hundred-Page Machine Learning Book', 'author':'Andriy Burkov'}
    return [book1, book2, book3]
 
def simple_query(request):
    mybooks=Book.objects.filter(title__icontains='and') # <- multiple objects
    return render(request, 'bookmodule/bookList.html', {'books':mybooks})

def complex_query(request):
    mybooks=books=Book.objects.filter(author__isnull = False).filter(title__icontains='and').filter(edition__gte = 2).exclude(price__lte = 100)[:10]
    if len(mybooks)>=1:
        return render(request, 'bookmodule/bookList.html', {'books':mybooks})
    else:
        return render(request, 'bookmodule/index.html')

def task1_view(request):

    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'books/task1.html', {'books': books})

def task2_view(request):
  
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'books/task2.html', {'books': books})

def task3_view(request):
   
    books = Book.objects.filter(
        ~Q(edition__gt=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'books/task3.html', {'books': books})

def task4_view(request):
   
    books = Book.objects.all().order_by('title')
    return render(request, 'books/task4.html', {'books': books})

def task5_view(request):
  
    results = Book.objects.aggregate(
        total_count=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        maximum_price=Max('price'),
        minimum_price=Min('price')
    )
    return render(request, 'books/task5.html', {'res': results})

#def task7_view(request):
    #cities = Address.objects.annotate(num_students=Count('student'))
    #return render(request, 'books/task7.html', {'cities': cities})

def Lab9task1(request):
  
    total_quantity = Book.objects.aggregate(total=Sum('quantity'))['total'] or 1
    
    books = Book.objects.annotate(
        availability_pct=ExpressionWrapper(
            (F('quantity') * 100.0) / total_quantity, 
            output_field=FloatField()
        )
    )
  
    return render(request, 'books/Lab9/Lab9task1.html', {'books': books})


def Lab9task2(request):
   
    publishers = Publisher.objects.annotate(total_stock=Sum('book__quantity'))
    return render(request, 'books/Lab9/Lab9task2.html', {'publishers': publishers})

def Lab9task3(request):

    publishers = Publisher.objects.annotate(oldest_book_date=Min('book__pubdate'))
    return render(request, 'books/Lab9/Lab9task3.html', {'publishers': publishers})

def Lab9task4(request):
 
    publishers = Publisher.objects.annotate(
        avg_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price')
    )
    return render(request, 'books/Lab9/Lab9task4.html', {'publishers': publishers})

def Lab9task5(request):
 
    publishers = Publisher.objects.annotate(
        high_rated_books=Count('book', filter=Q(book__rating__gte=4))
    )
    return render(request, 'books/Lab9/Lab9task5.html', {'publishers': publishers})

def Lab9task6(request): 
    
    publishers = Publisher.objects.annotate(
        filtered_books=Count('book', filter=Q(book__price__gt=50, book__quantity__gte=1, book__quantity__lte=5))
    )
    return render(request, 'books/Lab9/Lab9task6.html', {'publishers': publishers})

def listbooks_part1(request):
    books = Book.objects.all()
    return render(request, 'books/listbooks_part1.html', {'books': books})

def addbook_part1(request):
    if request.method == 'POST':
        book_title = request.POST.get('title')
        author_name = request.POST.get('author')       
        new_book = Book.objects.create(title=book_title)   
        author_obj, created = Author.objects.get_or_create(name=author_name)
        new_book.author.add(author_obj)

        return redirect('listbooks_part1')   
    return render(request, 'books/addbook_part1.html')
    
def editbook_part1(request, id):
    book = Book.objects.get(id=id)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.save()       
        author_name = request.POST.get('author')
        author_obj, created = Author.objects.get_or_create(name=author_name)
        book.author.set([author_obj])      
        return redirect('listbooks_part1')
    
    return render(request, 'books/editbook_part1.html', {'book': book})

def deletebook_part1(request, id):
    book = Book.objects.get(id=id)

    if request.method == 'POST':
        book.delete() 
        return redirect('listbooks_part1') 
    return render(request, 'books/deletebook_part1.html', {'book': book})

def listbooks_part2(request):
    books = Book.objects.all()
    return render(request, 'books/listbooks_part2.html', {'books': books})

def addbook_part2(request):
    if request.method == 'POST':
        form = BookForm(request.POST) 
        if form.is_valid():
            form.save() 
            return redirect('listbooks_part2')
    else:
        form = BookForm()    
    return render(request, 'books/addbook_part2.html', {'form': form})

def editbook_part2(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save() 
            return redirect('listbooks_part2')
    else:
        form = BookForm(instance=book)  
    return render(request, 'books/editbook_part2.html', {'form': form})

def deletebook_part2(request, id):
    book = Book.objects.get(id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('listbooks_part2')   
    return render(request, 'books/deletebook_part2.html', {'book': book})


def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})

def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_form.html', {'form': form, 'title': 'Add Student'})

def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_form.html', {'form': form, 'title': 'Update Student'})

def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.delete()
        return redirect('student_list')
    return render(request, 'student_confirm_delete.html', {'student': student})

def student2_list(request):
    students = Student2.objects.all()
    return render(request, 'student2_list.html', {'students': students})

def add_student2(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/books/students2/')
    else:
        form = Student2Form()
    return render(request, 'student2_form.html', {'form': form, 'title': 'Add Student (Task 2)'})

def update_student2(request, pk):
    student = get_object_or_404(Student2, pk=pk)
    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/books/students2/')
    else:
        form = Student2Form(instance=student)
    return render(request, 'student2_form.html', {'form': form, 'title': 'Update Student (Task 2)'})

def delete_student2(request, pk):
    student = get_object_or_404(Student2, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/books/students2/')
    return render(request, 'student2_confirm_delete.html', {'student': student})

def member_list(request):
    members = Member.objects.all()
    return render(request, 'member_list.html', {'members': members})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else:
        form = MemberForm()
    return render(request, 'member_form.html', {'form': form})

