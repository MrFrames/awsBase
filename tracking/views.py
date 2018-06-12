from django.shortcuts import render
from django.views import generic
from .models import pastData, get_past_data, add_data, section, place
import json

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

def ben(request):
    print("Fetching ben's stuff...")
    sections = section.objects.all()
    sorted_places = place.objects.order_by('section').order_by('order')
    print(str(type(sorted_places)))

    # Function Below constructs a json object to pass to the main website.

    json_dict = {}

    for sec in sections:
        json_dict[sec.name] = {"color":sec.color}
        placeObjList = list(sec.place_set.all().order_by('order'))
        placeNameList = [place.name for place in placeObjList]
        placeList = [[i.name,i.lat,i.lon] for i in placeObjList]

        if not sec.startPlace.name in placeNameList:
            startData = [sec.startPlace.name,
                         sec.startPlace.lat,
                         sec.startPlace.lon]
            placeList = [startData] + placeList
        if not sec.endPlace.name in placeNameList:
            endData = [sec.endPlace.name,
                         sec.endPlace.lat,
                         sec.endPlace.lon]
            placeList.append(endData)
        json_dict[sec.name]["places"] = placeList
    print(json_dict)

    json_obj = json.dumps(json_dict)

    first_section = section.objects.all().filter(pk = 1)[0]
    section2 = first_section.place_set.all()

    context = {
        'sections': sections,
        'places' : sorted_places,
        'sorted_json' : json_obj
    }

    template = "tracking/index.html"

    return render(request, template, context)



def geo(request):
    print("Fetching Georgia's stuff...")
    context = {}
    template = "tracking/Geo.html"
    return render (request, template, context)


def comb(request):
    print("Fetching ben's stuff...")
    sections = section.objects.all()
    sorted_places = place.objects.order_by('section').order_by('order')
    print(str(type(sorted_places)))

    # Function Below constructs a json object to pass to the main website.

    json_dict = {}

    for sec in sections:
        json_dict[sec.name] = {"color":sec.color}
        placeObjList = list(sec.place_set.all().order_by('order'))
        placeNameList = [place.name for place in placeObjList]
        placeList = [[i.name,i.lat,i.lon] for i in placeObjList]

        if not sec.startPlace.name in placeNameList:
            startData = [sec.startPlace.name,
                         sec.startPlace.lat,
                         sec.startPlace.lon]
            placeList = [startData] + placeList
        if not sec.endPlace.name in placeNameList:
            endData = [sec.endPlace.name,
                         sec.endPlace.lat,
                         sec.endPlace.lon]
            placeList.append(endData)
        json_dict[sec.name]["places"] = placeList
    print(json_dict)

    json_obj = json.dumps(json_dict)

    first_section = section.objects.all().filter(pk = 1)[0]
    section2 = first_section.place_set.all()

    context = {
        'sections': sections,
        'places' : sorted_places,
        'sorted_json' : json_obj
    }

    template = "tracking/comb.html"

    return render(request, template, context)
