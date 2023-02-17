from django.contrib import admin

from .models import Book,BookReview,BookAuthor,Author


class BookAdmin(admin.ModelAdmin):
    search_fields = ("title", "isbn")
    list_display = ('title', 'isbn', 'description')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")
    search_fields = ("first_name","last_name")


class BookAuthorAdmin(admin.ModelAdmin):
    pass


class BookReviewAdmin(admin.ModelAdmin):
    pass



admin.site.register(Book, BookAdmin)
admin.site.register(BookAuthor,BookAuthorAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(BookReview,BookReviewAdmin)

