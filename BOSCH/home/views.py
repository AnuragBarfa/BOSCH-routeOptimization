from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request,'home.html')

def mapView(request):
	return render(request,'mapView.html')
