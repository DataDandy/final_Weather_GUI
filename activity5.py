from datetime import datetime
import requests
import pytemperature


def weather():
    api_start = 'https://api.openweathermap.org/data/2.5/weather?q='
    api_key = '&appid=089d638e7bcd08656a35fd6ae8eaa004'
    now = datetime.now()
    print("ISQA 3900 Open Weather API")
    print(now.strftime("%A %B %d, %Y"))
    filename = input("\nEnter the output filename: ")
    myfile = None
    try:
        myfile = open(filename, "w")

    except:
        print("Unable to open file " + filename +
              "\nData will not be saved to a file")
    choice = "y"
    while choice.lower() == "y":
        try:
            # input city and country code
            city = input("Enter city: ")
            print("Use ISO letter country code like: https://countrycode.org/")
            country = input("Enter country code: ")
            # app configures url to generate json data
            url = api_start + city + ',' + country + api_key
            json_data = requests.get(url).json()
            # getting weather data from json
            weather_description = json_data['weather'][0]['description']
            weather_temp = json_data['main']['temp']
            weather_pressure = json_data['main']['pressure']
            weather_humidity = json_data['main']['humidity']

            # printing information
            print("The Weather Report for " + city + " in " + country + " is:")
            print("\tCurrent Conditions: ", weather_description)
            print("\tCurrent Temperature in Fahrenheit: ", pytemperature.k2f(weather_temp))
            print("\tCurrent Pressure in hpa: ", weather_pressure)
            print(f'\tCurrent Humidity: {weather_humidity}%')

            if myfile:
                myfile.write(f"The Weather Report for {city} in {country} is:\n")
                myfile.write(f"\tCurrent Conditions: {weather_description}\n")
                myfile.write(f"\tCurrent Temperature in Fahrenheit: {pytemperature.k2f(weather_temp)}\n")
                myfile.write(f"\tCurrent Pressure in hpa: {weather_pressure}\n")
                myfile.write(f"\tCurrent Humidity: {weather_humidity}%\n\n\n")

        except:
            print(f"\tUnable to access {city} in {country} \n\tVerify city name and country code")
        choice = input("Continue (y/n)?: ")
        print()
    if myfile:
        myfile.close()
    print('Thank you - Goodbye')


if __name__ == "__main__":
    main()
