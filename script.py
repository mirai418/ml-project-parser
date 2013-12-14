# template script for accessing flight data.

import csv

def main():
	filenames = createFilenames()

	for filename in filenames:
		with open(filename, 'rb') as csvfile:
			r = csv.reader(csvfile)
			print filename
			r.next()
			for row in r:
				print row
			print 


def stringify(i):
	if (i < 10):
		return "0" + str(i)
	else:
		return str(i)

def createFilenames():
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

main()