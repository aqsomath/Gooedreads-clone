from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView

from books.forms import AddReviewForm, AddBookForm
from books.models import Book, BookReview


class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        search_query = request.GET.get("q","")
        if search_query:
            books = books.filter(title__icontains=search_query)
        pagination = Paginator(books,10)
        page_num = request.GET.get("page", 1)
        page_obj = pagination.get_page(page_num)
        return render(request, "books/list.html", {"page_obj":page_obj, "search_query":search_query})


class BookDetailView(View):
    def get(self,request, id):
        book = Book.objects.get(id=id)
        add_review = AddReviewForm()


        return render(request, "books/book_detail.html", {"book":book, "form":add_review})
#
# class PaginationBook(ListView):
#     model = Book
#     paginate_by = 2



class AddReviewView(LoginRequiredMixin,View):
   def post(self, request, id):
       book = Book.objects.get(id=id)
       add_review = AddReviewForm(data=request.POST)

       if add_review.is_valid():
           BookReview.objects.create(
               book = book,
               user = request.user,
               stars_given = add_review.cleaned_data["stars_given"],
               comment= add_review.cleaned_data["comment"]
           )

           return redirect(reverse("books:detail", kwargs={"id":book.id}))
       return render(request, "books/book_detail.html", {"form":add_review, "book":book})


class AddBookView(LoginRequiredMixin,View):
    def get(self,request):
        create_book = AddBookForm()
        return render(request, "books/create_book.html", {"create":create_book})
    def post(self,request):
        create_book = AddBookForm(data=request.POST)
        if create_book.is_valid():
            Book.objects.create(
                title = create_book.cleaned_data["title"],
                description = create_book.cleaned_data["description"],
                isbn = create_book.cleaned_data["isbn"],
                cover_picture = create_book.cleaned_data["cover_picture"]
            )
            return redirect("books:list")
        return render(request, "books/create_book.html", {"create": create_book})

class ConfirmDeleteBookView(LoginRequiredMixin,View):
    def get(self,request,id):
        book = Book.objects.get(id=id)
        return render(request,"books/confirm_delete.html", {"book":book})

class DeleteBookView(LoginRequiredMixin,View):
    def get(self,request, id):
        book = Book.objects.get(id=id)
        book.delete()
        return redirect(reverse("books:list",))

# class DeleteBookView(DeleteView):
#     model = Book
#     success_url = reverse_lazy("books:list")


class DeleteReviewView(LoginRequiredMixin,View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review.delete()
        return redirect(reverse("books:detail",kwargs={"id":book_id} ))



class ConfirmDeleteVReviewView(LoginRequiredMixin, View):
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        return render(request, "books/confirm_review_delete.html", {"book":book, "review":review})


class EditReviewView(LoginRequiredMixin,View):
    def get(self,request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = AddReviewForm(instance=review)
        return render(request, "books/edit_review.html", { "review_form":review_form,"review":review, "book":book})
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form = AddReviewForm(instance=review, data=request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect(reverse("books:detail", kwargs={"id":book.id}))
        return render(request, "books/edit_review.html", { "review_form":review_form,"review":review, "book":book})








