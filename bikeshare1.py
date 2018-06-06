import time
import pandas
import datetime
import calendar
from datetime import timedelta
## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'
def get_city():
    '''Asks the user for a city and returns the filename for that city's bike share data.
    Args:
        none.
    Returns:
        (str) Filename for a city's bikeshare data.
    '''
    city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n').lower()
    if city == "chicago":
        return chicago
    elif city == "new york":
        return new_york_city
    elif city == "washington":
        return washington
    else:
        print("invalid location")
        get_city()
def get_time_period():
    '''Asks the user for a time period and returns the specified filter.
    Args:
        none.
    Returns:
        (str) The filter time period requirements
    '''
    while True :
        time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n').lower()
        if time_period not in ('month', 'day', 'none' ):
            print("Not an appropriate choice.")
        else:
            return time_period.lower()

def get_month():
    '''Asks the user for a month and returns the specified month.
    Args:
        none.
    Returns:
        (str) The month the user is interested in
    '''
    month = input('\nWhich month? January, February, March, April, May, or June?\nPlease type your response as an integer.\n')
    nums = ['1','2','3','4','5','6']
    if month in nums:
        return int(month)
    else:
        print("Not an appropriate choice.")
        get_month()

def get_day(month):
    '''Asks the user for a day and returns the specified day.
    Args:
        none.
    Returns:
        (int) The day the user is interested in
    '''
    day = input('\nWhich day? Please type your response as an integer.\n')

    mods = ['1','2','3','4','5','6','7']
    if day in mods :
        return int(day)
    else:
        print("Not an appropriate choice.")
        get_day(month)

def find_highest_index(array):
    '''Finds the index of the highest number in an array
    Args:
        array to be searched
    Returns:
        (int) the index of the highest number
    '''
    max_val = max(array)
    max_idx = array.index(max_val)
    return max_idx
def filter_dataset(city_data, filter_array):
    '''Filters the city file based on the time filter input by user
    Args:
        (dataframe) the data extracted from the city_file
        (array) the filter requirements input by user
    Return:
        (dataframe) the filtered data
    '''
    df = city_data
    if filter_array[2]:
        filter_from = datetime.datetime(2017,filter_array[1], filter_array[2])
        filter_to = filter_from + timedelta(days = 1)
    else:
        filter_from = datetime.datetime(2017,filter_array[1], 1)
        filter_to = (filter_from.replace(day=28) + timedelta(days=4))
        filter_to = filter_to.replace(day=1)
        print(filter_to)
    filtered = df[(df['Start Time'] >= str(filter_from)) & (df['Start Time'] <= str(filter_to))]
    return filtered
def popular_month(city_data):
    '''DESCRIPTION
    Args:
        (dataframe) The data table for the city of interest
    Returns:
        (str) The name of the most popular month
    '''
    start_times = city_data.xs('Start Time', axis = 1)
    months = [0]*12
    for dates in start_times:
        months[int(dates.split()[0].split("-")[1])-1] += 1
    return calendar.month_name[find_highest_index(months)+1]
def popular_day(city_data):
    '''Calculates the most popular day of the week for bikeshare usage
    Args:
        (dataframe) The data from city of interest
    Returns:
        (str) The name of the most popular day
    '''
    start_times = city_data.xs('Start Time', axis = 1)
    day_of_week = [0]*7
    for i in start_times:
        year_month_day = i.split()[0]
        year, month, day = (int(x) for x in year_month_day.split("-"))
        day_of_week[(datetime.date(year, month, day).weekday())] +=1
    return calendar.day_name[find_highest_index(day_of_week)]
def popular_hour(city_data):
    '''Calculates the most popular hour to start a ride
    Args:
        (dataframe) the data from the city of interest
    Returns:
        (str) The hour (in 24 hour format) of the most popular start time
    '''
    start_times = city_data.xs('Start Time', axis = 1)
    hours = [0]*25
    for dates in start_times:
        hours[int(dates.split()[1].split(":")[0])-1] += 1
    return str(find_highest_index(hours))
def seconds_converter(seconds):
    '''Used for trip_duration(city_data), converts seconds into (hours minutes seconds)
    Args:
        seconds -- amount of seconds
    Returns:
        (str) Tells user the amount of time
    '''
    # divmod docs: https://docs.python.org/2/library/functions.html#divmod
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return '%d Days %02d Minutes and %02d seconds' % (h, m, s)
def trip_duration(city_data):
    '''Calculates the total and average trip time
    Args
        (dataframe) the data from the city of interest
    Returns:
        (array) An array containing time delta of totaltime and average time
    '''
    calc_mean = round(city_data['Trip Duration'].mean())
    calc_duration = city_data['Trip Duration'].sum()
    mean = seconds_converter(calc_mean)
    total = seconds_converter(calc_duration)
    return total, mean
def popular_stations(city_data):
    '''Finds the most popular start and end stations
    Args:
        (dataframe) the data from the city of interest
    Returns:
        (Array) An array where index 0 is most popular start station
        and index 1 is most popular end station
    '''
    return_array = []
    start_dict = {}
    end_dict = {}
    start_stations = city_data.xs("Start Station", axis = 1)
    end_stations = city_data.xs("End Station", axis = 1)
    for station in start_stations:
        if station not in start_dict:
            start_dict[station] = 1
        else:
            start_dict[station] += 1
    value = list(start_dict.values())
    key = list(start_dict.keys())
    return_array.append(key[value.index(max(value))])
    for station in end_stations:
        if station not in end_dict:
            end_dict[station] = 1
        else:
            end_dict[station] += 1
    value = list(end_dict.values())
    key = list(end_dict.keys())
    return_array.append(key[value.index(max(value))])
    return return_array
