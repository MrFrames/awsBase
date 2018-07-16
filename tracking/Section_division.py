import requests
import matplotlib.pyplot as plt
import json
import pickle

start_coord = [51.5285582,-0.2416795]  # London
water_test_coord = [56.181609, -0.2443077]  # North sea
end_coord = [48.8588536,2.3120406]  # Paris

def get_sample (start_coord,end_coord, divisions):
    test_coord_list = [start_coord]

    delta_coord = [end_coord[0]-start_coord[0],
                   end_coord[1]-start_coord[1]]

    for i in range(1,divisions):
        lat = start_coord[0] + (delta_coord[0]/divisions)*i
        lng = start_coord[1] + (delta_coord[1]/divisions)*i
        test_coord_list.append([lat,lng])
        print("{}:{}".format(lat,lng))

    return test_coord_list

def get_response (lat,lng):
    url = "https://maps.googleapis.com/maps/api/elevation/json?"
    latlng = "locations=" + str(lat) + "," + str(lng) + "&"
    key = "key=AIzaSyCxywHXPqUPih3DcwKjXT7eNj_q-p0yAhA"
    url = url + latlng + key

    response=requests.get(url)
    return response

def get_elevation(lat,lng):
    elevation_response = get_response(lat,lng)
    #print("lat:{}, lng: {}".format(lat,lng))
    data_dict = json.loads(elevation_response.text)
    results = data_dict.get('results')[0]
    elevation = results.get('elevation')
    return elevation

def over_water(coord1,coord2):
    coord_list = get_sample(coord1,coord2, 10)
    for coord in coord_list:
        if get_elevation(coord[0],coord[1]) <= 0:
            return True
    return False

def get_save_elevation_data(start, end, divisions, save_return):
    get_elevation(start[0],start[1])
    elevation_list = []
    coord_list = get_sample(start,end,divisions)
    for coord in coord_list:
        elevation = get_elevation(coord[0], coord[1])
        print(elevation)
        elevation_list.append((elevation,coord))
    if save_return != "return":
        with open(save_return, "wb") as file:
            pickle.dump(elevation_list,file)
    else:
        return elevation_list

#get_save_elevation_data(start_coord, end_coord, 100,"London_Paris.pkl")

def sort_data_into_sections(dataIn):

    above_sealevel_sections = []
    for i in range(0,len(dataIn)):
        if i == 0 and dataIn[i][0] > 0:
            above_sealevel_sections.append([dataIn[i]])
        elif dataIn[i][0] > 0 and dataIn[i-1][0] <= 0:
            above_sealevel_sections.append([dataIn[i]])
        elif dataIn[i][0] > 0 and dataIn[i-1][0] > 0:
            above_sealevel_sections[-1].append(dataIn[i])
    return above_sealevel_sections

def break_up_sections(sections, number):
    section_list = []
    print("sections:")
    print(sections)

    # Logic returns number of sections, if larger than number of broken up
    print("section length: " + str(len(sections)))

    if len(sections) >= number:
        section_dict = {}
        for i in range(0, len(sections)):
            section_dict[i] = (len(sections[i]),1)
        print("More sections than number :" + str(section_dict))
        return section_dict
    else:
        new_number = number - len(sections)

    # Inits a list with the section length, the divisor & the
    # orginal index for later lookup

    for i in range(0,len(sections)):
        section_list.append([len(sections[i]),1,i])

    '''
    Loops for available divisions determined above, and carries out the 
    following for the section with the longest subsection length:
    
    > Adds to the divisor.
    > Divides the orginal section length by the new value to determine a new 
    subsection length.
    '''
    for i in range (0,new_number):
        section_list = sorted(section_list, key=lambda x: x[0], reverse=True)
        original_length = section_list[0][0] * section_list[0][1]
        section_list[0][1] += 1
        section_list[0][0] = original_length/section_list[0][1]

    section_dict = {}
    #Converts result to dict for easy index lookup
    for i in range(0,len(section_list)):
        section_dict[section_list[i][2]] = (section_list[i][0],
                                            section_list[i][1])
    return (section_dict)

def get_chopped_sections(section_dict,sections):
    new_sections = []
    for i in range(0,len(sections)):
        division = section_dict.get(i)[1]
        section = sections[i]
        for i in range(1,division+1):
            length = len(section)
            limit = int((length/division)*i)
            start = int((length/division)*(i-1))
            if limit != length:
                limit = limit+1
            print("[{}:{}] in {}".format(start,limit, length))
            new_sections.append([i[1] for i in section[start:limit]])
    return(new_sections)

def get_resolved_sections(sections,resolution):
    resolved_sections = []
    for section in sections:
        if len(section) <= resolution:
            resolved_sections.append(section)
        else:
            new_section = []
            for i in range(0,resolution-1):
                index = int(((len(section))/(resolution-1))*i)
                new_section.append(section[index])
            new_section.append(section[-1])
            resolved_sections.append(new_section)
    return resolved_sections

'''
dataIn = []
with open("London_Paris.pkl", "rb") as file:
    dataIn = pickle.load(file)
print(dataIn)

sections = sort_data_into_sections(dataIn)
print(sections)

section_dict = break_up_sections(sections,3)

chopped_sections = get_chopped_sections(section_dict,sections)
for section in chopped_sections:
    print(section)

resolved_sections = get_resolved_sections(chopped_sections, 7)

for section in sections:
    print(section)

'''



#print(resolved_sections)

#for section in resolved_sections:
#    print(len(section))

'''
chopped_sections = get_chopped_sections(section_dict,sections)

for section in chopped_sections:
    print(len(section))
    print(section)

'''