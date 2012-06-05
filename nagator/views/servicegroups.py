import re
import sys
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	servicegroups_founded = []
	servicegroups_filtered = []

	try:
		servicegroups = nc['all_servicegroup']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No servicegroup")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for servicegroup in servicegroups:
   		filtered = False
	   	for element in filtre:
			if element in servicegroup.keys():
   				try:
	   			   filtre_pattern = re.compile(filtre[element])
				except:
		   			with indent(3, quote=colored.red(' >> ')):
			   			puts('Regexp error')
				   	sys.exit(1)
				if not filtre_pattern.match(servicegroup[element]):
   					filtered = True
	   				break
				else:
		   			filtered = False
			else:
   				filtered = True
	   			break

		if not filtered:
   			servicegroups_founded.append(servicegroup)
	   	else:
			servicegroups_filtered.append(servicegroup)

	with indent(3, quote=colored.white(' ====> ')):
		puts("Servicegroups founded")

	if servicegroups_founded:
		for servicegroup in servicegroups_founded:
			with indent(3, quote=colored.green(' >> ')):
			  	puts("%s" % servicegroup['servicegroup_name'])

			if not 'small' in options:
				for key, value in sorted(servicegroup.items()):
					if key != 'meta':
						if key in servicegroup['meta']['defined_attributes']:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.green(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % len(servicegroups_founded))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Servicegroups filtered")

		if servicegroups_filtered:
			for servicegroup_filtered in servicegroups_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % servicegroup_filtered['servicegroup_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % len(servicegroups_filtered))

def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')
	with indent(2, quote=colored.white('     + ')):
		puts('titles after \">>\" are servicegroup_name')
