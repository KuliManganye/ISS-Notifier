import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.50853
MY_LONG = -0.12574
MY_EMAIL = "email"
MY_PASSWORD = "password"

def is_iss_overhead():
    response = requests.get(url="http://api.open.notify.org.iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_longitude = data["iss_position"]["longitude"]
    iss_latitude = data["iss_position"]["latitude"]

    if MY_LAT <= iss_longitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour()

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: Look Up\n\nThe Iss is above you in the sky!")