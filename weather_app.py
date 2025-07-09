import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFormLayout,
    QLineEdit, QPushButton, QLabel,
    QMessageBox, QComboBox, QVBoxLayout, QHBoxLayout, QGroupBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.setGeometry(200, 550, 500, 550)

        # Create widgets
        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name")

        self.country_input = QLineEdit()
        self.country_input.setPlaceholderText("Enter country name")

        self.unit_selector = QComboBox()
        self.unit_selector.addItems(["Celsius (°C)", "Fahrenheit (°F)"])

        self.search_button = QPushButton("Search")

        self.result_label = QLabel("Weather info will appear here.")
        self.result_label.setAlignment(Qt.AlignCenter)

        self.weather_icon = QLabel()
        self.weather_icon.setAlignment(Qt.AlignCenter)

        # Main form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.addRow(self.city_input)
        form_layout.addRow(self.country_input)
        form_layout.addRow(self.unit_selector)
        form_layout.addRow(self.search_button)

        # Group box for result display
        result_box = QGroupBox("Weather Info")
        result_layout = QVBoxLayout()
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.weather_icon)
        result_box.setLayout(result_layout)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(result_box)

        self.setLayout(main_layout)

        # Connect the button
        self.search_button.clicked.connect(self.get_weather)

    def get_weather(self):
        city = self.city_input.text().strip()
        country = self.country_input.text().strip()
        
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name.")
            return
        if not country:
            QMessageBox.warning(self, "Input Error", "Please enter a country name.")
            return

        api_key = "dcf1d0a077126ba4cc7925ac2dcd5132"
        unit_text = self.unit_selector.currentText()
        units = "metric" if "Celsius" in unit_text else "imperial"
        unit_symbol = "°C" if units == "metric" else "°F"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country}&units={units}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            city_name = data["name"]
            country_name = data["sys"]["country"]
            temperature = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            wind_dir = data["wind"].get("deg", "N/A")  # some APIs may omit 'deg'
            clouds = data["clouds"]["all"]

            icon_code = data["weather"][0]["icon"]
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

            # Set result label
            self.result_label.setText(
                f"City: {city_name}\nCountry: {country_name}\n"
                f"Temperature: {temperature}{unit_symbol}\n"
                f"Weather: {weather.capitalize()}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Wind Direction: {wind_dir}°\n"
                f"Cloudiness: {clouds}%"
                )

            # Load weather icon
            icon_response = requests.get(icon_url)
            if icon_response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(icon_response.content)
                self.weather_icon.setPixmap(pixmap)
            else:
                self.weather_icon.clear()

        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Failed to get weather data:\n{e}")
        except KeyError:
            QMessageBox.warning(self, "Error", "City not found or invalid API response.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    try:
        with open("style.qss", "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("No QSS stylesheet found.")

    window = Weather()
    window.show()
    sys.exit(app.exec_())


