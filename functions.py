import requests
import urllib2
import json
import pprint
import os
from model import connect_to_db, db, Airport, User, Saved_trip, Flight, Lodging




################################################################################

#functinos related to flight 



def request_QPX(departure_airport, destination_airport, input_departure_date,input_return_date):
    """sending request to QPX and return the results as python dictionary"""
    print "INSIDE REQUEST", destination_airport, departure_airport, input_departure_date, input_departure_date

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
            "date": input_departure_date,
            "maxStops": 0
          },
          {
            "origin": destination_airport,
            "destination": departure_airport,
            "date": input_return_date,
            "maxStops": 0
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

    print flight_response_dict

    return flight_response_dict



def parse_QPX(flight_response_dict):
    """Take input python dictionary and parse out desire fields into new dictionary"""

    #Set key-value pair for new flight dictionary
    flight_info_dict = {"destination_city" : flight_response_dict["trips"]["data"]["city"][0]["name"],
        "departure_city" : flight_response_dict["trips"]["data"]["city"][1]["name"],
        "departure_airport" :  flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["origin"],
        "destination_airport" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["destination"],
        "carrier" : flight_response_dict["trips"]["data"]["carrier"][0]["name"],
        "outbound_departure_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["departureTime"],
        "outbound_arrival_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["leg"][0]["arrivalTime"],
        "inbound_departure_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][1]["segment"][0]["leg"][0]["departureTime"],
        "inbound_arrival_time" : flight_response_dict["trips"]["tripOption"][0]["slice"][1]["segment"][0]["leg"][0]["arrivalTime"],
        "flight_price" : flight_response_dict["trips"]["tripOption"][0]["saleTotal"],
        "outbound_carrier_id" :flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["flight"]["carrier"],
        "outbound_flight_number" : flight_response_dict["trips"]["tripOption"][0]["slice"][0]["segment"][0]["flight"]["number"],
        "inbound_carrier_id" : flight_response_dict["trips"]["tripOption"][0]["slice"][1]["segment"][0]["flight"]["carrier"],
        "inbound_flight_number" :flight_response_dict["trips"]["tripOption"][0]["slice"][1]["segment"][0]["flight"]["number"] }




    return flight_info_dict

def get_flight_id(flight_info_dict):
    """get flight id from db or newly added flight"""

    #search if flght is already saved in database
    search_flight_in_db = Flight.query.filter(Flight.departure_airport==flight_info_dict["departure_airport"],
                        Flight.destination_airport==flight_info_dict["destination_airport"],
                        Flight.carrier==flight_info_dict["carrier"],
                        Flight.outbound_departure_time==flight_info_dict["outbound_departure_time"],
                        Flight.outbound_arrival_time==flight_info_dict["outbound_arrival_time"],
                        Flight.inbound_departure_time==flight_info_dict["inbound_departure_time"],
                        Flight.inbound_arrival_time==flight_info_dict["inbound_arrival_time"],
                        Flight.flight_price==flight_info_dict["flight_price"],
                        Flight.outbound_carrier_id==flight_info_dict["outbound_carrier_id"],
                        Flight.outbound_flight_number==flight_info_dict["outbound_flight_number"],
                        Flight.inbound_carrier_id==flight_info_dict["inbound_carrier_id"],
                        Flight.inbound_flight_number==flight_info_dict["inbound_flight_number"]).first()
    
    #if flight not in database, save it 
    if not search_flight_in_db:

        flight = Flight(departure_airport=flight_info_dict["departure_airport"],
                        destination_airport=flight_info_dict["destination_airport"],
                        carrier=flight_info_dict["carrier"],
                        outbound_departure_time=flight_info_dict["outbound_departure_time"],
                        outbound_arrival_time=flight_info_dict["outbound_arrival_time"],
                        inbound_departure_time=flight_info_dict["inbound_departure_time"],
                        inbound_arrival_time=flight_info_dict["inbound_arrival_time"],
                        flight_price=flight_info_dict["flight_price"],
                        outbound_carrier_id=flight_info_dict["outbound_carrier_id"],
                        outbound_flight_number=flight_info_dict["outbound_flight_number"],
                        inbound_carrier_id=flight_info_dict["inbound_carrier_id"],
                        inbound_flight_number=flight_info_dict["inbound_flight_number"])
    
        db.session.add(flight)
        db.session.commit()

    #get id for the newly added flight
    if not search_flight_in_db:
        current_flight_id = Flight.query.order_by(Flight.flight_id.desc()).first().flight_id
        #print "flight not in db", current_flight_id    
    
    #get id for the already existed flight
    else:
        current_flight_id = search_flight_in_db.flight_id
        #print "flight in db", current_flight_id

    return current_flight_id



################################################################################

#functions related to lodging



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

    return lodging_response_dict


def parse_Airbnb(lodging_response_dict):
    """Take input python dictionary and parse out desire fields into new dictionary"""

    #Set key-value pair for new flight dictionary
    lodging_info_dict = {"airbnb_id" : lodging_response_dict["search_results"][0]["listing"]["id"],
    "address" : lodging_response_dict["search_results"][0]["listing"]["public_address"],
    "picture_url" : lodging_response_dict["search_results"][0]["listing"]["picture_url"],
    "price" : lodging_response_dict["search_results"][0]["pricing_quote"]["localized_total_price"]}

    return lodging_info_dict



def get_lodging_id(lodging_info_dict):
    """get lodging id from db or newly added lodging"""

    #search if lodging is already saved in database
    search_lodging_in_db = Lodging.query.filter(Lodging.airbnb_id==lodging_info_dict["airbnb_id"],
                        Lodging.address==lodging_info_dict["address"],
                        Lodging.picture_url==lodging_info_dict["picture_url"],
                        Lodging.price==lodging_info_dict["price"]).first()

    #if lodging not in database, save it 
    if not search_lodging_in_db:
        lodging = Lodging(airbnb_id=lodging_info_dict["airbnb_id"],
                        address=lodging_info_dict["address"],
                        picture_url=lodging_info_dict["picture_url"],
                        price=lodging_info_dict["price"])
    
        db.session.add(lodging)
        db.session.commit()

    #get id for the newly added flight
    if not search_lodging_in_db:
        current_lodging_id = lodging.query.order_by(Lodging.lodging_id.desc()).first().lodging_id
        #print "lodging not in db", current_lodging_id    
    
    #get id for the already existed flight
    else:
        current_lodging_id = search_lodging_in_db.lodging_id
        #print "lodging in db", current_lodging_id

    return current_lodging_id



################################################################################

#functions related to the trip


def save_trip_to_db(current_flight_id, current_lodging_id, current_user_id):
    """store the user saved trip into database"""

    #search if lodging is already saved in database
    search_trip_in_db = Saved_trip.query.filter(Saved_trip.user_id==current_user_id,
                                                Saved_trip.flight_id == current_flight_id,
                                                Saved_trip.lodging_id== current_lodging_id).first()
    
    #if trip not in database, save it 
    if not search_trip_in_db:

        saved_trip = Saved_trip(user_id=current_user_id,
                            flight_id = current_flight_id,
                            lodging_id = current_lodging_id)

        db.session.add(saved_trip)
        db.session.commit()
        return "Trip saved!"

    #if trip already saved in db before, show message
    else:
        return "You have already saved this trip before!"
   

    
def request_google_maps(dep_lat, dep_long, des_lat, des_long):
    """sending request to Google Maps and return the results as python dictionary"""

    #The url to send request
    api_key = os.environ['Google_maps_KEY']
    
    url = "https://maps.googleapis.com/maps/api/staticmap?key=%s"%(api_key)



    #The search parameters to pass into request body
    search_param = { 'size': "400x400",
                    'markers': str(dep_lat)+","+str(dep_long)+"|"+str(des_lat)+","+str(des_long),
                    'path': "geodesic:true|"+str(dep_lat)+","+str(dep_long)+"|"+str(des_lat)+","+str(des_long),
                    'language':"en"}


    #Send json request and get response
    map_response = requests.get(url, params=search_param)

    print map_response.url
    return map_response.url

    











