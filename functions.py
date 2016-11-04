import requests
import urllib2
import json
import pprint
import os
from model import connect_to_db, db, Airport, User, Saved_trip, Flight, Lodging


def request_QPX(departure_airport, destination_airport, input_departure_date,input_return_date):
    """sending request to QPX and return the results as python dictionary"""

    #The url to send request
    api_key = os.environ['QPX_KEY']
    url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=%s" %(api_key)

    #The search parameters to pass into request body 
    search_param ={
      "request": {
        "slice": [
          {
            "origin": departure_airport,
            "destination": destination_airport,
            "date": input_departure_date
          },
          {
            "origin": destination_airport,
            "destination": departure_airport,
            "date": input_return_date
          }
        ],
        "passengers": {
          "adultCount": 1
        },
        "solutions": 1
      }
    }

    #Turn search parameters into json format
    request_body = json.dumps(search_param)

    #Send json request and return json response
    response_json = urllib2.Request(url, request_body, {'Content-Type':'application/json'})

    #Open the json response
    response_open = urllib2.urlopen(response_json)

    #Turn json response into python dictionary
    flight_response_dict = json.load(response_open)

    # Closes JSON results
    response_open.close()

    #pprint.pprint(flight_response_dict)

    return flight_response_dict


flight_response_dict={u'kind': u'qpxExpress#tripsSearch',
 u'trips': {u'data': {u'aircraft': [{u'code': u'320',
                                     u'kind': u'qpxexpress#aircraftData',
                                     u'name': u'Airbus A320'}],
                      u'airport': [{u'city': u'NYC',
                                    u'code': u'JFK',
                                    u'kind': u'qpxexpress#airportData',
                                    u'name': u'New York John F Kennedy International'},
                                   {u'city': u'SFO',
                                    u'code': u'SFO',
                                    u'kind': u'qpxexpress#airportData',
                                    u'name': u'San Francisco International'}],
                      u'carrier': [{u'code': u'VX',
                                    u'kind': u'qpxexpress#carrierData',
                                    u'name': u'Virgin America Inc.'}],
                      u'city': [{u'code': u'NYC',
                                 u'kind': u'qpxexpress#cityData',
                                 u'name': u'New York'},
                                {u'code': u'SFO',
                                 u'kind': u'qpxexpress#cityData',
                                 u'name': u'San Francisco'}],
                      u'kind': u'qpxexpress#data',
                      u'tax': [{u'id': u'ZP',
                                u'kind': u'qpxexpress#taxData',
                                u'name': u'US Flight Segment Tax'},
                               {u'id': u'AY_001',
                                u'kind': u'qpxexpress#taxData',
                                u'name': u'US September 11th Security Fee'},
                               {u'id': u'US_001',
                                u'kind': u'qpxexpress#taxData',
                                u'name': u'US Transportation Tax'},
                               {u'id': u'XF',
                                u'kind': u'qpxexpress#taxData',
                                u'name': u'US Passenger Facility Charge'}]},
            u'kind': u'qpxexpress#tripOptions',
            u'requestId': u'P8fdcjzcur79HQuFP0PMTu',
            u'tripOption': [{u'id': u'K25yfAkiSP9R7Gse1GfyfL001',
                             u'kind': u'qpxexpress#tripOption',
                             u'pricing': [{u'baseFareTotal': u'USD500.47',
                                           u'fare': [{u'basisCode': u'I14QNR',
                                                      u'carrier': u'VX',
                                                      u'destination': u'NYC',
                                                      u'id': u'AZ8I/Igwj5ld5rC9gZBpNbU6iOfOzV8/0hnXdOOI9Rh2',
                                                      u'kind': u'qpxexpress#fareInfo',
                                                      u'origin': u'SFO'},
                                                     {u'basisCode': u'M7QNR',
                                                      u'carrier': u'VX',
                                                      u'destination': u'SFO',
                                                      u'id': u'AjJaAwvBZEGAsNO46iuPSqQ/YP+VwJwcuZoZJlU4I2Sk',
                                                      u'kind': u'qpxexpress#fareInfo',
                                                      u'origin': u'NYC'}],
                                           u'fareCalculation': u'SFO VX NYC 236.28I14QNR VX SFO 264.19M7QNR USD 500.47 END ZP SFO JFK XT 37.53US 8.00ZP 11.20AY 9.00XF SFO4.50 JFK4.50',
                                           u'kind': u'qpxexpress#pricingInfo',
                                           u'latestTicketingTime': u'2016-11-01T23:59-04:00',
                                           u'passengers': {u'adultCount': 1,
                                                           u'kind': u'qpxexpress#passengerCounts'},
                                           u'ptc': u'ADT',
                                           u'saleFareTotal': u'USD500.47',
                                           u'saleTaxTotal': u'USD65.73',
                                           u'saleTotal': u'USD566.20',
                                           u'segmentPricing': [{u'fareId': u'AZ8I/Igwj5ld5rC9gZBpNbU6iOfOzV8/0hnXdOOI9Rh2',
                                                                u'kind': u'qpxexpress#segmentPricing',
                                                                u'segmentId': u'GCzbm1WcKP83Bxp3'},
                                                               {u'fareId': u'AjJaAwvBZEGAsNO46iuPSqQ/YP+VwJwcuZoZJlU4I2Sk',
                                                                u'kind': u'qpxexpress#segmentPricing',
                                                                u'segmentId': u'G2DW+95NLCIV5YNN'}],
                                           u'tax': [{u'chargeType': u'GOVERNMENT',
                                                     u'code': u'US',
                                                     u'country': u'US',
                                                     u'id': u'US_001',
                                                     u'kind': u'qpxexpress#taxInfo',
                                                     u'salePrice': u'USD37.53'},
                                                    {u'chargeType': u'GOVERNMENT',
                                                     u'code': u'AY',
                                                     u'country': u'US',
                                                     u'id': u'AY_001',
                                                     u'kind': u'qpxexpress#taxInfo',
                                                     u'salePrice': u'USD11.20'},
                                                    {u'chargeType': u'GOVERNMENT',
                                                     u'code': u'XF',
                                                     u'country': u'US',
                                                     u'id': u'XF',
                                                     u'kind': u'qpxexpress#taxInfo',
                                                     u'salePrice': u'USD9.00'},
                                                    {u'chargeType': u'GOVERNMENT',
                                                     u'code': u'ZP',
                                                     u'country': u'US',
                                                     u'id': u'ZP',
                                                     u'kind': u'qpxexpress#taxInfo',
                                                     u'salePrice': u'USD8.00'}]}],
                             u'saleTotal': u'USD566.20',
                             u'slice': [{u'duration': 320,
                                         u'kind': u'qpxexpress#sliceInfo',
                                         u'segment': [{u'bookingCode': u'I',
                                                       u'bookingCodeCount': 7,
                                                       u'cabin': u'COACH',
                                                       u'duration': 320,
                                                       u'flight': {u'carrier': u'VX',
                                                                   u'number': u'26'},
                                                       u'id': u'GCzbm1WcKP83Bxp3',
                                                       u'kind': u'qpxexpress#segmentInfo',
                                                       u'leg': [{u'aircraft': u'320',
                                                                 u'arrivalTime': u'2016-12-26T23:45-05:00',
                                                                 u'departureTime': u'2016-12-26T15:25-08:00',
                                                                 u'destination': u'JFK',
                                                                 u'destinationTerminal': u'4',
                                                                 u'duration': 320,
                                                                 u'id': u'LlGbPe4+SzCWcu1D',
                                                                 u'kind': u'qpxexpress#legInfo',
                                                                 u'mileage': 2579,
                                                                 u'onTimePerformance': 78,
                                                                 u'origin': u'SFO',
                                                                 u'originTerminal': u'2',
                                                                 u'secure': True}],
                                                       u'marriedSegmentGroup': u'0'}]},
                                        {u'duration': 395,
                                         u'kind': u'qpxexpress#sliceInfo',
                                         u'segment': [{u'bookingCode': u'M',
                                                       u'bookingCodeCount': 7,
                                                       u'cabin': u'COACH',
                                                       u'duration': 395,
                                                       u'flight': {u'carrier': u'VX',
                                                                   u'number': u'11'},
                                                       u'id': u'G2DW+95NLCIV5YNN',
                                                       u'kind': u'qpxexpress#segmentInfo',
                                                       u'leg': [{u'aircraft': u'320',
                                                                 u'arrivalTime': u'2016-12-31T11:05-08:00',
                                                                 u'departureTime': u'2016-12-31T07:30-05:00',
                                                                 u'destination': u'SFO',
                                                                 u'destinationTerminal': u'2',
                                                                 u'duration': 395,
                                                                 u'id': u'LMANNSdFEyoXCMVH',
                                                                 u'kind': u'qpxexpress#legInfo',
                                                                 u'mileage': 2579,
                                                                 u'onTimePerformance': 100,
                                                                 u'origin': u'JFK',
                                                                 u'originTerminal': u'4',
                                                                 u'secure': True}],
                                                       u'marriedSegmentGroup': u'1'}]}]}]}}


