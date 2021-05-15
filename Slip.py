# Imports nessesary libraires for APIs
import json
# Requests as req just means we write 'req' instead of 'requests'
import requests as req
# Imports package which encodes str into URL format
import urllib.parse
# Adding classes for fancy text
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
# Defining different varuibles
base_url = "https://maps.googleapis.com/maps/api"
url_end = "&key=AIzaSyCQrI7XpRa4ABzc_cqPCxLCcneG5S5mMR8"
origin_parameter = "origin="
destination_parameter = "destination="
transportation_mode = "walking"
# Introduction print()
print('')
print(color.DARKCYAN+color.BOLD+"Welcome to Slip!"+color.END)
print(color.CYAN+"This program will lets you see the intensity of a walk simply from it's origin and destination!"+color.END)
print('')
# Informing of proper format
print(color.YELLOW+"When entering addresses please use the global code copy and pasted from Google Maps. eg. 5759+2P Woodstock, Ontario"+color.END)
print(color.YELLOW+"When entering coodinates please use the following format: \'latitude,longitude\', eg. 41.43206,-81.38992"+color.END)
print('')
    # # Asks if biking or hiking, to provide differeing end data, and for the API 'mode' parameter FLAG: was unessesary to implement, simply objective for later
    # transportation_mode = input("Will you be 'bicycling' or 'walking'?   ")
# Collecting start and destination data
# entering and storing of the raw, unformatted origin/destination
raw_origin = input(color.GREEN+"Please enter the address/coordinates of your starting point using the format above:   "+color.END)
raw_desination = input(color.GREEN+"Please enter the address/coordinates of your destination using the format above:   "+color.END)
# testing shortcut that autosets vars
if raw_origin == "test":
    raw_origin = "43.520779, -79.977398"
    raw_desination= "G2PC+MH Milton, Ontario"
if raw_desination == "test":
    raw_origin = "G23Q+X5 Milton, Ontario"
    raw_desination = " 43.530579, -79.974906 "
# Taking raw origin and raw destination and encoding it to URL-friendly text
url_origin = urllib.parse.quote(raw_origin)
url_destination = urllib.parse.quote(raw_desination)
# Creating the def for polyline grabbing from the address and mode info
# def polyline_grab(): 
# Makes the API URL for the API to ping by concatonating a fuck ton of the different varuibles
polyline_url = base_url + "/directions/json?"+origin_parameter+url_origin+"&mode="+transportation_mode+"&"+destination_parameter+url_destination+"&samples=25"+url_end
# Uses the weird method and stores the get as a .text file
unparsed_data = req.get(polyline_url)
# Parses the previous text file into a json file
parsed_data = json.loads(unparsed_data.text)
# finds the total distance and encoded polyline from the json
total_distance = (parsed_data["routes"][0]["legs"][0]["distance"]["value"])
polyline_encoded = (parsed_data["routes"][0]["overview_polyline"]["points"])

# API 2:

# takes the polyline data from the previous API, and url-encodes it to be fit into the new API URL
polyline_url_encoded = urllib.parse.quote(polyline_encoded)
# Takes the previous poly info attained from the previous API, and creates the new elevation API url
elevation_url = base_url+"/elevation/json?locations=enc:"+polyline_url_encoded+url_end
# takes the elevation url, runs it and parses it's data
preparsed_elevation_data = req.get(elevation_url)
parsed_elevation_data = json.loads(preparsed_elevation_data.text)
# collects the elevation points from the json, and appends to list
elevation_list = []
temp_index = 0
#  checks the length of the dict/list to be appended
max_index = len(parsed_elevation_data["results"])
while True:
    temp_var = parsed_elevation_data["results"][temp_index]["elevation"]
    elevation_list.append(temp_var)
    temp_index = temp_index + 1
    # checks if on last index, if so it breaks loop
    if temp_index == max_index:
        break
# Calculating elevation gain
temp_index= 0
elevation_total = 0
elevation_difference = 0
future_elevation = 0
current_elevation = 0
while True:
    current_elevation = elevation_list[temp_index]
    future_elevation = elevation_list[temp_index+1]
    elevation_difference = future_elevation - current_elevation
    if elevation_difference > 0:
        elevation_total = elevation_difference + elevation_total
    temp_index = temp_index + 1
    if temp_index == max_index - 1:
        break
print('')
print('')
print('')
print(color.PURPLE+"The total distance of your journey will be "+str(total_distance)+"m."+color.END)
print(color.PURPLE+"The total elevation gain during your journey is "+str(elevation_total)+"m."+color.END)
# If statements code

if total_distance < 10000 and elevation_total < 500:
     print(color.BOLD+"Very Easy. Suitable for people of all ages who are in fair condition."+color.END)

elif total_distance < 15000 and elevation_total < 800:
    print(color.BOLD+"Easy. A suitable hike for you if you have a basic fitness level."+color.END)

elif (elevation_total > 800 and elevation_total < 1500) and total_distance == 15000:
    print(color.BOLD+"Moderate. This is considered easy for frequent hikers of any age."+color.END)

elif (elevation_total > 1000 and elevation_total < 1500) and total_distance > 15000:
    print(color.BOLD+"Challenging. A very long distance hike with big elevation gains. High fitness level is required because speed will be important to complete. Age and experience will also be factors in completing a hike of this difficulty."+color.END)

elif (elevation_total > 1000 and elevation_total < 1500) and total_distance > 15000:
    print(color.BOLD+"Challenging. A very long distance hike with big elevation gains. High fitness level is required because speed will be important to complete. Age and experience will also be factors in completing a hike of this difficulty."+color.END)
elif elevation_total >= 1500 and total_distance >= 15000:
    print(color.BOLD+"At this elevation differntial and length this is a multi-day trip for professionals only and requires preperation."+color.END)


