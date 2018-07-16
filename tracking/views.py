from django.shortcuts import render
from django.views import generic
from .models import post, meetUp,section, place, pastData, resolved_coord, \
    capped_resolved_coord,type
import json
from django.http import HttpResponse
from .coords import haversine
import datetime
import requests
import re
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .Section_division import *
import ast
import random as rand
from django.core.mail import send_mail

send_mail('subject', 'body of the message', 'sender@example.com', ['receiver1@example.com', 'receiver2@example.com'])

# Create your views here.

def email(request):
    '''
    Constructs, and sends an email from a post request on the home page.

    returns status to be passed to the email template.
    '''

    name = request.POST.get("name")
    content = request.POST.get("email_content")
    section = request.POST.get("section")

    try:
        first_line = "{} clicked on the section: {}, message below:<br>".format(
            name,section)
        content = first_line + content
        print(content)
        send_mail("Message from {}, sent from browngirlonabike.com!".format(name),
                  first_line,
                  "Farhas.robot.butler@browngirlonabike.com",
                  ["benstorey0@gmail.com"],
                  html_message=content)
        status = "Email sent successfully"
    except:
        status = "Email failed"

    template = 'tracking/email.html'

    context = {"status" : status}

    return render(request,template,context)

def not_capped(request):
    return index(request, 0)

def capped(request):
    return index(request, 24)

def index(request, behind):

    all_posts = post.objects.all().filter(show=True)

    # Get's the last 3 posts for displaying on the site.

    post_count = len(list(all_posts))
    pull = 3 if len(all_posts) > 3 else len(all_posts)
    last3posts = list(all_posts)[len(all_posts)-pull:]
    last3posts.reverse()

    all_meetUps = meetUp.objects.all()

    sorted_places = place.objects.order_by('section').order_by('order')

    # List of all posts, with relevant data for positioning on map.

    posts_raw = [[pos.place.lat,
                  pos.place.lon,
                  pos.title,
                  pos.time.strftime('%d/%m/%Y'),
                  pos.content.split('.')[0],
                  pos.image.url,
                  pos.pk] for pos in all_posts if pos.image]

    allPosts_json = json.dumps(posts_raw)

    # List of all meetups:

    meetUps_raw = [[meet.place.lat, meet.place.lon, meet.name] for
                   meet in all_meetUps]

    allMeetUps_json = json.dumps(meetUps_raw)

    '''
    JSON  with data broken up by section, poly to be used for poly lines,
    route to be used for routing.
    '''

    sections = section.objects.all()

    polySectionNames = ["Boat","Plane","Train"]
    poly_sections = [i for i in sections if i.type.name in polySectionNames]
    poly_sectionsJson = get_section_json(poly_sections)

    route_sections = [i for i in sections if i.type.name == "Cycling"]
    print("Route sections:")
    print(route_sections)
    route_sectionJson = get_section_json(route_sections)

    hist_sections_json = json.dumps(get_hist_Sections(behind))


    context = {
        '3posts': last3posts,
        'post_count': post_count,
        'all_posts': allPosts_json,
        'all_meetUps' : allMeetUps_json,
        'sections_json' : route_sectionJson,
        'poly_sectionsJson' : poly_sectionsJson,
        'hist_section_array' : hist_sections_json
    }

    template = "tracking/index.html"

    return render(request, template, context)

def get_hist_Sections(delayed):
    '''
    Returns historical sections (those constructed from actual position data)

    Delayed represents weather delayed historical data, or current data will be returned.

    For info on resolved coords, see the section_division.py file.
    '''
    if delayed:
        history_section_data = capped_resolved_coord.objects.all()
    else:
        history_section_data = resolved_coord.objects.all()

    # Tries each assending integer as a section number until the query
    # returns an empty list. On each loop, adds the list of resolved_coord
    # objects to sec_list
    remaining = True
    count = 0
    sec_list = []
    while remaining:
        sec = list(history_section_data.filter(section=count))
        print(count)
        if len(sec) == 0:
            remaining = False
        else:
            sec_list.append(sec)
            count += 1

    # Converts the list into coords that google maps can interperate.
    sec_list = [[{"lat": x.lat, "lng": x.lon} for x in sec] for sec in
                sec_list]

    hist_sections = {}

    '''
    Removes the start and end coords, as these need special designation in
    the maps JavaScript api.
    '''
    for i in range(0, len(sec_list)):
        start = sec_list[i].pop(0)
        end = sec_list[i].pop(-1)
        hist_sections[i] = {"start": start, "end": end, "places": sec_list[i]}

    return hist_sections