def parse_QPX(flight_response_dict):
    """Takes input python dictionary and parse out desire fields into new dictionary"""

    #Set key-value pair for new flight dictionary
    flight_info_dict = {"destination_city" : flight_response_dict["trips"]["data"]["city"][0]["name"],
        "departure_city" : flight_response_dict["trips"]["data"]["city"][1]["name"],
        "departure_airport" :  flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["origin"],
        "destination_airport" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["destination"],
        "carrier" : flight_response_dict["trips"]["data"]["carrier"][0]["name"],
        "outbond_departure_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["departureTime"],
        "outbond_arrival_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["arrivalTime"],
        "inbond_departure_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][1]["segment"][0]["leg"][0]["departureTime"],
        "inbond_arrival_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][1]["segment"][0]["leg"][0]["arrivalTime"],
        "flight_price" : flight_response_dict["trips"]["tripOption"][0]["saleTotal"]}

    return flight_info_dict


def request_Airbnb(destination_city, input_departure_date, input_return_date):
    """sending request to QPX and return the results as python dictionary"""

    #The url to send request
    api_key = os.environ['Airbnb_KEY']
    url = "https://api.airbnb.com/v2/search_results?client_id=%s" %(api_key)
    
    #The search parameters to pass into request body
    search_param = { 'locale' : 'en-US', 
        'currency' : 'USD',
        # '_format': 'for_search_results_with_minimal_pricing',
        '_limit':  '1',
        #'_offset': '0',
        'guests':  '1',
        'ib':  'false',
        'sort':  '1',
        'min_beds' :  '1',
        'location':  destination_city,
        'price_min' : '40',
        # 'price_max': '210',
        # 'fetch_facets':'true',
        # 'ib_add_photo_flow':'true',
        # 'min_num_pic_urls':'10',
        'checkin': input_departure_date,
        'checkout': input_return_date}


    #Send json request and return json response
    response_json = requests.get(url, params=search_param)

    #Turn json response into python dictionary
    lodging_response_dict = response_json.json()


    #pprint.pprint(lodging_response_dict)

    print "URL IS HERE!!!!!!!!*************** ", (response_json.url)

    return lodging_response_dict


