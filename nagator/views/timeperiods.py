import re
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	timeperiods_founded = []
	timeperiods_filtered = []

	try:
		timeperiods = nc['all_timeperiod']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No timeperiod")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for timeperiod in timeperiods:
   		filtered = False
	   	for element in filtre:
			if element in timeperiod.keys():
   				try:
	   			   filtre_pattern = re.compile(filtre[element])
				except:
		   			with indent(3, quote=colored.red(' >> ')):
			   			puts('Regexp error')
				   	sys.exit(1)
				if not filtre_pattern.match(timeperiod[element]):
   					filtered = True
	   				break
				else:
		   			filtered = False
			else:
   				filtered = True
	   			break

		if not filtered:
   			timeperiods_founded.append(timeperiod)
	   	else:
			timeperiods_filtered.append(timeperiod)

	with indent(3, quote=colored.white(' ====> ')):
		puts("Commands founded")

	if timeperiods_founded:
		for timeperiod in timeperiods_founded:
			with indent(3, quote=colored.green(' >> ')):
			  	puts("%s" % timeperiod['timeperiod_name'])

			if not 'small' in options:
				for key, value in sorted(timeperiod.items()):
					if key != 'meta' and key != 'timeperiod_name':
				   		with indent(3, quote=colored.white('    | ')):
							puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % len(timeperiods_founded))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Commands filtered")

		if timeperiods_filtered:
			for timeperiod in timeperiods_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % timeperiod['timeperiod_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % len(timeperiods_filtered))

def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')
	with indent(2, quote=colored.white('     + ')):
		puts('titles after \">>\" are timeperiod_name')
