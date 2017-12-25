import csv
from math import sqrt, radians, sin, cos, asin
from itertools import islice


def get_distance_from_user_location(user_long, user_lati, long, lati):

    # Haversines formula for finding surface distance between 2 points on sphere

    earth_radius = 6371
    long1 = radians(user_long)
    lati1 = radians(user_lati)
    long2 = radians(long)
    lati2 = radians(lati)

    return 2 * earth_radius * asin(
        sqrt((sin((lati2 - lati1) / 2) ** 2) + cos(lati1) * cos(lati2) * (sin((long2 - long1) / 2) ** 2)))


def price_to_float(price):

    if len(price) > 0:
        return float(price.strip('$').replace(',', ''))
    return 0


def get_list_of_distances(user_long, user_lati):

    list_of_distances_from_user_location = []

    with open('listings.csv', 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            abb_longitude = float(line[49])
            abb_latitude = float(line[48])
            distance_from_location = get_distance_from_user_location(user_long, user_lati, abb_longitude, abb_latitude)
            list_of_distances_from_user_location.append(distance_from_location)

    return list_of_distances_from_user_location


def get_list_of_capacity():  # Capacity of people

    list_of_capacity = []

    with open('listings.csv', 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            list_of_capacity.append(line[53])

    return list_of_capacity


def get_list_of_weekly_prices():

    list_of_weekly_prices = []

    with open('listings.csv', 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            if len(line[61]) > 0:

                cur_weekly_price = price_to_float(line[61])

            else:

                cur_weekly_price = price_to_float(line[60]) * 7

            list_of_weekly_prices.append(cur_weekly_price)

    return list_of_weekly_prices


def list_csv_positions(user_long, user_lati, people, num_locations):

    list_of_capacity = get_list_of_capacity()
    closest_location_pos = []
    j = 0

    for k in list_of_capacity:

        if int(k) == people:

            closest_location_pos.append(j)

        if len(closest_location_pos) == num_locations:

            break

        j += 1

    list_of_distances_from_user_location = get_list_of_distances(user_long, user_lati)

    for cur_distance in list_of_distances_from_user_location:

        i = 0

        for cur_pos in closest_location_pos:

            cur_index = list_of_distances_from_user_location.index(cur_distance)

            if cur_distance < list_of_distances_from_user_location[cur_pos] and cur_index not in closest_location_pos:

                if int(list_of_capacity[cur_index]) == people:

                    closest_location_pos[i] = list_of_distances_from_user_location.index(cur_distance)

            i += 1

    return closest_location_pos


def get_price(user_long, user_lati, people, accuracy):    # Accuracy is weird in this function. 1 mean 2 and stuff

    list_of_distances_from_user_location = get_list_of_distances(user_long, user_lati)
    nearby_location_positions = list_csv_positions(user_long, user_lati, people, accuracy + 1)
    list_of_weekly_prices = get_list_of_weekly_prices()

    max_distance = list_of_distances_from_user_location[nearby_location_positions[len(nearby_location_positions) - 1]]

    numerator = 0
    denominator = 0

    if accuracy == 0:

        return 0

    for i in nearby_location_positions:

        cur_distance = list_of_distances_from_user_location[i]
        numerator = numerator + (list_of_weekly_prices[i] * (max_distance - cur_distance))
        denominator = denominator + (max_distance - cur_distance)

    return numerator / denominator  # Weighted average of the 5 close airbbs (technically 4)


def get_price_efficient(nearby_location_positions, list_of_distances_from_user_location, list_of_weekly_prices):

    numerator = 0
    denominator = 0
    max_distance = list_of_distances_from_user_location[nearby_location_positions[len(nearby_location_positions) - 1]]

    for i in nearby_location_positions:

        cur_distance = list_of_distances_from_user_location[i]
        numerator = numerator + (list_of_weekly_prices[i] * (max_distance - cur_distance))
        denominator = denominator + (max_distance - cur_distance)

    answer = numerator / denominator

    return answer


def super_function(listings_file, user_long, user_lati, user_capacity, accuracy):

    list_of_distances_from_user_location = []
    list_all_capacity = []
    list_of_weekly_prices = []
    list_all_ids = []
    list_all_urls = []
    list_all_pics = []

    with open(listings_file, 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            abb_longitude = float(line[49])
            abb_latitude = float(line[48])
            distance_from_location = get_distance_from_user_location(user_long, user_lati, abb_longitude, abb_latitude)
            list_of_distances_from_user_location.append(distance_from_location)

            if len(line[61]) > 0:

                cur_weekly_price = price_to_float(line[61])

            else:

                cur_weekly_price = price_to_float(line[60]) * 7

            list_of_weekly_prices.append(cur_weekly_price)
            list_all_capacity.append(line[53])
            list_all_ids.append(line[0])
            list_all_urls.append(line[1])
            list_all_pics.append(line[17])

    closest_location_pos = []
    list_prices = []
    list_ids = []
    list_urls = []
    list_pics = []

    j = 0
    for k in list_all_capacity:  # This is basically to 'initialize' the closest_location_pos so it can be compared to

        if int(k) == user_capacity:

            closest_location_pos.append(j)
            list_prices.append(list_of_weekly_prices[j])
            list_ids.append(list_all_ids[j])
            list_urls.append(list_all_urls[j])
            list_pics.append(list_all_pics[j])

        if len(closest_location_pos) == accuracy:

            break

        j += 1

    for cur_distance in list_of_distances_from_user_location:

        i = 0
        for cur_pos in closest_location_pos:

            cur_index = list_of_distances_from_user_location.index(cur_distance)

            if cur_distance < list_of_distances_from_user_location[cur_pos] and cur_index not in closest_location_pos:

                if int(list_all_capacity[cur_index]) == user_capacity:

                    closest_location_pos[i] = cur_index
                    list_prices[i] = list_of_weekly_prices[cur_index]
                    list_ids[i] = list_all_ids[cur_index]
                    list_urls[i] = list_all_urls[cur_index]
                    list_pics[i] = list_all_pics[cur_index]

            i += 1

    numerator = 0
    denominator = 0
    max_distance = list_of_distances_from_user_location[closest_location_pos[len(closest_location_pos) - 1]]

    k = 0
    for i in closest_location_pos:

        cur_distance = list_of_distances_from_user_location[i]
        numerator = numerator + (list_prices[k] * (max_distance - cur_distance))
        denominator = denominator + (max_distance - cur_distance)
        k += 1

    answer = numerator / denominator

    return answer, list_ids, list_prices, list_urls, list_pics


# NEW WORK 12 24 17
# creating  class wil drastically minimize the lines required for this program, as well as will teach me an important
# lesson.
# to make the efficiency better or whatever, this definitely needs a recursive function

class abnb():

    def __init__(self, line):
        self.id = line[0]
        self.lati = line[48]
        self.long = line[49]
        self.capacity = line[53]
        self.url = line[1]
        self.pic = line[17]
        if len(line[61]) > 0:
            self.price = line[61]
        else:
            self.price = line[60] * 7
