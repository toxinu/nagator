import re
import sys
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	hosts_founded = []
	hosts_template_founded = []

	hosts_filtered = []
	hosts_template_filtered = []

	try:
		hosts = nc['all_host']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No host")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for host in hosts:
		filtered = False
		for element in filtre:
			if element in host.keys():
				try:
					filtre_pattern = re.compile(filtre[element])
				except:
					with indent(3, quote=colored.red(' >> ')):
						puts('Regexp error')
					sys.exit(1)
				if not filtre_pattern.match(host[element]):
					filtered = True
					break
				else:
					filtered = False
			else:
				filtered = True
				break

		if not filtered:
			if host.has_key('register'):
				if host['register'] == 0:
					hosts_founded.append(host)
				else:
					hosts_template_founded.append(host)
			else:
				hosts_founded.append(host)
		else:
			if host.has_key('register'):
				if host['register'] == 0:
					hosts_filtered.append(host)
				else:
					hosts_template_filtered.append(host)
			else:
				hosts_filtered.append(host)

	hosts_founded = sorted(
						hosts_founded,
						key=lambda k: k['meta']['defined_attributes']['host_name']) 
	hosts_template_founded = sorted(
						hosts_template_founded,
						key=lambda k: k['name']) 

	hosts_filtered = sorted(
						hosts_filtered,
						key=lambda k: k['meta']['defined_attributes']['host_name']) 
	hosts_template_filtered = sorted(
						hosts_template_filtered,
						key=lambda k: k['name']) 


	with indent(3, quote=colored.white(' ====> ')):
		puts("Hosts founded")

	if hosts_template_founded:
		for host in hosts_template_founded:
			with indent(3, quote=colored.red(' >> ')):
				puts("%s" % host['name'])
			if not 'small' in options:
				for key, value in sorted(host.items()):
					if key != 'meta':
						if key in host['meta']['inherited_attributes']:
							with indent(3, quote=colored.white('    | ')):
							   puts("%s: %s" % (colored.blue(key), colored.green(value)))
						else:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	if hosts_founded:
		for host in hosts_founded:
			with indent(3, quote=colored.green(' >> ')):
				puts("%s" % host['host_name'])
			if not 'small' in options:
				for key, value in sorted(host.items()):
					if key != 'meta':
						if key in host['meta']['inherited_attributes']:
							with indent(3, quote=colored.white('    | ')):
							   puts("%s: %s" % (colored.blue(key), colored.green(value)))
						else:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % (len(hosts_founded) + len(hosts_template_founded)))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Hosts filtered")

		if hosts_template_filtered:
			for host in hosts_template_filtered:
				with indent(3, quote=colored.red(' >> ')):
					puts("%s" % host['name'])

		if hosts_filtered:
			for host in hosts_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % host['host_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % (len(hosts_filtered) + len(hosts_template_filtered)))


def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')

	with indent(2, quote=colored.white('   - ')):
		puts(colored.white('Titles'))
	with indent(2, quote=colored.white('     + ')):
		puts(colored.red('red \">>\" are templates (name atttribute)'))
		puts(colored.green('green \">>\" are not templates (host_name attribute)'))
	if not 'small' in options:
		with indent(2, quote=colored.white('   - ')):
			puts(colored.white('Attributes'))
		with indent(2, quote=colored.white('     + ')):
			puts(colored.green('green values are inherited attributes'))
			puts(colored.yellow('yellow values are defined attributes'))
