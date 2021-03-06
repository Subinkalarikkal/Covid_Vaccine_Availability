import requests
from pygame import mixer
from datetime import datetime, timedelta
import time

age = 50
pincodes = ["679332"]
num_days = 2

print_flag = 'Y'

print("Starting search for Covid vaccine slots in the pincode!")

actual = datetime.today()
list_format = [actual + timedelta(days=i) for i in range(num_days)]
actual_dates = [i.strftime("%d-%m-%Y") for i in list_format]

while True:
    counter = 0

    for pincode in pincodes:
        for given_date in actual_dates:

            URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}".format(
                pincode, given_date)
            header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

            result = requests.get(URL, headers=header)

            if result.ok:
                response_json = result.json()
                if response_json["centers"]:
                    if (print_flag.lower() == 'y'):
                        for center in response_json["centers"]:
                            for session in center["sessions"]:
                                if (session["min_age_limit"] <= age and session["available_capacity"] > 0):
                                    mixer.init()
                                    mixer.music.load('sound/msg.mp3')
                                    mixer.music.play()
                                    print('Pincode: ' + pincode)
                                    print("Available on: {}".format(given_date))
                                    print("\t Block name:", center["block_name"])
                                    print("\t Center name", center["name"])
                                    print("\t Price: ", center["fee_type"])
                                    print("\t Availablity : ", session["available_capacity"])

                                    if (session["vaccine"] != ''):
                                        print("\t Vaccine type: ", session["vaccine"])
                                    print("\n")
                                    counter = counter + 1
            else:
                print("Not getting response from the server!")

    if counter:
        print("No more Vaccination slot available in your area..Please wait once you get notified!")
    else:
        mixer.init()
        mixer.music.load('sound/msg1.mp3')
        mixer.music.play()
        print("Search Completed!")

    dt = datetime.now() + timedelta(minutes=4)

    while datetime.now() < dt:
        time.sleep(1)