def popular_trip(city_data):
    '''Finds the most popular trip
    Args:
        (dataframe) the data from the city of interest
    Returns:
        (str) The most popular trip including 'to' between stations
    '''
    start_stations = city_data.xs("Start Station", axis = 1)
    end_stations = city_data.xs("End Station", axis = 1)
    trips = start_stations + " to " + end_stations
    trip_dict = {}
    for trip in trips:
        if trip not in trip_dict:
            trip_dict[trip]=1
        else:
            trip_dict[trip]+=1
    value = list(trip_dict.values())
    key = list(trip_dict.keys())
    return key[value.index(max(value))]
def users(city_data):
    '''tallies up counts of user types
    Args:
        (dataframe) the data from the city of interest
    Returns:
        (dictionary) dictionary where key is user type, value is number
    '''
    user_dict = {"Subscriber": 0, "Customer": 0}
    users = city_data.xs("User Type", axis = 1)
    for user in users:
        if user not in user_dict:
            user_dict[user] = 1
        else:
            user_dict[user] +=1
    return user_dict
def gender(city_data):
    '''Tallies up gender counts
    Args:
        (dataframe) the data from the city of interest
    Returns:
        (array) array[0] = male counts, array[1] = female count
    '''
    return_array = [0]*2
    genders = city_data.xs("Gender", axis = 1)
    for gender in genders:
        if gender == "Male":
            return_array[0] += 1
        if gender == "Female":
            return_array[1] += 1
    return return_array
def birth_years(city_data):
    '''Finds the most popular birth year, as well as the year of the oldest and youngest user
    Args:
        (dataframe) the data from the city of interest
    Returns:
        (array) index 0= most popular birth year, index 1= birth year of oldest user
        index 2= birth year of youngest user
    '''
    return_array = []
    year_dict = {}
    years = city_data.xs("Birth Year", axis = 1).dropna()
    for year in years:
        year = int(year)
        if year not in year_dict:
            year_dict[year] = 1
        else:
            year_dict[year] += 1
    value = list(year_dict.values())
    key = list(year_dict.keys())
    return_array.append(key[value.index(max(value))]) #most popular year
    sorted_years = sorted(year_dict.keys())
    return_array.append(sorted_years[0])  #birth year of oldest user
    return_array.append(sorted_years[-1]) #birth year of youngest user
    return return_array
def display_data(city_data):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.
    Args:
        (dataframe) the data from the city of interest
    Returns:
        none.
    '''
    display = input('\nWould you like to view individual trip data?'
                    'Type \'yes\' or \'no\'.\n')
    i = 0
    while display.lower() == 'yes':
        print(city_data[i:i+4])
        i += 5
        display = input("\nWould you like to view five more lines?"
                         "Type 'yes' or 'no'.\n")
def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    city_file = get_city()
    city_file
    time_period = get_time_period()
    filter_array = [None, None, None]
    if time_period == "month":
        filter_array = [time_period, get_month(), None]
    elif time_period == "day":
        filtermonth = get_month
        filter_array = [time_period, get_month(), get_day(filtermonth)]
    print("Converting the %s. data file to table and filtering for time period" % city_file)
    start_time = time.time()
    city_data = pandas.read_csv(city_file)
    city_data.sort_values(by = "Start Time")
    if filter_array[1]:
        city_data = filter_dataset(city_data, filter_array)
    print("That took %s seconds." % (time.time() - start_time))
    print('Calculating the first statistic...')
    # What is the most popular month for start time?
    if time_period == 'none':
        start_time = time.time()
        print("the most popular month is: " + popular_month(city_data))
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")
    # What is the most popular day of week (Monday, Tuesday, etc.) for start time?
    if time_period == 'none' or time_period == 'month':
        start_time = time.time()
        print("The most popular day of the week is: " + popular_day(city_data))
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")
    start_time = time.time()
    # What is the most popular hour of day for start time?
    print("The most popular hour of day to start is: " + popular_hour(city_data))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    # What is the total trip duration and average trip duration?
    total, mean = trip_duration(city_data)
    print("The total trip duration is :{} and the average trip duration is: {} ".format(total,mean))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    # What is the most popular start station and most popular end station?
    stations = popular_stations(city_data)
    print("The most popular start station is: {} \nEnd station: {} ".format(stations[0],stations[1]))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    # What is the most popular trip?
    print("The most popular trip is: " + popular_trip(city_data))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    # What are the counts of each user type?
    print('Counts of each user type:\n' + str(users(city_data)))
    print("That took %s seconds." % (time.time() - start_time))
    print("Calculating the next statistic...")
    start_time = time.time()
    # What are the counts of gender?
    if city_file != "washington.csv":
        male_female = gender(city_data)
        print("Gender counts:\nMale: {}     Female: {} ".format(male_female[0],male_female[1]))
        print("That took %s seconds." % (time.time() - start_time))
        print("Calculating the next statistic...")
        start_time = time.time()
    # What are the earliest (i.e. oldest user), most recent (i.e. youngest user), and
    # most popular birth years?
        ages = birth_years(city_data)
        print("The most popular birth year: {} \nOldest user's birth year: {} \n"
              "Youngest user's birth year: {}".format(ages[0],ages[1],ages[2]))
        print("That took %s seconds." % (time.time() - start_time))
    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_data)
    # Restart?
    restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
    if restart.lower() == 'yes':
        statistics()
if __name__ == "__main__":
    statistics()