def parse_Airbnb(lodging_response_dict):
    """Takes input python dictionary and parse out desire fields into new dictionary"""

    #Set key-value pair for new flight dictionary
    lodging_info_dict = {"airbnb_id" : lodging_response_dict["search_results"][0]["listing"]["id"],
    "address" : lodging_response_dict["search_results"][0]["listing"]["public_address"],
    "picture_url" : lodging_response_dict["search_results"][0]["listing"]["picture_url"],
    "price" : lodging_response_dict["search_results"][0]["pricing_quote"]["localized_total_price"]}

    return lodging_info_dict

def get_flight_id(flight_info_dict):
    """get flight id from db or newly added flight"""

    search_flight_in_db = Flight.query.filter(Flight.departure_airport==flight_info_dict["departure_airport"],
                        Flight.destination_airport==flight_info_dict["destination_airport"],
                        Flight.carrier==flight_info_dict["carrier"],
                        Flight.outbond_departure_time==flight_info_dict["outbond_departure_time"],
                        Flight.outbond_arrival_time==flight_info_dict["outbond_arrival_time"],
                        Flight.inbond_departure_time==flight_info_dict["inbond_departure_time"],
                        Flight.inbond_arrival_time==flight_info_dict["inbond_arrival_time"],
                        Flight.flight_price==flight_info_dict["flight_price"]).first()
    
    if not search_flight_in_db:

        flight = Flight(departure_airport=flight_info_dict["departure_airport"],
                        destination_airport=flight_info_dict["destination_airport"],
                        carrier=flight_info_dict["carrier"],
                        outbond_departure_time=flight_info_dict["outbond_departure_time"],
                        outbond_arrival_time=flight_info_dict["outbond_arrival_time"],
                        inbond_departure_time=flight_info_dict["inbond_departure_time"],
                        inbond_arrival_time=flight_info_dict["inbond_arrival_time"],
                        flight_price=flight_info_dict["flight_price"])
    
        db.session.add(flight)
        db.session.commit()

    if not search_flight_in_db:
        current_flight_id = Flight.query.order_by(Flight.flight_id.desc()).first().flight_id
        print "flight not in db", current_flight_id    
    else:
        current_flight_id = search_flight_in_db.flight_id
        print "flight in db", current_flight_id

    return current_flight_id


