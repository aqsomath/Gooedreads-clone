from django.shortcuts import render
from books.models import Book

def landing_page(request):
    book1 =  Book.objects.get(id=1)
    book2 =  Book.objects.get(id=2)


    return render(request, "landing_page.html", {"book1":book1,
                                                 "book2":book2,


                                                 })