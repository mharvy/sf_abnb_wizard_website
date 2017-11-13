from django.shortcuts import render_to_response
from bookings_optimization_script import super_function
from geopy.geocoders import GoogleV3



# SET FUNCTION ATTRIBUTES #
set_accuracy = 5
# This can be changed, but not easily, as the html of results page would need to be edited
# Also the complexity is atrocious so 'accuracy' (number of abbs compared to) should be really low, like even 5 is
# stretching it unfortunately

title = 'Bookings Optimization Tool'
explanation = 'This tool is used for finding the highest possible daily price to sell an ABnB at, while still having a ' \
              'booking every day/night. It looks at close ABnBs with the same capacity, and shows the lowest price they' \
              'are selling at, which is also where you should sell at. This ensures that everybody looking for ABnBs in' \
              'your area will choose you over your competitors.'
instructions = 'It is fairly simple to use this tool. First, input specific day in the yyyy-mm-dd format. This is ' \
               'because ABnB owners like to change their prices on certain days, like weekends and holidays and such.' \
               'Then, input a location, just like you would on googlemaps, meaning you can use addresses, coordinates,' \
               'etc. Then, select the capacity of people that your ABnB has, as this is a large factor how people ' \
               'choose ABnBs. Finally, press submit and the wizard ' \
               'will do his magic.'
listings_file = 'listings.csv'
calendar_file = 'calendar.csv'


def user_input(request):
    content = {
        'title': title,
        'explanation': explanation,
        'instructions': instructions,
    }
    return render_to_response('bookings_optimization_input.html', content)


def results(request):
    user_day = request.GET['user_day']
    user_location = request.GET['user_location']
    user_capacity = int(request.GET['num_capacity'])

    geolocator = GoogleV3()
    location = geolocator.geocode(user_location)
    user_long = location.longitude
    user_lati = location.latitude

    best_price, list_prices, list_ids, list_distances, list_pics, list_urls = super_function(listings_file,
                                                                                             calendar_file,
                                                                                             user_long,
                                                                                             user_lati,
                                                                                             user_capacity,
                                                                                             user_day,
                                                                                             set_accuracy)

    data = {
        'title': title,
        'day': user_day,
        'location': location,
        'long': user_long,
        'lati': user_lati,
        'capacity': user_capacity,

        'best_price': best_price,
        'list_prices': list_prices,
        'list_ids': list_ids,
        'list_distances': list_distances,
        'list_pics': list_pics,
        'list_urls': list_urls,
    }
    return render_to_response('bookings_optimization_result.html', data)
