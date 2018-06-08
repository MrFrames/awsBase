from django.shortcuts import render
from django.views import generic
from .models import pastData, get_past_data, add_data, section, place

# Create your views here.

#def get_places():


class homeView(generic.ListView):
    #new_data = get_past_data()
    #add_data(new_data)
    model = section
    template_name = 'tracking/index.html'
    '''
    def get_queryset(self):
        return section.objects.all()
    '''

def homeView2(request):
    sections = section.objects.all()
    sorted_places = place.objects.order_by('order')

    '''
    for sec in sections:
        section_places = sorted_places.objects.filter(section = sec)
        context[sec.name] = sorted_list
    '''

    first_section = section.objects.all().filter(pk = 1)[0]
    section2 = first_section.place_set.all()

    #start_place = first_section.startPlace
    context = {
        'sections': sections,
        'places' : sorted_places
    }

    template = "tracking/index.html"
    return render(request, template, context)