def postList(request):
    '''
    Passes all relevant data to a blog post, as well as the pk for the next
    and previous posts for navigation to the blog view.

    Get's list of vars, and gets the requesed posts pk's position in
    that list, assigned to current_index.
    '''

    queryset = list(post.objects.all().filter(show=True))
    pk_list = [x.pk for x in queryset]
    id = int(request.GET.get('pk'))
    current_post = post.objects.all().get(pk=id)
    current_index = pk_list.index(id)

    '''
    checks if next and previous pk's exist, and assigns them to vars if 
    they do, 0 indicates that it doesn't
    '''
    next_pk, prev_pk = 0,0
    if current_index+1 < len(queryset):
        next_pk = pk_list[current_index+1]
    if current_index != 0:
        prev_pk = pk_list[current_index-1]

    context = {
        "post" : current_post,
        "next" : next_pk,
        "prev" : prev_pk
    }

    return render(request, "tracking/blog.html", context)

@login_required(login_url='')
def dash(request):
    '''
    Handles logic and context input for the site dashboard.
    '''

    # Last position used to center maps on the riders last position.
    last_data = list(pastData.objects.all())[-1]
    lat = last_data.lat
    lng = last_data.lon

    lastPosForJson = {"lat":lat,"lng":lng}
    lastPos = json.dumps(lastPosForJson)

    #Simple data in for the stats tab:
    movingTime = last_data.totalMovingTime
    distance = last_data.totalDistance/1000
    elevation = last_data.totalElevation
    if movingTime == 0:
        movingTime = 1
    averageSpeed= (distance/movingTime)*3600

    #Data formating for stats tab:

    seconds = movingTime % 60
    tot_minutes = int(movingTime / 60)
    minutes = tot_minutes % 60
    tot_hours = int(tot_minutes / 60)
    hours = tot_hours % 24
    days = int(tot_hours / 24)

    movingTime = "{} days, {} hours, {} minutes and {} seconds".format(days,
                                                                       hours,
                                                                       minutes,
                                                                       seconds)
    distance = "{0:.2f} km".format(distance)
    if elevation > 3000:
        elevation = "{0:.2f} km".format(elevation / 1000)
    else:
        elevation = str(int(elevation)) + " m"
    averageSpeed = "{0:.2f} km/h".format(averageSpeed)

    '''
    Below handles logic for different returns after form inpust: meetup, 
    blog posts, and map sections.
    
    saveStatus is passed into the html to give a notification that a save
    was successful.
    '''
    post_in = 0
    saveStatus = 0
    if request.method == 'POST':
            print(request.POST.get('meet up'))
            if request.POST.get('meet up'):
                saveStatus = saveMeetUp(request)
                post_in = 0
            elif request.POST.get('start'):
                saveSection (request)
            else:
                saveStatus = savePost(request)
                post_in = 0

    '''
    Gets a json of all posts, used to select posts from a dropdown menu in
    the blog post tab.
    '''
    all_posts_json = get_postsJson()


    context = {
        "movingTime": movingTime,
        "distance": distance,
        "averageSpeed": averageSpeed,
        "elevation" : elevation,
        "saved" : saveStatus,
        "post_in" : post_in,
        "posts": all_posts_json,
        "lastPos" : lastPos
    }
    template = "tracking/dashboard.html"

    return render(request,template,context)

def get_postsJson():
    '''
    Constructs a json containing all relevant data for each blog post,
    the first order of keys are the post titles, and the lower structure can be
    seen in definition of inner_dict below:
    '''
    all_posts = list(post.objects.all())
    post_dict = {}

    for pos in all_posts:
        place_pk = pos.place.pk
        place_name = pos.place.name
        lat = pos.place.lat
        lng = pos.place.lon

        post_pk = pos.pk
        title = pos.title
        content = pos.content

        if pos.image:
            image_url = pos.image.url
        else:
            image_url = "No image saved"

        inner_dict = {"coord":{"lat":lat,"lng":lng},
                      "placePk": place_pk,
                      "place_name": place_name,
                      "postPk": post_pk,
                      "content": content,
                      "image": image_url}

        post_dict[title] = inner_dict

    return json.dumps(post_dict)

