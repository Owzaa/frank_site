from django.shortcuts import render
from datetime import date


def payments(request):
       
    year = date.today().year
    return render(request, 'apps/payments/payment.html',{'year':year})