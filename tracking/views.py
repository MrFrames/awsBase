from django.shortcuts import render
from django.views import generic
from .models import pastData, get_past_data, add_data

# Create your views here.

class homeView(generic.ListView):
    #new_data = get_past_data()
    #add_data(new_data)
    template_name = 'tracking/index.html'
    def get_queryset(self):
        return pastData.objects.all()