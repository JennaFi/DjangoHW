from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    return render(request, 'home_page.html')

def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        context = {'name': name, 'phone': phone}

        return render(request, 'feedback_form.html', context)
    return render(request, 'contacts.html')

