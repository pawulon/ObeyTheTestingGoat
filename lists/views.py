from django.shortcuts import render
from django.shortcuts import redirect
from lists.models import Item

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')                
    
    return render(request, 'home.html')
                  