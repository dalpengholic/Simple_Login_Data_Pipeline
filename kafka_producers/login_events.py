import random
from datetime import datetime, timedelta

def create_login_event():
    browsers = ['safari', 'chrome', 'firefox', 'edge']
    countries = ['Finland', 'US', 'South Korea', 'India', 'Spain', 'Sweden']
    
    # Generate a random timestamp within the range of 2022 Jan 1st and 2022 Dec 31st
    user_id = random.randint(1, 500)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_date = start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))
    timestamp = random_date.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Select a random browser from the list
    browser = random.choice(browsers)
    country = random.choice(countries)

    # Create the login event record
    login_event = {
        'user_id': user_id,
        'timestamp': timestamp,
        'browser_info': browser,
        'country': country
    }

    return login_event
