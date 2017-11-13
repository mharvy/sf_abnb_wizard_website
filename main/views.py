from django.shortcuts import render_to_response
import csv
from investment_strategy import strategize


def create_long_string(file):
    long_string = ''
    with open(file, 'rt') as explanation:
        for line in explanation:
            long_string = long_string + line
    return long_string


# SITE INFORMATION
site_name = 'AirBnB Wizard'
author_name = 'Marc Harvey'
author_age = 'Freshman'
author_school = 'University of Illinois at Urbana-Champaign'

listings_file = 'listings.csv'
greeting = create_long_string('main_page_greeting.txt')
main_info = create_long_string('main_page_text.txt')
pe_greeting = create_long_string('main_pe_greeting.txt')
bo_greeting = create_long_string('main_bo_greeting.txt')
inv_greeting = create_long_string('main_inv_greeting.txt')
inf_greeting = create_long_string('main_inf_greeting.txt')
about_greeting = create_long_string('main_about_greeting.txt')


def homepage(request):

    content = {
        'site_name': site_name,
        'greeting': greeting,
        'main_info': main_info,
        'pe_info': pe_greeting,
        'bo_info': bo_greeting,
        'inv_info': inv_greeting,
        'inf_info': inf_greeting,
        'about_info': about_greeting,
    }

    return render_to_response('homepage.html', content)


def make_dict_from_nb_csv(csv_file):

    gucci_dict = {}

    with open(csv_file, 'rt') as neighborhoods:

        reader1 = csv.reader(neighborhoods)

        for line in reader1:

            gucci_dict[line[0]] = line[1]

    return gucci_dict


def infopage(request):

    content = {**make_dict_from_nb_csv('neighbourhoods.csv'), **make_dict_from_nb_csv('neighborhood_returns.csv')}

    return render_to_response('informatics.html', content)


def invepage(request):

    content = make_dict_from_nb_csv('neighborhood_returns.csv')

    return render_to_response('investpage.html', content)


def aboutpage(request):

    content = {
        'site_name': site_name,
        'author_name': author_name,
        'author_age': author_age,
        'author_school': author_school,
    }

    return render_to_response('aboutpage.html', content)


def waitpage(request):

    return render_to_response('waitpage.html')
