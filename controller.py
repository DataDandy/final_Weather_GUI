from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from view import *
from datetime import datetime
import requests
import pytemperature

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Controller(QMainWindow, Ui_MainWindow):
    """Function to set up the Controller class. The Controller holds all the functions necessary for the program to run.
    It is good practice to keep the Controller separate from the main.py and the view.py.
    """
    def __init__(self, *args, **kwargs):
        """Function to initiate the GUI setup. Defines button actions and shows initial GUI output of Date.
        """
        now = datetime.now()
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.buttonSearch.clicked.connect(lambda: self.search())
        self.buttonClear.clicked.connect(lambda: self.clear())
        self.labelOutputDate.setText(now.strftime("%A %B %d, %Y"))

    def search(self):
        """Function to create the search processes for the GUI. User will enter city and country and the system will
        output the weather along with an image of the weather's icon from a JSON file. The JSON does not allow for
        entering a state, but the output is very accurate for searched cities.
                """
        api_start = 'https://api.openweathermap.org/data/2.5/weather?q='
        api_key = '&appid=089d638e7bcd08656a35fd6ae8eaa004'
        city = self.inputCity.text()
        country = self.inputCountry.text()

        try:
            url = api_start + city + ',' + country + api_key
            json_data = requests.get(url).json()
            # getting weather data from json
            weather_description = json_data['weather'][0]['description']
            weather_temp = json_data['main']['temp']
            weather_humidity = json_data['main']['humidity']
            icon = json_data['weather'][0]['icon']
            image_url = f'https://openweathermap.org/img/wn/{icon}@2x.png'
            image_data = requests.get(image_url).content
            qpixmap = QPixmap()
            qpixmap.loadFromData(image_data)

            self.labelOutput.setText(f"The Weather Report for {city}, in {country}: \n\tCurrent Conditions: "
                                     f"{weather_description}\n\tCurrent Temperature in Fahrenheit: "
                                     f"{pytemperature.k2f(weather_temp):.0f}\n\tCurrent Humidity: {weather_humidity}%")
            self.labelImage.setPixmap(qpixmap)

        except:
            self.clear()
            self.labelOutput.setText(f'\tUnable to access {city} in {country} \n\tVerify city name and country code')

    def clear(self):
        """Function to clear the data the user entered and prepare it for new input.
        """
        blank = self.inputCity.setText("")
        self.inputCountry.setText("")
        self.labelOutput.setText("")
        self.labelImage.clear()