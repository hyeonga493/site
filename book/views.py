from django.shortcuts import render, redirect
from .models import Book
#_  im = bool(request.POST.get("impo"))

def index(request):
    b = request.user.book_set.all()
    context = {
        'b' : b
    }
    return render(request, 'book/index.html', context)

def create(request):
    if request.method == "POST":
        sn = request.POST.get('sname')
        su = request.POST.get('surl')
        sc = request.POST.get('scon')
        im = bool(request.POST.get('impo'))
        Book(site_name=sn, site_url=su, site_con=sc, impo=im, user=request.user).save()
        return redirect('book:index')
    return render(request, 'book/create.html')
