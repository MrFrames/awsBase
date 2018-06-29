from django.shortcuts import render
from django.views import generic
from .models import post, meetUp,section, place, pastData
import json
from django.http import HttpResponse
from .coords import haversine
from datetime import datetime
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.

def comb(request):
    print("Fetching ben's stuff...")
    print("posts:")
    all_posts = post.objects.all().filter(show=True)

    post_count = len(list(all_posts))
    pull = 3 if len(all_posts) > 3 else len(all_posts)
    last3posts = list(all_posts)[len(all_posts)-pull:]
    last3posts.reverse()
    print(last3posts)
    print("posts: " + str(last3posts))

    all_meetUps = meetUp.objects.all()
    print("meetUps:")
    for meet in all_meetUps:
        print(meet.name)

    sorted_places = place.objects.order_by('section').order_by('order')
    print(str(type(sorted_places)))

    # List of all posts:

    posts_raw = [[pos.place.lat, pos.place.lon, pos.title] for pos in
                 all_posts]

    allPosts_json = json.dumps(posts_raw)

    # List of all meetups:

    meetUps_raw = [[meet.place.lat, meet.place.lon, meet.name] for
                   meet in all_meetUps]

    allMeetUps_json = json.dumps(meetUps_raw)

    # JSON  with data broken up by section, poly to be used for poly lines,
    # route to be used for routing.

    sections = section.objects.all()

    polySectionNames = ["Boat","Plane","Train"]
    poly_sections = [i for i in sections if i.type.name in polySectionNames]
    poly_sectionsJson = get_section_json(poly_sections)

    route_sections = [i for i in sections if i.type.name == "Bicycle"]
    route_sectionJson = get_section_json(route_sections)



    full_route = []

    context = {
        '3posts': last3posts,
        'post_count': post_count,
        'full_route': full_route,
        'all_posts': allPosts_json,
        'all_meetUps' : allMeetUps_json,
        'sections_json' : route_sectionJson,
        'poly_sectionsJson' : poly_sectionsJson
    }

    template = "tracking/comb.html"

    return render(request, template, context)

def ext(request):
    data = list(pastData.objects.all())
    ext_data_list(data)
    return HttpResponse("Updated data")

def input(request):

    lat = request.GET['lat']
    lng = request.GET['lng']
    time = request.GET['time']

    row_instance = pastData(lat=lat,lon=lng,time=time)
    row_instance.save()

    data_objects = list(pastData.objects.all())

    if len(data_objects)>1:
        lastCoord = list(data_objects)[-2]
        print (lastCoord.time)

    print("{},{} recorded at: {}".format(lat,lng,time))
    return HttpResponse("Hello world!")

def postList(request):
    queryset = list(post.objects.all().filter(show=True))
    pk_list = [x.pk for x in queryset]
    print(pk_list)
    id = int(request.GET.get('pk'))

    print("pk: " + str(id))

    current_post = post.objects.all().get(pk=id)
    current_index = pk_list.index(id)
    next_pk, prev_pk = 0,0
    if current_index+1 < len(queryset):
        next_pk = pk_list[current_index+1]
    if current_index != 0:
        prev_pk = pk_list[current_index-1]

    print ("next: " + str(next_pk))
    context = {
        "post" : current_post,
        "next" : next_pk,
        "prev" : prev_pk
    }

    return render(request, "tracking/blog.html", context)

@login_required(login_url='')
def dash(request):
    last_data = list(pastData.objects.all())[-1]
    movingTime = last_data.totalMovingTime
    distance = last_data.totalDistance/1000
    if movingTime == 0:
        movingTime = 1
    averageSpeed= (distance/movingTime)*3600
    #saveStatus is passed into the html to give a notification that the save
    # was successful.
    saveStatus = 0
    cur_post = 0
    if request.method == 'POST':
        print(request.POST['placePk'])
        saveStatus = savePost(request,
                              int(request.POST['placePk']),
                              int(request.POST['postPk']))
        post_in =0
    else:
        try:
            pk = request.GET['postPk']

            cur_post = list(post.objects.all().filter(pk=int(pk)))[0]
            post_in = 1
        except:
            post_in = 0

    print(post_in)
    print(saveStatus)
    context = {
        "movingTime": movingTime,
        "distance": distance,
        "averageSpeed": averageSpeed,
        "saved" : saveStatus,
        "post_in" : post_in,
        "post" : cur_post
    }
    template = "tracking/dashboard.html"

    return render(request,template,context)

