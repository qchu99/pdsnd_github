import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv', # Key changed from 'new york city' to 'new york' to conform with user prompt
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Ask user to input city, and loop until valid input is entered
    city = input('\nWould you like to see data from Chicago, New York or Washington?\n').lower()
    while city not in CITY_DATA.keys():
        city = input('\nPlease enter valid city (i.e., Chicago, New York or Washington).\n').lower()

    # Ask user to choose filter by month and/or day, and loop until valid input is entered
    filter = input('\nWould you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n').lower()
    while filter not in ['month', 'day', 'both', 'none']:
        filter = input('\nPlease try again. The input must be month, day, both or none.\n').lower()

    # Set default to no filter, with changes made by the following IF statements
    month = 'all'
    day = 'all'

    # Ask user to enter month if either 'month' or 'both' is inputed as filter, and loop until valid entry
    if filter == 'month' or filter == 'both':
        month = input('\nWhich month? January, February, March, April, May or June?\n').lower()
        while month not in ['january', 'february', 'march', 'april', 'may', 'june']:
            month = input('\nPlease enter valid month (i.e., January - June)\n').lower()

    # Create dictionary for days of week and corresponding abbreviations
    day_dict = {'M': 'monday', 'Tu': 'tuesday', 'W': 'wednesday', 'Th': 'thursday', 'F': 'friday', 'Sa': 'saturday', 'Su': 'sunday'}

    # Ask user to enter day if either 'day' or 'both' is inputed as filter, and loop until valid entry
    # Convert abbreviations to days of week
    if filter == 'day' or filter == 'both':
        day_index = input('\nWhich day? Please type a day M, Tu, W, Th, F, Sa, Su.\n')
        while day_index not in ['M', 'Tu', 'W', 'Th', 'F', 'Sa', 'Su']:
            day_index = input('\nPlease enter valid day (i.e., M, Tu, W, Th, F, Sa, Su.\n')
        day = day_dict[day_index]

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month to create new dataframe, if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    # filter by day of week to create new dataframe, if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # find and display the most popular month by converting index to name of month
    month_index = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[month_index - 1]
    print('\nThe most popular month to travel is {}\n'.format(popular_month))

    # find and display the most common day of week
    popular_dayofweek = df['day_of_week'].mode()[0]
    print('\nThe most popular day of week to travel is {}\n'.format(popular_dayofweek))

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find and display the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('\nThe most popular hour to start your travel is {}\n'.format(popular_hour))

    # calculate and display computing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # find and display most commonly used start station
    popular_startstation = df['Start Station'].mode()[0]
    print('\nThe most popular start station is {}\n'.format(popular_startstation))

    # find and display most commonly used end station
    popular_endstation = df['End Station'].mode()[0]
    print('\nThe most popular end station is {}\n'.format(popular_endstation))

    # combine Start Station and End Station to create Route column
    df['Route'] = df['Start Station'] + ' to ' + df['End Station']

    # find and display most frequent combination of start station and end station trip
    popular_route = df['Route'].mode()[0]
    print('\nThe most popular route is {}\n'.format(popular_route))

    # calculate and display computing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # calculate and display total travel time in days, hours, minutes and seconds (looked up timedelta function in Stackoverflow)
    travel_secs = float(df['Trip Duration'].sum())
    duration = str(datetime.timedelta(seconds=travel_secs))
    print('\nTotal travel time is {}.'.format(duration))

    # calculate and display mean travel time in minutes and seconds
    avg_mins, avg_secs = divmod(df['Trip Duration'].mean(), 60)
    print('\nAverage travel time is {} minutes and {} seconds.'.format(int(avg_mins), int(avg_secs)))

    # calculate and display computing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # calculate and display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe breakdown of users is as follows:\n{}'.format(user_types))

    # IF statement to proceed with Chicago and New York data only, since washington.csv does not have gender and birth year information.
    if city != 'washington':
        # calculate and display counts of gender
        gender = df['Gender'].value_counts()
        print('\nThe breakdown of gender is as follows:\n{}'.format(gender))

        # calculate and display earliest, most recent, and most common year of birth
        oldest = int(df['Birth Year'].min())
        youngest = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode())
        print('\nThe earliest, most recent and most common year of birth are {}, {} and {} respectively.\n'.format(oldest, youngest, common))

    # calculate and display computing time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays five lines of data at a time as specified by user."""

    see_data = input('\nWould you like to see the first five lines of the raw data? Enter yes or no.\n')
    line_count = 0

    # loop terminates with any input other than 'yes'
    while see_data == 'yes':
        print(df.iloc[line_count:line_count + 5])
        line_count += 5
        see_data = input('\nWould you like see five more lines of the raw data? Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
