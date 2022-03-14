import datetime
import time
from flask import Flask, request, render_template, jsonify
from flask_simple_geoip import SimpleGeoIP
import requests
import yelp_getter

application = Flask(__name__)

# Location Getter
application.config.update(GEOIPIFY_API_KEY=yelp_getter.GEO_KEY)
simple_geoip = SimpleGeoIP(application)



# Param Constructor
def param_constructor(term:str="pizza", location:str="", limit:int=10, ip_data:dict=simple_geoip, at_ten:bool=True):
    """Given search terms, construct parameters for API.
    Args:
        term (str): search term, can provide "food", or "burritos".
        location (str): User provided location, "Seattle", "New York City". Default NYC
        limit (int): Limit of search results (default 10)
        ip_data (dict): IP JSON object from SimpleGEOIP, will default to this if no location given
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    # Get Current Time and Check 10PM
    date = datetime.datetime.now().replace(hour=22,minute=0,second=0,microsecond=0)
    unixtime = time.mktime(date.timetuple())


    param = {'term':term, 'limit':limit, 'sort_by':'distance'}
    if at_ten:
        param['open_at'] = int(unixtime)
    # Check if location given
    if not location:
        data = simple_geoip.get_geoip_data()
        print(data)
        # By LAT LNG, then CITY
        loc = data.get('location')
        lat, lng = loc.get('lat'), loc.get('lng')
        city = loc.get('city')
        if lat and lng:
            param['latitude'] = lat
            param['longitude'] = lng
        elif city:
            param['location'] = city
        else:
            param['location'] = 'NYC'
    elif location:
        param['location'] = location
    return param

@application.route('/')
def index():
    title='10PM and 16 Missed Calls'
    response = render_template('index.html', title=title)
    return response

@application.route('/food')
def food():
    title='10PM and Let\'s Find Some Food'
    response = render_template('food.html', title=title)
    return response

@application.route('/results', methods =["GET", "POST"])
def results():
    if request.method == "POST":
       location = request.form.get("loc")
       type = request.form.get("type")
    if location and type:
        params = param_constructor(term=type, location=location, at_ten=False)
    else:
        params = param_constructor(at_ten=False)
    print(params)
    data = yelp_getter.yelp_request(url_params=params)
    # print(data)
    if data:
        places = data.get('businesses')
    display = []
    for place in places:
        name, link, img = place.get('alias'), place.get('url'), place.get('image_url')
        display.append((name, link, img))
    return jsonify(display)

# 404 Route
@application.errorhandler(404)
def not_found(e):
    response = render_template("404.html", title='Page not found')
    return response




if __name__ == '__main__':
    application.run(debug=True)