def savePost(request,placePk,postPk):
    saveStatus = 0
    #try:
    if placePk != 0:
        newPlace = list(place.objects.all().filter(pk=placePk))[0]
    else:
        newPlace = place()
    newPlace.name=request.POST['name']
    newPlace.lat=request.POST['lat']
    newPlace.lon=request.POST['lng']
    newPlace.order=1
    print("created place instance")
    newPlace.save()
    saveStatus = "Place saved OK."
    #    try:
    setPlace = list(place.objects.all().filter(name=request.POST['name']))[0]
    print("setPlace: " + setPlace.name)
    if postPk != 0:
        newPost = list(post.objects.all().filter(pk=postPk))[0]
    else:
        newPost = post()
    print("newPost: " + newPost.title)
    print(request.FILES.get('filepath', False))
    if 'pic' in request.FILES:
        newPost.image=request.FILES['pic']
    newPost.title=request.POST['post_title']
    newPost.content=request.POST['post_content']
    newPost.show=True
    newPost.place=setPlace
    print("ok up to save...")
    newPost.save()
    saveStatus = saveStatus + ", post saved OK."
    #    except:
    saveStatus = saveStatus + ", error saving post!"
    #except:
    saveStatus = "Error saving place!"
    return saveStatus

def postView(request):
    template = "tracking/allPosts.html"

    posts = list(post.objects.all())

    context ={
        "all_posts" : posts
    }

    return render(request,template,context)


def get_section_json(sections):
    json_dict = {}
    for sec in sections:
        # Each section has a key in the dict/json.
        # Constructs list of place coordinates in format google maps can interpret
        # with the key 'places'
        json_dict[sec.name] = {"color":sec.type.color}
        json_dict[sec.name]['transportMethod'] = sec.type.name
        placeObjList = list(sec.place_set.all().order_by('order'))

        startPlace = placeObjList.pop(placeObjList.index(sec.startPlace))
        json_dict[sec.name]["start"] = {"lat":startPlace.lat,
                                        "lng":startPlace.lon}
        endPlace = placeObjList.pop(placeObjList.index(sec.endPlace))
        json_dict[sec.name]["end"] = {"lat":endPlace.lat,
                                        "lng":endPlace.lon}
        placeList = [{"lat":i.lat,"lng":i.lon} for i in placeObjList]

        json_dict[sec.name]["places"] = placeList

        # Same with posts for each section
        postList = []


        '''
        #adds posts to json, needs logic to handle 'no image'
        for pla in placeObjList:
            placePosts = list(pla.postPlace.all())
            postList = postList + placePosts
        postList = [[pos.place.lat,
                     pos.place.lon,
                     pos.title,
                     pos.image.url,
                     pos.content] for pos in postList]

        json_dict[sec.name]["posts"] = postList
        '''

        # Same for meetUps for each section

        meetList = []
        for pla in placeObjList:
            placeMeetUps = list(pla.meetUpPlace.all())
            meetList = meetList + placeMeetUps
        meetList = [[meetUp.place.lat,
                     meetUp.place.lon,
                     meetUp.name] for
                    meetUp in meetList]

        json_dict[sec.name]["meetUps"] = meetList

    return json.dumps(json_dict)

def ext_data_list(dataObjList):
    data = dataObjList
    for i in range(1,len(data)):
        row0 = data[i-1]
        row1 = data[i]
        ext_data(row0,row1)

def ext_data(dataObj0,dataObj1):
    '''
    Extrapolates data from previous time step for summary in dashboard.
    ToDo:
      > Add google maps distance, logic to use point to point distance if
        google maps fails.

      > Vary 'add to total distance' cutoff based on position accuracy
    '''
    p0 = (dataObj0.lat, dataObj0.lon)
    p1 = (dataObj1.lat, dataObj1.lon)
    # Gets time difference in seconds:
    time = get_dif(dataObj0.time, dataObj1.time)
    # Gets point to point distance:
    distanceAB = haversine(p0, p1) * 1000
    # Gets distance from google maps:
    dyn_distance = get_google_distance(p0, p1)
    # Gets speed in m/s:
    speed = distanceAB / time
    # If speed is less than 2.5m/s, doesn't register as moving time:
    if speed > 2.5:
        movingTime = time
        movingDistance = distanceAB
    else:
        movingTime = 0
        movingDistance = 0
    # Adds moving time to total moving time count:
    totalMovingTime = dataObj0.totalMovingTime + movingTime

    totalDistance = dataObj0.totalDistance + movingDistance
    # Assigns values to the data objects:
    dataObj1.deltaT = time
    dataObj1.distanceAB = distanceAB
    dataObj1.speed = speed
    dataObj1.movingTime = time
    dataObj1.totalMovingTime = totalMovingTime
    dataObj1.totalDistance = totalDistance

    # Saves the new extrapolated data:
    dataObj1.save()

def get_dif(dateTimeObj1, dateTimeObj2):

    return (dateTimeObj2-dateTimeObj1).total_seconds()

def get_google_distance(point1,point2):
    return 0
