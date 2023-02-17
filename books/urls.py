from django.urls import path
from .views import \
    BookListView, \
    BookDetailView, \
    AddReviewView, \
    AddBookView, \
    ConfirmDeleteBookView,\
    DeleteBookView, \
    ConfirmDeleteVReviewView,\
    DeleteReviewView,EditReviewView

# ,AddBookView,
# DeleteBookView, \

app_name="books"
urlpatterns = [
    path("list/", BookListView.as_view(), name="list"),
    path("<int:id>/", BookDetailView.as_view(), name="detail"),
    path("<int:id>/review", AddReviewView.as_view(), name="reviews"),
    path("create/", AddBookView.as_view(), name='create'),
    path("<int:id>/delete/confirm/", ConfirmDeleteBookView.as_view(), name="confirm"),
    path("<int:id>/delete/", DeleteBookView.as_view(), name="delete"),
    path("<int:book_id>/review/<int:review_id/delete/confirm/",
         ConfirmDeleteVReviewView.as_view(), name="delete-confirm"),
    path("<int:book_id>/review/<int:review_id>/delete/",DeleteReviewView.as_view(),name="delete-review"),
    path("<int:book_id>/review/<int:review_id>/edit", EditReviewView.as_view(), name="edit")



]