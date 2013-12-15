# compiles the two datasets together.
# I only focus on flights from PIT (Pittsburgh International Airport)
# For every flight departing from PIT, I find the respective weather information based on history and make a row in the table.

import csv

def main():
	path = "../data/flights_month/"
	writePath = "../data/compilation/"
	filenames = createFlightFilenames()

	with open(writePath + "departures.csv", "wb") as csvfile:
		wd = csv.writer(csvfile, delimiter=',')
		with open(writePath + "arrivals.csv", "wb") as csvfile:
			wa = csv.writer(csvfile, delimiter=',')
			for filename in filenames:
				with open(path + filename, 'rb') as csvfile:
					r = csv.reader(csvfile)
					r.next()
					for row in r:
						dep = row[9]
						dest = row[14]
						if (dep == "PIT" or dest == "PIT"):
							# we will do some pre-analysis feature selection, as many of these fields are either redundant, unnecessary, unhelpful, or cannot replicate in real life
							featureSelect(row, dep == "PIT")
							res = addWeather(row)
							postSelect(res)
							print res
							if (dep == "PIT"):
								wd.writerow(res)
							else:
								wa.writerow(res)

def stringify(i):
	res = "0" + str(i) if (i < 10) else str(i)
	return res

def createFlightFilenames():
	filenames = []
	for i in xrange(1,13):
		year = "13" if i < 8 else "12"
		month = stringify(i)
		filename = "20%s_%s.csv" % (year, month)
		filenames.append(filename)
	return filenames

def postSelect(row):
	r = row.pop(10)
	row.append(r)
	del row[9]
	del row[4]
	del row[0]

def featureSelect(row, dep):
	try:
		# obtain flight number through carrier and actual number - want this to be unique
		row[7] = row[5] + row[7]
		# col 23 is time block, which ranges from -2 to 12. if diverted, lets add it to block 14
		if (int(float(row[27])) == 1):
			row[23] = "14"
		# col 23 is time block, which ranges from -2 to 12. if cancelled, lets add it to block 13
		if (int(float(row[25])) == 1):
			row[23] = "13"
		if (int(row[23]) <= 0):
			row[23] = "False"
		else:
			row[23] = "True"		
		# get rid of float... actually this is not used.
		row[28] = int(float(row[28]))
	except Exception, e:
		pass
	# some empty stuff... delete
	if (len(row) == 47):
		del row[46]
	# not enough data... diverted flights
	del row[45] # div1 airport id
	del row[44] # div1 airport
	del row[43] # div distance
	del row[42] # div arr delay
	del row[41] # div1 elapsed time
	del row[40] # div reached dest
	del row[39] # div landing
	# gate return info. delete for now
	del row[38]
	del row[37]
	del row[36]
	# delay break down... cant determine for actual so delete
	del row[35]
	del row[34]
	del row[33]
	del row[32]
	del row[31]
	# more important stuff
	del row[29] # keep distance group, delete actual distance
	del row[28] # after inspection, this only takes value 1, so delete
	del row[27] # diverted - merged with block
	del row[26] # cancel code
	del row[25] # cancelled - merged with block
	del row[22] # delay 15
	del row[21] # time in minutes
	del row[20] # actual delay - negative if early
	del row[19] # actual departure time
	del row[17]
	del row[16]
	del row[15]
	if (not dep):
		del row[14]
	del row[13]
	del row[12]
	del row[11]
	del row[10]
	if (dep):
		del row[9]
	del row[8]
	#del row[5] # carrier

# this will break if the feature selection is changed...
def addWeather(flightRow):
	path = "../data/weather/"
	year = flightRow[0]
	month = flightRow[1]
	day = flightRow[2]
	t = flightRow[9]
	filename = "weather_%s_%s_%s.csv" % (year, month, day)
	res = None

	with open(path + filename, 'rb') as csvfile:
		r = csv.reader(csvfile)
		curMin = 1440 # minutes in day
		curRow = None
		for row in r:
			tempTime = row[3]
			featureSelectWeather(row)
			# should return in minutes the difference.
			# it should be in parabolic function, where it gets less and less and then increases. need min point
			diff = abs(timeDifference(t, tempTime))
			if (diff < curMin):
				curMin = diff
				curRow = row
			# we hit the min point right before this
			else:
				res = flightRow + curRow
				return res
		# last one is min
		res = flightRow + curRow
	return res


def timeDifference(t, tempTime):
	# t is in military time.
	tHour = int(t[0:2])
	tMin = int(t[2:4])
	tMins = tHour * 60 + tMin
	# tempTime is in format hh:mm AP
	tempTimeMeridian = tempTime.split(" ")[1]
	tempTimeHour = int(tempTime.split(":")[0]) % 12
	tempTimeMin = int(tempTime.split(" ")[0].split(":")[1])
	if (tempTimeMeridian == "PM"):
		tempTimeHour += 12
	tempTimeMins = tempTimeHour * 60 + tempTimeMin
	return tempTimeMins - tMins

def featureSelectWeather(row):
	#visibility - less than 3km is poor
	if (float(row[8]) < 2):
		row[8] = "Poor"
	elif (float(row[8]) < 6):
		row[8] = "Fair"
	else:
		row[8] = "Good"
	# wind speed
	if (not (row[10] == "Calm")):
		row[10] = "Fair" if (float(row[10]) < 18) else "Strong"
	# gust
	row[11] = "None" if row[11] == "-" else "Some"
	# precipitation
	if (not (row[12] == "N/A")):
		if (float(row[12]) < 0.1):
			row[12] = "Light"
		elif (float(row[12]) < 0.3):
			row[12] = "Moderate"
		else:
			row[12] = "Strong"
  # conditions...
	if (row[14] == "Overcast" or row[14] == "Scattered Clouds" or row[14] == "Partly Cloudy" or row[14] == "Clear"):
		row[14] = "Clear"
	elif (row[14] == "Mostly Cloudy" or row[14] == "Haze" or row[14] == "Fog" or row[14] == "Mist" or row[14] == "Patches of Fog"):
		row[14] = "Cloudy"
	elif (row[14] == "Light Freezing Drizzle" or row[14] == "Light Drizzle"):
		row[14] = "Drizzle"
	elif (row[14] == "Light Rain" or row[14] == "Rain" or row[14] == "Heavy Rain" or row[14] == "Light Freezing Rain"):
		row[14] = "Rain"
	elif(row[14] == "Light Snow" or row[14] == "Snow" or row[14] == "Heavy Snow"):
		row[14] = "Snow"
	elif(row[14] == "Thunderstorm" or row[14] == "Light Thunderstorms and Rain" or row[14] == "Heavy Thunderstorms and Rain" or row[14] == "Thunderstorms and Rain"):
		row[14] = "Thunderstorm"

	del row[16]
	del row[15] # wind dir degrees	
	del row[13] # too many missing vals
	del row[7] # sea point pressure
	del row[3]
	del row[2]
	del row[1]
	del row[0]

main()