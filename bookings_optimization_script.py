import csv
from itertools import islice
import price_estimation_script


def get_list_of_all_abb_ids():

    list_of_abb_ids = []

    with open('listings.csv', 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            list_of_abb_ids.append(line[0])

    return list_of_abb_ids


def get_close_abb_ids(nearby_location_positions):

    # Must have same number of bedrooms of course

    list_of_abb_ids = get_list_of_all_abb_ids()
    close_abb_ids = []

    for position in nearby_location_positions:

        close_abb_ids.append(list_of_abb_ids[position])

    return close_abb_ids


def get_close_abb_prices_on_day(close_abb_ids, day):

    # This function works, but calendar.csv is kindof wack. make sure that close_abb_ids is pretty big

    list_of_abb_prices = []

    with open('calendar.csv', 'rt') as calendar:

        reader1 = csv.reader(calendar)

        for abb_id in close_abb_ids:

            for line in islice(reader1, 1, None):

                if line[0] == abb_id and line[1] == day and line[2] == 't':

                    list_of_abb_prices.append(price_estimation_script.price_to_float(line[3]))
                    continue

            list_of_abb_prices.append(0)

    return list_of_abb_prices


def list_all_prices_on_day(calendar_file, day):

    # This function is extremely important to the success of this whole bookings optimization project.
    # I have feelings toward it that rival those of a proud father toward his baby firstborn son, despite
    # it having a rather horrid complexity. I am willing to see past the flaws because I love it, and it is
    # pretty damn accurate if the assumptions I'm basing this whole thing on are correct.

    # Important note: we could just form the list_of_ids within this function, but that would be counter-
    # intuitive, since we will want to display the close ids on the webpage, and this way we only have to
    # form the list once, and thereafter can just call it in our function (our/we = my/me  :( )

    list_of_calendar_prices = []

    with open(calendar_file, 'rt') as calendar:

        reader1 = csv.reader(calendar)

        for line in islice(reader1, 1, None):

            if line[1] == day:

                list_of_calendar_prices.append(price_estimation_script.price_to_float(line[3]))

    # There was a ton of useless stuff in this function that has just been removed. In fact, I removed a nested for-loop
    # with a complexity of like 2^n or something so this whole app should run much faster now

    return list_of_calendar_prices


def list_csv_positions_advanced(user_long, user_lati, people, list_of_all_prices_on_day, num_locations):

    # 'advanced' in that it only lists indexes of abnbs that are open on the specified day

    list_of_capacity = price_estimation_script.get_list_of_capacity()
    closest_location_pos = []
    j = 0

    for k in list_of_capacity:

        if int(k) == people:
            closest_location_pos.append(j)

        if len(closest_location_pos) == num_locations:
            break

        j += 1

    list_of_distances_from_user_location = price_estimation_script.get_list_of_distances(user_long, user_lati)

    for cur_distance in list_of_distances_from_user_location:

        i = 0

        for cur_pos in closest_location_pos:

            cur_index = list_of_distances_from_user_location.index(cur_distance)

            if cur_distance < list_of_distances_from_user_location[cur_pos] and cur_index not in closest_location_pos \
                    and list_of_all_prices_on_day[cur_index] != 0:

                if int(list_of_capacity[cur_index]) == people:
                    closest_location_pos[i] = list_of_distances_from_user_location.index(cur_distance)

            i += 1

    return closest_location_pos


def get_bookings_maximizing_price(closest_location_pos, list_of_all_prices_on_day):

    lowest_price = 100000

    for index in closest_location_pos:

        if list_of_all_prices_on_day[index] < lowest_price:

            lowest_price = list_of_all_prices_on_day[index]

    return lowest_price


def super_function(listings_file, calendar_file, user_long, user_lati, people, user_day, num_locations):
    # This is my attempt to cut the runtime a lot by combining all the functions, parsing each csv file only once
    # Also, it should return some sort of dict so that my views file can easily use it
    closest_location_pos = []
    closest_location_distances = []
    closest_location_ids = []
    closest_location_urls = []
    closest_location_pics = []
    closest_location_prices = []

    list_of_distances_from_user_location = []
    list_of_abb_capacities = []
    list_of_abb_ids = []
    list_of_abb_urls = []  # I'm really want to include links to the close cheap AirBnB's, so I'll need this
    list_of_abb_pics = []  # This would be pretty cool too so im going to add this for now

    with open(listings_file, 'rt') as listings:  # Only time I will open and go through listings

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            list_of_abb_capacities.append(line[53])
            list_of_abb_ids.append(line[0])
            list_of_abb_urls.append(line[1])
            list_of_abb_pics.append(line[17])

            abb_longitude = float(line[49])
            abb_latitude = float(line[48])
            distance_from_location = price_estimation_script.get_distance_from_user_location(user_long, user_lati, abb_longitude, abb_latitude)
            list_of_distances_from_user_location.append(distance_from_location)

    list_of_all_prices_on_day = list_all_prices_on_day(calendar_file, user_day)

    j = 0
    for k in list_of_abb_capacities:

        if int(k) == people:
            closest_location_pos.append(j)
            closest_location_distances.append(list_of_distances_from_user_location[j])
            closest_location_ids.append(list_of_abb_ids[j])
            closest_location_urls.append(list_of_abb_urls[j])
            closest_location_pics.append(list_of_abb_pics[j])
            closest_location_prices.append(list_of_all_prices_on_day[j])

        if len(closest_location_pos) == num_locations:
            break

        j += 1

    for cur_distance in list_of_distances_from_user_location:

        i = 0

        for cur_pos in closest_location_pos:

            cur_index = list_of_distances_from_user_location.index(cur_distance)

            if cur_distance < list_of_distances_from_user_location[cur_pos] and cur_index not in closest_location_pos \
                    and list_of_all_prices_on_day[cur_index] != 0:

                if int(list_of_abb_capacities[cur_index]) == people:
                    closest_location_pos[i] = list_of_distances_from_user_location.index(cur_distance)
                    closest_location_distances[i] = list_of_distances_from_user_location[closest_location_pos[i]]
                    closest_location_ids[i] = list_of_abb_ids[closest_location_pos[i]]
                    closest_location_urls[i] = list_of_abb_urls[closest_location_pos[i]]
                    closest_location_pics[i] = list_of_abb_pics[closest_location_pos[i]]
                    closest_location_prices[i] = list_of_all_prices_on_day[closest_location_pos[i]]

            i += 1

    for i in range(0, num_locations - 2):
        for j in range(i, num_locations - 1):
            if closest_location_prices[i] > closest_location_prices[j]:
                closest_location_prices[i], closest_location_prices[j] = closest_location_prices[j], \
                                                                         closest_location_prices[i]
                closest_location_ids[i], closest_location_ids[j] = closest_location_ids[j], \
                                                                         closest_location_ids[i]
                closest_location_urls[i], closest_location_urls[j] = closest_location_urls[j], \
                                                                         closest_location_urls[i]
                closest_location_pics[i], closest_location_pics[j] = closest_location_pics[j], \
                                                                         closest_location_pics[i]
                closest_location_distances[i], closest_location_distances[j] = closest_location_distances[j], \
                                                                     closest_location_distances[i]

    b_maxing_price = closest_location_prices[0]

    return b_maxing_price, closest_location_prices, closest_location_ids, closest_location_distances, \
           closest_location_pics, closest_location_urls
