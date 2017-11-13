# basically, find average price per bedroom for each neighborhood, and compare them.
# the one that has the highest will be labeled as the most profitable

# i don't really like this method, as it doesn't take any cost into consideration. however, how there was no supplied
# data that had property values and whatnot, which would really help make a tool like this quite accurate

# in fact, ill probably have to provide a disclaimer explaining the absence of cost consideration

# an important note is that i am taking bedrooms into account instead of accommodations on this one.
# i decided to do this because this is an investment problem, and bedrooms can't be changed easily, but accommodations
# can be. all one would need to do is like add a bigger bed or something and say it fits 2. bedrooms are a better solid
# variable for housing in this case i would say


import csv
from price_estimation_script import price_to_float
from itertools import islice


def float_to_price(float):
    price = str(float)
    last_index = price.find('.') + 3
    return '$' + price[0: last_index]


def strategize(listings_file, neighborhood_file):

    neighborhood_returns = {  # Each neighborhood has a list [total price/bedrooms, total apartments]
        'Bayview': [0, 0],
        'Bernal Heights': [0, 0],
        'Castro/Upper Market': [0, 0],
        'Chinatown': [0, 0],
        'Crocker Amazon': [0, 0],
        'Diamond Heights': [0, 0],
        'Downtown/Civic Center': [0, 0],
        'Excelsior': [0, 0],
        'Financial District': [0, 0],
        'Glen Park': [0, 0],
        'Golden Gate Park': [0, 0],
        'Haight Ashbury': [0, 0],
        'Inner Richmond': [0, 0],
        'Inner Sunset': [0, 0],
        'Lakeshore': [0, 0],
        'Marina': [0, 0],
        'Mission': [0, 0],
        'Nob Hill': [0, 0],
        'Noe Valley': [0, 0],
        'North Beach': [0, 0],
        'Ocean View': [0, 0],
        'Outer Mission': [0, 0],
        'Outer Richmond': [0, 0],
        'Outer Sunset': [0, 0],
        'Pacific Heights': [0, 0],
        'Parkside': [0, 0],
        'Potrero Hill': [0, 0],
        'Presidio': [0, 0],
        'Presidio Heights': [0, 0],
        'Russian Hill': [0, 0],
        'Seacliff': [0, 0],
        'South of Market': [0, 0],
        'Treasure Island/YBI': [0, 0],
        'Twin Peaks': [0, 0],
        'Visitacion Valley': [0, 0],
        'West of Twin Peaks': [0, 0],
        'Western Addition': [0, 0],
    }

    with open(listings_file, 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            cur_neighborhood = line[39]
            if line[55] == '':
                continue
            cur_bedrooms = int(line[55])
            if cur_bedrooms == 0:
                continue
            if len(line[60]) != 0:
                cur_price = price_to_float(line[60])
            else:
                cur_price = price_to_float(line[61]) / 7
            cur_avg_price_per_bedroom = cur_price / cur_bedrooms

            if cur_neighborhood in neighborhood_returns:

                neighborhood_returns[cur_neighborhood][0] += cur_avg_price_per_bedroom
                neighborhood_returns[cur_neighborhood][1] += 1

    for neighborhood in neighborhood_returns:

        cur_numerator = neighborhood_returns[neighborhood][0]
        cur_denominator = neighborhood_returns[neighborhood][1]

        neighborhood_returns[neighborhood] = cur_numerator / cur_denominator

    for neighborhood in neighborhood_returns:

        if ' 'or '/' in neighborhood:
            neighborhood_returns[neighborhood.replace(' ', '').replace('/', '')] = neighborhood_returns.pop(neighborhood)

    cur_best_neighborhood = 'Bayview'

    for neighborhood in neighborhood_returns:

        if neighborhood_returns[neighborhood] > neighborhood_returns[cur_best_neighborhood]:

            cur_best_neighborhood = neighborhood

    for neighborhood in neighborhood_returns:

        cur_float = neighborhood_returns[neighborhood]
        neighborhood_returns[neighborhood] = float_to_price(cur_float)

    with open(neighborhood_file, 'w', newline='') as neighborhoods:

        writer1 = csv.writer(neighborhoods)

        for element in neighborhood_returns:

            writer1.writerow([element, neighborhood_returns[element]])

        writer1.writerow(['best_neighborhood', cur_best_neighborhood])
        writer1.writerow(['best_neighborhood_price', neighborhood_returns[cur_best_neighborhood]])

    return 0
