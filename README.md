# sf_abnb_wizard_website

Marc Harvey - University of Illinois at Urbana/Champaign

---------------------------------------------------------------------------------------------------------------------------------------

This is a Django webapp that helps abnb owners maximize profits. It was made for a mindsumo challenge: https://www.mindsumo.com/contests/airbnb-sf?utm_campaign=solution_received_notification&utm_source=mindsumo&utm_medium=email

NOTE: The algorithms for price estimation and bookings optimization are implemented in price_estimation_script.py and bookings_optimization_script.py respectively. Additionally, the other algorithms used to analyze data and such, are also located in python files in the top directory.

---------------------------------------------------------------------------------------------------------------------------------------

My Algorithms:


----------------
Price Estimation
----------------
Assumptions

- ABnB's that are close in location to each other, are competitors, and thus sell at similar prices.

- When people rent ABnB's, they look to certain locations in SF, not the entirety of SF

- Capacity has a lot to do with price of an ABnB, as it divides the audience/consumer base. eg. someone who needs room for 2 people won't look for 4 people ABnB's

First, form a list of distances from user's location for every ABnB in listings.csv O(1)
    Using Haversines formula for surface distance between two points on a sphere
    
At the same time, form a list of all capacities (of people) of every listing in listings.csv, so that the file only needs to be opened once. Also, form a list of all weekly prices of every abb in listings.csv O(1)

Then, loop through the distances and capacities list, finding the closest abbs that have the same capacity.  Store the indexes of the distances/capacities that are the lowest/same in a list of length 'accuracy'. O(n^2) n=accuracy :(
    
Next,  compute a weighted average of all of the close abbs, by using the list of close indexes to find the distances (weights) and weekly prices.
    
That is the expected price of an ABnB based solely on location and capacity!


---------------------
Bookings Optimization
---------------------
Assumptions

- Day of purchase really effects price, as weekends and holidays are generally more expensive.

- The competitors of ABnBs are other ABnBs that are of same capacity that are open on the same days, and also are close in location.

- People stick to one area when renting ABnBs, not the entirety of SF

First. get a list of close ABnB indexes with same capacity, only now they must also be open on the specified day according to calendar.csv O(n^2) n=accuracy :(  Basically the same as price estimation method, but with an added conditional that ends up taking a lot more time

While doing this, also form a list of all ABnB prices on the specified day

Then, find the lowest price out of all the close ABnBs, and that is considered the bookings optimizing price.

---------------------------------------------------------------------------------------------------------------------------------------

Comments/Concerns

It needs to be said that the runtime complexity is atrocious. I understand that, but at the same time, I feel that my algorithms produce extremely accurate results. I'm sure there are ways to lower the complexity more than I already did (yeah, it was higher :( ), but I believe those changes would edit the fundamental way the algorithms work. In hindsight, I really wanted to add a cache, so that duplicate inputs would work instantly, but I didn't have time. Maybe in the not-so-distant future I'll implement one of those. 

I did however,  get around to doing some of the extra exercises, like the popularity calculation, and the investment strategy one. The neighborhood popularity one was suspiciously easy, as it was a one time parse through listings.csv, which had neighborhood and average review for each listing. The investment strategy problem still really stumps me though, as I didn't see any information involving property costs or the like, only information involving what the ABnBs sold for. So, I just implemented that, and showed which neighborhoods had the highest average revenue per bedroom, which is the best I could do with the data given.


I know my data visualizations are pretty wack, only displaying interesting metrics and not maps, and I hope the aesthetic and functionality of my site makes up for it. I really wanted a map for the results of pe and bo, or even for the inputs, but didn't have time to implement. It would be a good thing to add later though.

Another note, some of my assumptions are supported in the informatics section of the site, such as the average abnb price per day graph, which shows why differentiating by day in the booking optimization problem is so important.

---------------------------------------------------------------------------------------------------------------------------------------

CITATIONS (or my attempt at them)

G. van Rossum, Python tutorial, Technical Report CS-R9526, Centrum voor Wiskunde en Informatica (CWI), Amsterdam, May 1995.

Django (Version 1.5) [Computer Software]. (2013). Retrieved from https://djangoproject.com.


