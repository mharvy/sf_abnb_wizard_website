import csv
from itertools import islice


def generate_popularity(listings_file, neighborhood_file):

    neighborhood_popularity = {  # Each neighborhood has a list [total popularity points, total apartments]
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

    neighborhood_popularity_new = {}  # to be returned because having only one dict caused problems

    amount_considered = 0

    with open(listings_file, 'rt') as listings:

        reader1 = csv.reader(listings)

        for line in islice(reader1, 1, None):

            if line[39] in neighborhood_popularity and line[79] != '':

                neighborhood_popularity[line[39]][1] += 1
                neighborhood_popularity[line[39]][0] += int(line[79])
                amount_considered += 1

        for neighborhood in neighborhood_popularity:

            cur_stats = neighborhood_popularity[neighborhood]
            neighborhood_popularity[neighborhood] = cur_stats[0] / cur_stats[1]

        for neighborhood in neighborhood_popularity:

            neighborhood_popularity_new[neighborhood.replace(' ', '').replace('/', '')] = neighborhood_popularity[neighborhood]

    with open(neighborhood_file, 'w', newline='') as neighborhoods:

        writer1 = csv.writer(neighborhoods)

        for element in neighborhood_popularity_new:

            writer1.writerow([element, round(neighborhood_popularity_new[element], 1)])

    return 0


def main():
    #listings = input('listings file >  ')
    #neighborhoods = input('neighborhoods file >  ')
    #generate_popularity(listings, neighborhoods)
    generate_popularity('listings.csv', 'neighbourhoods.csv')


if __name__ == '__main__':
    main()
