from django import forms
from .models import Book

class BookForm(forms.ModelForm):
	
	class Meta:
		model = Book
		fields = ('location','no_of_students', )