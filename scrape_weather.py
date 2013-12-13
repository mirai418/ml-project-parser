import urllib2
import csv

def main():
	daysInMonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	startYear = 2012
	years = 2
	for year in xrange(years):
		if ((startYear + year) % 4 == 0):
			daysInMonth[1] = 29
		else:
			daysInMonth[1] = 28
		for month in xrange(1, 13):
			for day in xrange(1, daysInMonth[month - 1] + 1):
				filename = "../data/weather/weather_%d_%d_%d.csv" % (startYear + year, month, day)
				f = open(filename, 'wb')
				with f as csvfile:
					getData(startYear + year, month, day, csvfile)
				f.close()

def getData(year, month, day, csv):
	global first
	newline = "<br />"
	url = urlify(year, month, day)
	response = urllib2.urlopen(url)
	line = response.readline()
	# line = response.readline().replace(newline, "")
	line = response.readline().replace(newline, "")
	if (first == 1):
		date = "year,month,day,"
		csv.write(date + line)
		first = 0
	while (line != ""):
		line = response.readline().replace(newline, "")
		if (line == ""):
			break
		date = "%d,%d,%d," % (year, month, day)
		csv.write(date + line)
		# print line

def urlify(year, month, day):
	return "http://www.wunderground.com/history/airport/KPIT/%d/%d/%d/DailyHistory.html?req_city=Pittsburgh&req_state=PA&req_statename=Pennsylvania&format=1" % (year, month, day)

first = 1
main()