def saveSection(request):
    '''
    Saves a section from incoming post data.
    variables passed in are js objects converted into strings,
    to be converted back into python dictionaries for parsing.
    '''

    secName = request.POST.get('Section name')
    start = request.POST.get('start')
    end = request.POST.get('end')
    waypoints = request.POST.get('waypoints')

    # Converts to dictionaries:
    start_dict = ast.literal_eval(start)
    end_dict = ast.literal_eval(end)
    waypoint_dict = ast.literal_eval(waypoints)

    # Existing names list is obtained to make sure that no two places have
    # the same name once saved, names are a random integer under 1,000,000.
    existing_names = [i.name for i in list(place.objects.all())]

    # saves start/end place
    name = rand.randrange(0,1000000)
    while name in existing_names:
        name = rand.randrange(0,1000000)
    start = place(name = str(name),
                  lat = start_dict.get('lat'),
                  lon = start_dict.get('lng'),
                  order = 1)
    start.save()

    existing_names.append(name)

    while name in existing_names:
        name = rand.randrange(0,1000000)

    end = place(name=str(name),
                lat=end_dict.get('lat'),
                lon=end_dict.get('lng'),
                order=1)
    end.save()

    # sets the section with the start and end places and the waypoints.

    cycling = type.objects.get(name="Cycling")

    sec = section(name = secName,
                  startPlace = start,
                  endPlace = end,
                  type = cycling)
    sec.save()

    # Waypoints must each be saved as places, then assigned the section
    # saved above to their section many-to-many field.
    for key in waypoint_dict.keys():
        waypoint = ""
        name = rand.randrange(0, 1000000)
        while name in existing_names:
            name = rand.randrange(0, 1000000)
        wayCoord = waypoint_dict[key]
        lat = wayCoord.get("lat")
        lng = wayCoord.get("lng")
        waypoint = place(name = str(name),
                         lat = lat,
                         lon = lng,
                         order = 1)
        waypoint.save()
        waypoint.section.add(sec)





    # set places to section

def saveMeetUp(request):
    '''
    Saves a meet up place by first saving the incoming place & then
    assigning that to the meetup's place foreign key field.
    '''
    newPlace = place()
    newPlace.name = request.POST['name']
    newPlace.lat = request.POST['lat']
    newPlace.lon = request.POST['lng']
    newPlace.order = 1
    newPlace.save()

    newMeet = meetUp()
    newMeet.name = request.POST['name']
    newMeet.info = request.POST['post_content']
    newMeet.show = True
    newMeet.place = newPlace

    newMeet.save()
    return ("saved new meetup place!")

def savePost(request):
    '''
    Saves a post, by first saving the incomming place first, then assigning
    the place to the post's foreign key field.
    '''

    placePk = int(request.POST['placePk'])
    postPk = int(request.POST['postPk'])

    if placePk != 0:
        newPlace = place.objects.get(pk=placePk)
    else:
        newPlace = place()

    newPlace.name=request.POST['name']
    newPlace.lat=request.POST['lat']
    newPlace.lon=request.POST['lng']
    newPlace.order=1
    newPlace.save()

    setPlace = place.objects.get(name=request.POST['name'])

    if postPk != 0:
        newPost = post.objects.get(pk=postPk)
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
    newPost.save()

    return "Saved ok!"

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


'''
Functions below are for extrapolating velocity, altitude etc from raw data. 
ext_data_list acts on all objects in the database, calling on ext_data, 
which acts on a table entry and it's previous entry to calculate relevant 
data.
'''

