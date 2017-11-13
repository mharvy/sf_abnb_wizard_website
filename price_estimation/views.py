from django.shortcuts import render_to_response
from price_estimation_script import super_function
from investment_strategy import float_to_price
from geopy.geocoders import GoogleV3


# SET FUNCTION ATTRIBUTES #
accuracy = 5
title = 'Price Estimation Tool'
explanation = 'This tool takes the prices of close airbnbs and find the weighted average them, determining an expected ' \
              'price for an AirBnB of any capacity or location with San Fransisco. It is very accurate, but needs to ' \
              'parse, through a lot of data, and thus may take up to 5 seconds to display results.'
instructions = 'It is fairly simple to use this tool. First, input a location within SF, just as you would in google' \
               'maps, meaning you can use addresses, coordinates, etc. Then, select the capacity of people that this ' \
               'ABnB has, as this is a large factor in price. Finally, press submit and the wizard will do his magic.'
listings_file = 'listings.csv'


def user_input(request):

    content = {
        'title': title,
        'explanation': explanation,
        'instructions': instructions,
    }

    return render_to_response('price_estimation_input.html', content)


def results(request):

    # DYNAMIC ATTRIBUTES #

    user_capacity = int(request.GET['num_capacity'])
    user_location = request.GET['user_location']
    geolocator = GoogleV3()
    location = geolocator.geocode(user_location)
    user_long = location.longitude
    user_lati = location.latitude

    expected_price, list_ids, list_prices, list_urls, list_pics = super_function('listings.csv',
                                                                                 user_long,
                                                                                 user_lati,
                                                                                 user_capacity,
                                                                                 accuracy)
    data = {
        'title': title,
        'location': user_location,
        'long': user_long,
        'lati': user_lati,
        'capacity': user_capacity,

        'expected_price': float_to_price(expected_price),
        'list_ids': list_ids,
        'list_prices': list_prices,
        'list_urls': list_urls,
        'list_pics': list_pics,
    }

    return render_to_response('price_estimation_result.html', data)
