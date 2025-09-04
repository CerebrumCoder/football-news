from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406348282',
        'name': 'Neal Guarddin',
        'class': 'PBP A'
    }

    return render(request, "main.html", context)
