# compiles the two datasets together.
# I only focus on flights from PIT (Pittsburgh International Airport)
# For every flight departing from PIT, I find the respective weather information based on history and make a row in the table.

import csv

def main():
	path = "../data/flights_month/"
	filenames = createFlightFilenames()

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
					print res
		break


def stringify(i):
	if (i < 10):
		return "0" + str(i)
	else:
		return str(i)

def createFlightFilenames():
	filenames = []
	for i in xrange(1,13):
		if (i < 8):
			year = "13"
		else:
			year = "12"
		month = stringify(i)
		filename = "20%s_%s.csv" % (year, month)
		filenames.append(filename)
	return filenames

def featureSelect(row, dep):
		# obtain flight number through carrier and actual number - want this to be unique
	row[7] = row[5] + row[7]
	# col 23 is time block, which ranges from -2 to 12. if diverted, lets add it to block 14
	if (int(float(row[27])) == 1):
		row[23] = "14"
	# col 23 is time block, which ranges from -2 to 12. if cancelled, lets add it to block 13
	if (int(float(row[25])) == 1):
		row[23] = "13"
	if (int(row[23]) < 0):
		row[23] = "0"
	# get rid of float... actually this is not used.
	row[28] = int(float(row[28]))
	# some empty stuff... delete
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
	del row[5]

# this will break if the feature selection is changed...
def addWeather(flightRow):
	path = "../data/weather/"
	year = flightRow[0]
	month = flightRow[1]
	day = flightRow[2]
	t = flightRow[8]
	filename = "weather_%s_%s_%s.csv" % (year, month, day)

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
	row.append("hey")
	return None


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
	del row[16]
	del row[15] # wind dir degrees	
	del row[7] # sea point pressure
	del row[3]
	del row[2]
	del row[1]
	del row[0]

main()