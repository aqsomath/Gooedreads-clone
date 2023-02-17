from django import forms
from books.models import BookReview, Book


class AddReviewForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = BookReview
        fields = ("stars_given", "comment")



class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "description","isbn","cover_picture")

class DeleteBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ("title", "description", "isbn", "cover_picture")
