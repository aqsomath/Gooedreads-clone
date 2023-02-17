from django.test import TestCase
from django.urls import reverse

from books.models import Book


class BooksTestView(TestCase):
    def test_no_book(self):
        response = self.client.get(
            reverse("books:list")
        )

        self.assertContains(response, "No found book")


    def test_book_list(self):
        book1 = Book.objects.create(title="Book1", description="description1", isbn="12121121")
        book2 = Book.objects.create(title="Book2", description="description2", isbn="125544121")
        book3 = Book.objects.create(title="Book3", description="description3", isbn="121545421")

        response = self.client.get(
            reverse("books:list")
        )

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response =  self.client.get(reverse("books:list")+"?page=2")

        self.assertContains(response, book3.title)
        self.assertContains(response, book3.description)



    def test_book_detail(self):
        book = Book.objects.create(title="Book1", description="description1", isbn="12121121")
        response = self.client.get(
            reverse("books:detail", kwargs={"id":book.id})
        )

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)


