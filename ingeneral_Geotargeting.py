import openpyxl
import googlemaps
import pprint
import time
import urllib.request, urllib.parse, urllib.error
import json
import ssl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'raw data'
wb.create_sheet(index = 1, title ='csvdata' )
ws1 = wb["csvdata"]



api_key = 'Enter your Google Map API'

if api_key is False:
    print("API is False")
else:
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json?'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

Failure = 0

print('*15 miles = 24140 meters')
print('*10 miles = 16093 meters')
print('*5 miles = 8047 meters')
print('The maximum of the radius: 50,000 meters')

while True:
    sstore = input("Set the Store Name: ")
    stype = input("Set the Store's Type: ")
    sradius = input("Set the radius (meters): ")

    sradius = int(sradius)
    if sradius > 50000:
        print('Radius has to less than 50,000')
        quit()
    elif sradius < 0:
        print('Radius has to greater than 0')
        quit()
    else: break


while True:
    fname = input("Enter file name: ")
    try:
        fh = open(fname)
    except:
        print('File cannot be opened:', fname+'\n' 'Please enter the correct name')
        quit()

    sumcount = 0
    #这是统计总数的

    for SchoolName in fh:
        SchoolName = SchoolName.rstrip()

        address = SchoolName
        if len(address) < 1: break

        parms = dict()
        parms['address'] = address
        if api_key is not False: parms['key'] = api_key
        url = serviceurl + urllib.parse.urlencode(parms)

        # print('Retrieving', url)
        uh = urllib.request.urlopen(url, context=ctx)
        data = uh.read().decode()
        # print('Retrieved', len(data), 'characters')

        try:
            js = json.loads(data)
        except:
            js = None

        if not js or 'status' not in js or js['status'] != 'OK':
            print('==== Failure To Retrieve ====')
            print(address, "could not find")
            Failure = Failure + 1
            continue

        # print(json.dumps(js, indent=4))

        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        # print('lat', lat, 'lng', lng)
        # location = js['results'][0]['formatted_address']
        # 这是地区的地址
        # print(location)
        # print(address)


        #lnl is the lat and lng data
        lnl = lat,lng

        #gamps is the plug in function
        gmaps = googlemaps.Client(key = api_key)

        places_result = gmaps.places_nearby(location = lnl, radius = sradius, open_now = False, name = sstore, type = stype)


        # pprint.pprint(places_result['results'])
        # print(places_result)
        #这里可以看源文件

        count = 0

        for place in places_result['results']:

            # define my place ID
            my_place_id = place ['place_id']
            count = count + 1
            sumcount = sumcount + 1

            #define the field we want sent back to us
            my_fields = ['name','formatted_address']

            places_details = gmaps.place(place_id = my_place_id, fields = my_fields)

            #===============把数据加进excel========================
            # print(places_details['result']['formatted_address'])

            col1 = places_details['result']['formatted_address']
            col2 = places_details['result']['name']
            values = [address,col1,col2]
            print(values)
            # 这里可以测试一下结果
            ws1.append(values)

            #====================分割线===========================



            # print(address)
            # pprint.pprint(places_details['result'])

        # print('Total:', address, 'nearby store:', count)
        # print("==================")

        #pause the script for 3 times
        time.sleep(3)

        #get the next 20 results
        try:
            places_result = gmaps.places_nearby(page_token = places_result['next_page_token'] )
            # pprint.pprint(places_result)

            for place in places_result['results']:

                # define my place ID
                my_place_id = place ['place_id']
                count = count + 1
                sumcount = sumcount + 1
                my_fields = ['name','formatted_address']
                places_details = gmaps.place(place_id = my_place_id, fields = my_fields)

                col1 = places_details['result']['formatted_address']
                col2 = places_details['result']['name']
                values = [address, col1, col2]
                print(values)
                # 这里可以测试一下结果
                ws1.append(values)

                # print(address)
                # pprint.pprint(places_details['result'])

        #     print('Total:',address,'nearby Tire Shop:',count)
        #     print("==================")
        #
        except: continue

    print("Total Failure to extract:",Failure)
    print('finis')
    print('Total Store:', sumcount)
    wb.save('ingeneral_geotargeting.xlsx')

