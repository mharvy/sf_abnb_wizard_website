import csv
import datetime
from itertools import islice
from price_estimation_script import price_to_float


def get_avg_price_per_day_of_week(calendar_file, target_file):

    daysofweek = [
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
        [0, 0],
    ]

    with open(calendar_file, 'rt') as calendar:

        reader1 = csv.reader(calendar)

        for line in islice(reader1, 1, None):
            date = line[1]
            year, month, day = (int(x) for x in date.split('-'))
            dayofweek = datetime.date(year, month, day).weekday()
            if line[2] != 'f':
                daysofweek[dayofweek][0] = daysofweek[dayofweek][0] + price_to_float(line[3])
                daysofweek[dayofweek][1] = daysofweek[dayofweek][1] + 1

    for i in range(0, 7):
        daysofweek[i] = round(daysofweek[i][0] / daysofweek[i][1], 2)

    with open(target_file, 'w', newline="") as target:

        writer1 = csv.writer(target)

        writer1.writerow(['Monday', daysofweek[0]])
        writer1.writerow(['Tuesday', daysofweek[1]])
        writer1.writerow(['Wednesday', daysofweek[2]])
        writer1.writerow(['Thursday', daysofweek[3]])
        writer1.writerow(['Friday', daysofweek[4]])
        writer1.writerow(['Saturday', daysofweek[5]])
        writer1.writerow(['Sunday', daysofweek[6]])

    return 0


get_avg_price_per_day_of_week('calendar.csv', 'avg_daily_prices.csv')