def get_lodging_id(lodging_info_dict):
    """get lodging id from db or newly added lodging"""

    search_lodging_in_db = Lodging.query.filter(Lodging.airbnb_id==lodging_info_dict["airbnb_id"],
                        Lodging.address==lodging_info_dict["address"],
                        Lodging.picture_url==lodging_info_dict["picture_url"],
                        Lodging.price==lodging_info_dict["price"]).first()

    if not search_lodging_in_db:
        lodging = Lodging(airbnb_id=lodging_info_dict["airbnb_id"],
                        address=lodging_info_dict["address"],
                        picture_url=lodging_info_dict["picture_url"],
                        price=lodging_info_dict["price"])
    
        db.session.add(lodging)
        db.session.commit()

    if not search_lodging_in_db:
        current_lodging_id = lodging.query.order_by(Lodging.lodging_id.desc()).first().lodging_id
        print "lodging not in db", current_lodging_id    
    else:
        current_lodging_id = search_lodging_in_db.lodging_id
        print "lodging in db", current_lodging_id

    return current_lodging_id



def save_trip_to_db(current_flight_id, current_lodging_id, current_user_id):
    """store the user saved trip into database"""


    search_trip_in_db = Saved_trip.query.filter(#Saved_trip.user_id==1,
                                                Saved_trip.user_id==current_user_id,
                                                Saved_trip.flight_id == current_flight_id,
                                                Saved_trip.lodging_id== current_lodging_id).first()
    if not search_trip_in_db:

        saved_trip = Saved_trip(user_id=current_user_id,
                            #user_id=1,
                            flight_id = current_flight_id,
                            lodging_id = current_lodging_id)

        db.session.add(saved_trip)
        db.session.commit()

    # else:
    #     flash("You already saved this trip!")
    #     print "YOU ALREADY SAVED THIS"
   

flight_info_dict= {'outbond_departure_time': u'2016-12-26T15:25-08:00', 'inbond_departure_time': u'2016-12-31T07:30-05:00', 'outbond_arrival_time': u'2016-12-26T23:45-05:00', 'carrier': u'Virgin America Inc.', 'departure_city': u'San Francisco', 'departure_airport': u'SFO', 'inbond_arrival_time': u'2016-12-31T11:05-08:00', 'destination_airport': u'JFK', 'flight_price': u'USD566.21', 'destination_city': u'New York'}
lodging_info_dict= {'price': 321, 'address': u'Domain Drive, Austin, TX 78758, United States', 'picture_url': u'https://a2.muscache.com/im/pictures/bd9607b3-7e74-4a1d-b45b-9dacd4e1c856.jpg?aki_policy=large', 'airbnb_id': 13488012}