def ext(request):
    # Simple view to call the extrapolate data function below
    data = list(pastData.objects.all())
    ext_data_list(data)
    return HttpResponse("Updated data")

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

      > Add is_over_water, to weed out boat paths
    '''
    p0 = (dataObj0.lat, dataObj0.lon)
    p1 = (dataObj1.lat, dataObj1.lon)

    # Gets time difference in seconds:
    elevation = get_elevation(p1[0],p1[1])

    time = get_dif(dataObj0.time, dataObj1.time)
    # Gets point to point distance:
    distanceAB = haversine(p0, p1) * 1000

    overWater = False
    if distanceAB > 10000:
        overWater = over_water(p0,p1)

    # Gets distance from google maps:
    dyn_distance = get_google_distance(p0, p1)
    # Gets speed in m/s:
    speed = distanceAB / time
    # If speed is less than 2.5m/s, doesn't register as moving time:
    if speed > 2.5 and speed < 17.5  and not overWater:
        movingTime = time
        movingDistance = distanceAB
    else:
        movingTime = 0
        movingDistance = 0
    # Adds moving time to total moving time count:
    totalMovingTime = dataObj0.totalMovingTime + movingTime

    totalDistance = dataObj0.totalDistance + movingDistance

    delta_elevation = dataObj1.elevation - dataObj0.elevation

    if delta_elevation > 0:
        totalElevation = dataObj0.totalElevation + delta_elevation
    else:
        totalElevation = dataObj0.totalElevation
    # Assigns values to the data objects:
    dataObj1.elevation = elevation
    dataObj1.deltaT = time
    dataObj1.distanceAB = distanceAB
    dataObj1.speed = speed
    dataObj1.movingTime = time
    dataObj1.totalMovingTime = totalMovingTime
    dataObj1.totalDistance = totalDistance
    dataObj1.totalElevation = totalElevation

    # Saves the new extrapolated data:
    dataObj1.save()

def get_dif(dateTimeObj1, dateTimeObj2):
    #returns difference between two datetime objects in order to prevent
    return (dateTimeObj2-dateTimeObj1).total_seconds()

def get_google_distance(point1,point2):
    # Idea was to use this function to get the google maps route distance
    # between two points, as a more accurate measure.
    return 0

def processData(request, hours):
    '''
    processes data on a url request, but also using crontab. Differs from
    ext_dat_list in that this function retrieves data from the spotgen api,
    while ext_data list just processes all available data in the database.
    Todo:
    > Find way to convert datetime string to datetime object to avoid saving
    and getting last object.
    '''
    hours = int(hours)
    template = "tracking/processData.html"
    contextIn = add_perams(hours)
    context = {
        "position_list": contextIn[:-1],
        "status" : contextIn[-1]
    }
    if request:
        return render(request,template,context)
    print("No request, cap with {} hours processed".format(hours))

def add_perams(cap):
    # Passes id and feed password to the request
    id = "14lbq7OpW2xeKr1EMLlUa0BRZGeiGWNYZ"
    feedPassword = "Browngirlbikes18"
    ret_value= process_data(id, feedPassword)
    return ret_value

def process_data(id, feedPassword):
    '''
    todo:
    Add method for handling 7 day limit, chron (duh)
    '''
    past_data = list(pastData.objects.all())

    # Below gets the datetimes for the start and end of the request period.

    endTime = datetime.datetime.now()
    endDateTime = (endTime.isoformat())[:-7] + "-0000"
    print("End Time: ")
    print(endDateTime)
    start = False

    #Logic for handling case where table is empty,  in which case the start
    # time is set to the maximum allowed by the spotgen api (7 days)
    if len(past_data)>0:
        last_place = list(past_data)[-1]
        startDateTime = last_place.lastGetTime
        startDateTime = (startDateTime.isoformat())[:-13] + "-0000"
    else:
        start = True
        startDateTime = endTime - datetime.timedelta(days=7) 
        startDateTime = (startDateTime.isoformat())[:-7] + "-0000"

    #Pseudo code for handling requests longer than 7 days:
    #If difference > 7 days, endDate = startdate + 7 days, call self with
    #4 min delay until difference is less. - Could save state to db & make
    # next 7 day call on next crontab run.

    # Get_list makes a request to the spotgen api.
    message_list = get_list(startDateTime, endDateTime, feedPassword, id)
    message_list.reverse()
    return_list = list(message_list)

    currentGetTime = datetime.datetime.now()

    # If no data, saves first instance of model before continuing
    if start == True and message_list:
        first_post = message_list.pop(1)
        lat = float(first_post[0])
        lng = float(first_post[1])
        time = first_post[2]
        elevation = get_elevation(lat,lng)
        x = pastData(lat=lat,lon=lng, time=time, elevation = elevation,
                     lastGetTime = currentGetTime)
        x.save()

    # If data remaining in message list, proceeds to enter it into the db &
    # uses ext_data to calculate values for each entry as it goes.
    if len(message_list)>0:
        for i in range (0, len(message_list)):
            last_place = list(pastData.objects.all())[-1]
            first_post = message_list.pop(0)
            lat = float(first_post[0])
            lng = float(first_post[1])
            time = first_post[2]
            next_place = pastData(lat=lat, lon=lng, time=time, lastGetTime = currentGetTime)
            next_place.save()
            next_place = list(pastData.objects.all())[-1]
            ext_data(last_place,next_place)

    return return_list + ["All ok!"]

def assign_sections(cap):
    cap = int(cap)
    print("cap:")
    print(cap)
    # Used to hard code the number of sections, could be added to a meta
    # data model for control from admin.
    section_number = 2
    waypoint_number = 7

    # Caps the data at a given number of hours in the past, this is used to
    # produce data for the main page, which needs to be a day behind for
    # security reasons.

    if cap:
        print("capping")
        capped = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=cap)
        print(capped)
    else:
        capped = datetime.datetime.now(datetime.timezone.utc)
        print("not capping")

    # Below for data from places
    all_places = [i for i in list(pastData.objects.all()) if i.time < capped]
    all_coords = [(place.elevation, [place.lat, place.lon], place.time) for
                  place in
                  all_places if place.speed > 2.5]
    print("all_coords:")
    print(all_coords)
    # Below for sample data
    # all_coords = get_save_elevation_data(start_coord,end_coord,100,"return")

    # Uses functions from Section_division.py to break up sections

    sections = sort_data_into_sections(all_coords)
    sections_meta = break_up_sections(sections, section_number)
    section_coords = get_chopped_sections(sections_meta, sections)
    resolved_sections = get_resolved_sections(section_coords, waypoint_number)

    # Removes all resolved coord objects, and repopulates the table
    if cap:
        capped_resolved_coord.objects.all().delete()
    else:
        resolved_coord.objects.all().delete()
    print(resolved_sections)



    for i in range(0, len(resolved_sections)):
        print(resolved_sections[i])
        for coord in resolved_sections[i]:
            if cap:
                print("saving to capped_resolved_coord()")
                x = capped_resolved_coord()
            else:
                x = resolved_coord()
            x.section = i
            x.lat = coord[0]
            x.lon = coord[1]
            print("saving...")
            x.save()

    # last section doesn't show on map, so a dummy section is populated to
    # keep usefull data. Not an elegant solution, but until I can find out
    # why it's happening, this will have to do.
    for i in range(0, 1):
        for x in range(0, 4):
            if cap:
                x = capped_resolved_coord(lat=51.5285582,
                                   lon=-0.2416795,
                                   section=len(resolved_sections) + i)
            else:
                x = resolved_coord(lat=51.5285582,
                               lon=-0.2416795,
                               section=len(resolved_sections) + i)
            print("saving empty...")
            x.save()

def get_list(startDateTime, endDateTime, feedPassword, id):
    #Section below defines the url to be requested.
    url = "https://api.findmespot.com/spot-main-web/consumer/rest-api/2.0/public/feed/"
    after_id = "/message.xml?"
    url = url + id + after_id

    peram_value = {"startDate": startDateTime,
                   "endDate": endDateTime,
                   "feedPassword": feedPassword}

    for key, value in peram_value.items():
        url = url + key + "=" + value + "&"

    url = url[:-1] # takes off the ampersand.
    print(url)
    response = requests.get(url)

    print(response.text)

    # Divides the response into messages:
    messages = re.findall('<message clientUnixTime="0">(.*?)</message>',
                          response.text)

    #For each message, gets the relevant data.
    message_list = []
    for message in messages:
        lat = (re.findall('<latitude>(.*?)</latitude>', message))[0]
        lng = (re.findall('<longitude>(.*?)</longitude>', message))[0]
        time = (re.findall('<dateTime>(.*?)</dateTime>', message))[0]
        message_list.append((lat, lng, time))

    return message_list

