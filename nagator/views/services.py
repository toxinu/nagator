import re
import sys
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	services_founded = []
	services_template_founded = []

	services_filtered = []
	services_template_filtered = []

	try:
		services = nc['all_service']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No service")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for service in services:
   		filtered = False
	   	for element in filtre:
			if element in service.keys():
   				try:
	   			   filtre_pattern = re.compile(filtre[element])
				except:
		   			with indent(3, quote=colored.red(' >> ')):
			   			puts('Regexp error')
				   	sys.exit(1)
				if not filtre_pattern.match(service[element]):
   					filtered = True
	   				break
				else:
		   			filtered = False
			else:
   				filtered = True
	   			break

		if not filtered:
			if service.has_key('register'):
				if service['register'] == 0:
					services_founded.append(service)
				else:
					services_template_founded.append(service)
			else:	
	   			services_founded.append(service)
	   	else:
			if service.has_key('register'):
				if service['register'] == 0:
					services_filtered.append(service)
				else:
					services_template_filtered.append(service)
			else:	
				services_filtered.append(service)

	services_founded = sorted(
						services_founded,
						key=lambda k: k['meta']['defined_attributes']['service_description'])
	services_template_founded = sorted(
						services_template_founded,
						key=lambda k: k['name'])
	services_filtered = sorted(
						services_filtered,
						key=lambda k: k['meta']['defined_attributes']['service_description'])
	services_template_filtered = sorted(
						services_template_filtered,
						key=lambda k: k['name'])

	with indent(3, quote=colored.white(' ====> ')):
		puts("Services founded")

	if services_template_founded:
		for service in services_template_founded:
			with indent(3, quote=colored.red(' >> ')):
   				puts("%s" % service['name'])

			if not 'small' in options:
   				for key, value in sorted(service.items()):
   					if key != 'meta':
	   					if key in service['meta']['inherited_attributes']:
		   					with indent(3, quote=colored.white('    | ')):
			   					puts("%s: %s" % (colored.blue(key), colored.green(value)))
				   		else:
					   		with indent(3, quote=colored.white('    | ')):
						   		puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	if services_founded:
		for service in services_founded:
			with indent(3, quote=colored.green(' >> ')):
   				puts("%s" % service['service_description'])

			if not 'small' in options:
   				for key, value in sorted(service.items()):
   					if key != 'meta':
	   					if key in service['meta']['inherited_attributes']:
		   					with indent(3, quote=colored.white('    | ')):
			   					puts("%s: %s" % (colored.blue(key), colored.green(value)))
				   		else:
					   		with indent(3, quote=colored.white('    | ')):
						   		puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % (len(services_founded) + len(services_template_founded)))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Services filtered")

		if services_template_filtered:
			for service in services_template_filtered:
				with indent(3, quote=colored.red(' >> ')):
					puts("%s" % service['name'])

		if services_filtered:
			for service in services_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % service['service_description'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % (len(services_filtered) + len(services_template_filtered)))

def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')
	with indent(2, quote=colored.white('   - ')):
		puts(colored.white('Titles'))
	with indent(2, quote=colored.white('     + ')):
		puts(colored.red('red \">>\" are templates (name attribute)'))
		puts(colored.green('green \">>\" are not templates (service_description attribute)'))
	if not 'small' in options:
		with indent(2, quote=colored.white('   - ')):
			puts(colored.white('Attributes'))
		with indent(2, quote=colored.white('     + ')):
			puts(colored.green('green values are inherited attributes'))
			puts(colored.yellow('yellow values are defined attributes'))
