import os
import sys
import requests
import datetime as dt
import time
import config as cfg

username = os.environ['REPL_OWNER']

while True:
		print("\n")

		def get_public_ip():
				try:
						response = requests.get('https://api64.ipify.org?format=json')
						data = response.json()
						return data['ip']
				except Exception as e:
						print(f"Failed to retrieve public IP: {str(e)}")
						return None

		IP_address = get_public_ip()

		city = input("Note about current location generator: it only works on a locally installed IDE such as VSCode or PyCharm.\nOn Replit, it shows the location of the Replit servers. Until I can find a workaround, please copy and paste into a local IDE. \n Name a city (leave blank for current location): \n")
		sep = ","
		if "," in city:
				city = city.split(sep, 1)[0]
		else:
				pass
		if city.lower() == "new york city":
				city = "New York"
		elif city == "":
				IP_address = get_public_ip()
				response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={cfg.location}&ip_address={IP_address}&fields=city")
				city = str(response.content)
				city = city.replace('b\'{"city":"', "")
				city = city.replace('"}\'', "")

		print("\n")

		def fetchData() -> str:
				j = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={cfg.api}&units={cfg.unit}&lang={cfg.lang}")

				source = j.json()

				# Checks if the return code is 200 and if it isn't, displays an error message.
				if source['cod'] == 200:
						pass
				elif source['cod'] == "404":
						print("Invalid city name given.")
						sys.exit("City was invalid")
				elif source['cod'] == 401:
						print("Invalid API key given.")
						sys.exit("Error on our end.")
				else:
						print("Unknown error occurred.")
						sys.exit("No clue what happened, honestly")

				return source

		source = fetchData()

		def viewAscii() -> None:
				iconName = source['weather'][0]['main']
				if iconName == "Clear":
						print("\033[33m",
									"      \   /    ",
									"       .-.     ",
									"    ‒ (   ) ‒  ",
									"       `-᾿     ",
									"      /   \    ",
									"               ", "\033[0m", sep='\n')
				elif iconName == "Clouds":
						print("       .--.     ",
									"    .-(    ).   ",
									"   (___.__)__)  ",
									"                ", sep='\n')
				elif iconName == "Rain":
						print("\033[97m",
									"       .--.     ",
									"    .-(    ).   ",
									"   (___.__)__)  ",
									"\033[34m",
									"   ʻ‚ʻ‚ʻ‚ʻ‚ʻ‚   ",
									"                ", "\033[0m", sep='\n')
				elif iconName == "Snow":
						print("       .--.     ",
									"    .-(    ).   ",
									"   (___.__)__)  ",
									"    * * * * *   ",
									"                ", sep='\n')
				else:
						print("       .--.     ",
									"    .-(    ).   ",
									"   (___.__)__)  ",
									"                ", sep='\n')

		# Checks which measurement unit to use.
		def unitCheck() -> str:
				if cfg.unit == "standard":
						tempUnit = "K"
						speedUnit = "m/s"
				elif cfg.unit == "metric":
						tempUnit = "°C"
						speedUnit = "m/s"
				elif cfg.unit == "imperial":
						tempUnit = "°F"
						speedUnit = "mph"

				return tempUnit, speedUnit

		tempUnit, speedUnit = unitCheck()

		# Prints ascii image and weather info.
		def printInfo():
				descGroup = source['weather'][0]
				desc = descGroup['description'] + "."
				desc = desc.replace("y", "ies")
				mainGroup = source['main']
				temp = mainGroup['temp']
				humidity = mainGroup['humidity']
				windGroup = source['wind']
				speed = windGroup['speed']
				viewAscii()

				print(f"Today in {city}, expect {desc} the temperature will be about {str(temp)}{tempUnit} with {str(humidity)} percent humidity and a wind speed of about {str(speed)} {speedUnit}")

				now = dt.datetime.now()
				todayVar = dt.datetime.today()
				lastDay = abs((todayVar - dt.datetime.strptime('2024/05/25', "%Y/%m/%d")).days)
				today = now.strftime(f"\nIt is %A, %B %d, %Y. The time is %I:%M:%S %p, and school ends in {lastDay} days")
				print("\033[33m", f"{today}", "\033[0m")
				time.sleep(1)

		printInfo()
