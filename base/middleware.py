from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime

def due_date_middleware(get_response):
    def middleware(request):
        response = get_response(request)

        if request.user.is_authenticated:
            today = datetime.now().date()
            due_date = request.user.due_date

            if request.user.is_dued:
                return render(request, 'subs.html')
            if today == due_date:
                u = User.objects.get(username=request.user.username)
                u.is_dued = True
                return render(request, 'subs.html')

        return response

    return middleware
