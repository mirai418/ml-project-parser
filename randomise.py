import random
import csv

# loop through each file.
# everytime find random number 1~100, if 1 then put it int he new set.

def main():
	i = 0
	filenames = createFilenames()
	with open('compilation.csv', 'wb') as csvfile:
		w = csv.writer(csvfile, delimiter=',')
		for filename in filenames:
			with open(filename, 'rb') as csvfile:
				f = csv.reader(csvfile)
				print filename
				f.next()
				for row in f:
					
					r = random.randint(1,100)
					if (r == 100):
						i = i + 1
						w.writerow(row)
						print row
	print i

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