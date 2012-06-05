import re
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	hostgroups_founded = []
	hostgroups_filtered = []

	try:
		hostgroups = nc['all_hostgroup']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No hostgroup")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for hostgroup in hostgroups:
   		filtered = False
	   	for element in filtre:
			if element in hostgroup.keys():
   				try:
	   			   filtre_pattern = re.compile(filtre[element])
				except:
		   			with indent(3, quote=colored.red(' >> ')):
			   			puts('Regexp error')
				   	sys.exit(1)
				if not filtre_pattern.match(hostgroup[element]):
   					filtered = True
	   				break
				else:
		   			filtered = False
			else:
   				filtered = True
	   			break

		if not filtered:
   			hostgroups_founded.append(hostgroup)
	   	else:
			hostgroups_filtered.append(hostgroup)

	with indent(3, quote=colored.white(' ====> ')):
		puts("Hostgroups founded")

	if hostgroups_founded:
		for hostgroup_founded in hostgroups_founded:
			with indent(3, quote=colored.green(' >> ')):
			  	puts("%s" % hostgroup_founded['hostgroup_name'])

			if not 'small' in options:
				for key, value in sorted(hostgroup_founded.items()):
					if key != 'meta':
						if key in hostgroup_founded['meta']['defined_attributes']:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.green(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % len(hostgroups_founded))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Hostgroups filtered")

		if hostgroups_filtered:
			for hostgroup_filtered in hostgroups_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % hostgroup_filtered['hostgroup_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % len(hostgroups_filtered))

def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')
	with indent(2, quote=colored.white('     + ')):
		puts('titles after \">>\" are hostgroup_name')
