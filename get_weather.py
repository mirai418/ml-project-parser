import csv

# month: January == 1
def getDay(day, month, year):
	daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	if (year % 4 == 0):
		daysInMonth[1] = 29
	dayNum = day
	for i in xrange (month - 1):
		dayNum += daysInMonth[i]
	return dayNum - 1

def getArrPos(timeStr, dayStr, monthStr, yearStr):
	day = int(dayStr)
	month = int(monthStr)
	year = int(yearStr)
	meridian = timeStr.split(" ")[1]
	timeIndex = int(timeStr.split(":")[0]) % 12
	if meridian == "PM":
		timeIndex += 12
	dayPos = getDay(day, month, year) * 24
	return timeIndex + dayPos

def loadWeather():
	arr = []
	i = 0
	filename = "weather.csv"
	with open(filename, 'rb') as csvfile:
		r = csv.reader(csvfile)
		r.next()
		for row in r:
			arr.append(row)
			i += 1

	for item in arr:
		print item
	return arr
