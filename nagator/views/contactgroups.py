import re
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	contactgroups_founded = []
	contactgroups_filtered = []

	try:
		contactgroups = nc['all_contactgroup']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No contactgroup")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for contactgroup in contactgroups:
   		filtered = False
	   	for element in filtre:
			if element in contactgroup.keys():
   				try:
	   			   filtre_pattern = re.compile(filtre[element])
				except:
		   			with indent(3, quote=colored.red(' >> ')):
			   			puts('Regexp error')
				   	sys.exit(1)
				if not filtre_pattern.match(contactgroup[element]):
   					filtered = True
	   				break
				else:
		   			filtered = False
			else:
   				filtered = True
	   			break

		if not filtered:
   			contactgroups_founded.append(contactgroup)
	   	else:
			contactgroups_filtered.append(contactgroup)

	with indent(3, quote=colored.white(' ====> ')):
		puts("Contactgroups founded")

	if contactgroups_founded:
		for contactgroup_founded in contactgroups_founded:
			with indent(3, quote=colored.green(' >> ')):
			  	puts("%s" % contactgroup_founded['contactgroup_name'])

			if not 'small' in options:
				for key, value in sorted(contactgroup_founded.items()):
					if key != 'meta':
						if key in contactgroup_founded['meta']['defined_attributes']:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.green(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % len(contactgroups_founded))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Contactgroups filtered")

		if contactgroups_filtered:
			for contactgroup_filtered in contactgroups_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % contactgroup_filtered['contactgroup_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % len(contactgroups_filtered))

def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')
	with indent(2, quote=colored.white('     + ')):
		puts('titles after \">>\" are contactgroup_name')
