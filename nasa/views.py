from ast import Str
from django.shortcuts import render
from django.conf import settings
from datetime import date, datetime, timedelta
import requests
from .models import Asteroid, Approach

# TODO : 
# - implémenter la gestion d'écart entre en start date et end date
# - indiquer que ça charge


def getAsteroidList(request):
    baseUrl = settings.NASA_ASTEROIDS_API_BASE_URL
    apiKey = settings.NASA_API_KEY
    start_date = None
    end_date = None
    results = None
    asteroids = []
    context = {}

    # On submit form with a POST, it gives us the start_date and the end_date so we can trigger the API Call
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # If the difference between the 2 dates is greater then 7 days, the request fails
        dateDifference = date.fromisoformat(end_date)-date.fromisoformat(start_date)
        if dateDifference > timedelta(days=7):
            results = 'error'
        else:
            urlRequest = baseUrl + "?start_date=" + start_date + \
                '&end_date=' + end_date + "&api_key=" + apiKey
            print('Url: ',urlRequest)
            apiRequest = requests.get(urlRequest)
            
            if apiRequest.status_code == 200:
                results = apiRequest.json()

            # Results data is a dictionnary of String<date> : List<AsteroidData>
            # So we parse the different date with a 1st loop 
            # Then use the date to parse each asteroid Data in a 2nd loop
            for day in results['near_earth_objects']:
                for asteroid in results['near_earth_objects'][str(day)]:
                    # Formatting Asteroid data : Size and Date for exploitation
                    averageSize = (asteroid['estimated_diameter']['meters']['estimated_diameter_min'] +
                                asteroid['estimated_diameter']['meters']['estimated_diameter_max'])/2
                    dateClosestHour = asteroid['close_approach_data'][0]["close_approach_date_full"].split(' ')
                    dateIsoFormatted = asteroid['close_approach_data'][0]["close_approach_date"]
                    dateClosest = dateIsoFormatted+'T'+dateClosestHour[1]+':00'

                    # Creating the Asteroid (see models.py) based on the API formatted data then add it to the Asteroid List
                    asteroid = Asteroid(
                        id=asteroid['id'],
                        name=asteroid['name'],
                        size=averageSize,
                        distance=asteroid['close_approach_data'][0]['miss_distance']['kilometers'],
                        dateClosest=datetime.fromisoformat(dateClosest)
                    )
                    print('Asteroid n°:'+ asteroid.id + ' on day : ' + str(asteroid.dateClosest))
                    asteroids.append(asteroid)

            # The data is not sorted : the first and last day are in first position then come days in between
            # So i sort the data according to the day
            def getDate(asteroid):
                return asteroid.dateClosest
            asteroids.sort(key=getDate)
            
            # Formatting start_date and end_date to output it in a readable way
            start_date = date.fromisoformat(start_date)
            end_date = date.fromisoformat(end_date)
            

    # Context Dictionnary to fill up the template with dynamic data
    context = {'results': results, 'asteroids': asteroids,
                        'start_date': start_date, 'end_date': end_date}

    return render(request, 'nasa/asteroids.html', context)


def getAsteroid(request, id):
    baseUrl = settings.NASA_ASTEROID_API_BASE_URL
    apiKey = settings.NASA_API_KEY
    urlRequest = baseUrl + id + "?api_key=" + apiKey

    # Get the data from Nasa Api and formatting it to json 
    result = requests.get(urlRequest).json()
    print('Url: ',urlRequest)
    
    # Formatting Asteroid data : Size and Date for exploitation
    averageSize = (result['estimated_diameter']['meters']['estimated_diameter_min'] +
                   result['estimated_diameter']['meters']['estimated_diameter_max'])/2

    # Creating the Asteroid Object with data from the request
    asteroid = Asteroid(
        id=result['id'],
        name=result['name'],
        size=averageSize,
        distance=result['close_approach_data'][0]['miss_distance']['kilometers'],
        dateClosest=result['close_approach_data'][0]['close_approach_date_full'],
        firstObservationDate=date.fromisoformat(
            result['orbital_data']['first_observation_date']),
        lastObservationDate=date.fromisoformat(
            result['orbital_data']['last_observation_date']),
        dataArcInDays=result['orbital_data']['data_arc_in_days'],
    )

    # Parsing the data to get the previous and next asteroid's Approach (see models.py)
    for approache in result['close_approach_data']:
        if date.fromisoformat(approache['close_approach_date']) < date.today():
            asteroid.previousApproaches.append(
                Approach(
                    asteroidId=result['id'],
                    approachDate=date.fromisoformat(
                        approache['close_approach_date']),
                    distance=approache['miss_distance']['kilometers']
                )
            )
            asteroid.previousApproaches.reverse()
        else:
            asteroid.nextApproaches.append(
                Approach(
                    asteroidId=result['id'],
                    approachDate=date.fromisoformat(
                        approache['close_approach_date']),
                    distance=approache['miss_distance']['kilometers']
                )
            )
            asteroid.nextObservation = asteroid.nextApproaches[0].approachDate

    context = {'asteroid': asteroid}
    return render(request, 'nasa/asteroid.html', context)
