#!/usr/bin/env python
import os
import sys
import re
from clint.textui import colored, indent, puts
from clint import args
from pynag.Parsers import config
from pynag import Model
from ConfigParser import SafeConfigParser

debug = False

def usage():
	with indent(1, quote=' '):
		puts('Usage: nagator [MODE] [OPTIONS] [FILTERS]')
		print
		puts('Modes')
		with indent(2, quote=' '):
			puts('--list [host|service]')
		print
		puts('Filters')
		with indent(2, quote=' '):
			puts('You can use every nagios configuration option')
		print
		puts('Options')
		with indent(2, quote=' '):
			puts('--options <option,option,..>')
		with indent(6):
			puts('legend          Legend at the end of output')
			puts('small           Smaller output')
			puts('show_filtered   Show filtered objects')
			puts('verbose         More verbose')
		print
		puts('Examples')
		with indent(2, quote=' '):
			puts(':: Hosts with host_name = "socket-server" and address = "127.0.0.1"')
			puts(' --list host --host_name \"socket-server\" --address \"127.0.0.1\"')
			print
			puts(':: Some filters with some options')
			puts(' --list host --flap_detection_enabled 1 \\')
			puts('             --process_perf_data 0      \\')
			puts('             --options legend,small')
		print
		puts('You can edit /etc/nagator.cfg for more configuration')
	sys.exit(0)

def legend(what, options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')

	if what == 'host':
		with indent(2, quote=colored.white('    - ')):
			puts(colored.white('Titles'))
		with indent(2, quote=colored.white('      + ')):
			puts(colored.red('red \">>\" are templates'))
			puts(colored.green('green \">>\" are not templates'))
		if not 'small' in options:
			with indent(2, quote=colored.white('    - ')):
				puts(colored.white('Attributes'))
			with indent(2, quote=colored.white('      + ')):
				puts(colored.green('green values are inherited attributes'))
				puts(colored.yellow('yellow values are defined attributes'))
	elif what == 'service':
		with indent(2, quote=colored.white('    - ')):
			puts(colored.white('Titles'))
	else:
		with indent(2, quote=colored.white('   ')):
			puts(colored.white('No legend for this mode'))

def mode_list(what, nc, filtre, options):
	hosts_filtered = []
	hosts_not_filtered = []
	services_filtered = []
	services_not_filtered = []

	if 'verbose' in options:
		if filtre:
			with indent(4, quote=colored.red('==>')):
				puts("Filter :")
			for key, value in sorted(filtre.items()):
				with indent(1, quote=colored.white('     + ')):
					puts("%s: %s" % (key, value))
		print

	if what == 'host':
		for host in nc['all_host']:
			filtered = False
			for element in filtre:
				if element in host.keys():
					#if host[element] != filtre[element]:
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
				hosts_not_filtered.append(host)
			else:
				hosts_filtered.append(host)

		print
		with indent(3, quote=colored.white(' ==> ')):
			puts("Hosts founded")

		if hosts_not_filtered:
			for host_not_filtered in hosts_not_filtered:
				if host_not_filtered.has_key('register'):
					if host_not_filtered['register'] == '0':
						with indent(3, quote=colored.red(' >> ')):
							puts("%s (template)" % host_not_filtered['name'])
					else:
						with indent(3, quote=colored.green(' >> ')):
							puts("%s" % host_not_filtered['host_name'])
				else:
					with indent(3, quote=colored.green(' >> ')):
						puts("%s" % host_not_filtered['host_name'])
				if not 'small' in options:
					for key, value in sorted(host_not_filtered.items()):
						if key != 'meta':
							if key in host_not_filtered['meta']['inherited_attributes']:
								with indent(3, quote=colored.white('    | ')):
									puts("%s: %s" % (colored.blue(key), colored.green(value)))
							else:
								with indent(3, quote=colored.white('    | ')):
									puts("%s: %s" % (colored.blue(key), colored.yellow(value)))
		else:
			with indent(3, quote=colored.white('     ')):
				puts("...nothing...")

		# Hosts filtered
		if 'show_filtered' in options:
			print
			with indent(3, quote=colored.white(' ==> ')):
				puts("Hosts filtered")
	
			if hosts_filtered:
				for host_filtered in hosts_filtered:
					if host_filtered.has_key('register'):
						if host_filtered['register'] == '0':
							with indent(3, quote=colored.red('  >> ')):
								puts("%s (template)" % host_filtered['name'])
						else:
							with indent(3, quote=colored.green('  >> ')):
								puts("%s" % host_filtered['host_name'])
					else:
						with indent(3, quote=colored.green('  >> ')):
							puts("%s" % host_filtered['host_name'])
			else:
				with indent(3, quote=colored.white('     ')):
					puts("...nothing...")

	if what == 'service':
		for service in nc['all_service']:

			filtered = False
			for element in filtre:
				if element in service.keys():
					#if service[element] != filtre[element]:
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
					if service['register'] == '0':
						with indent(3, quote=colored.red(' >> ')):
							puts("%s (template)" % service['name'])
					else:
						with indent(3, quote=colored.green(' >> ')):
							puts("%s" % service['service_description'])
				else:
					with indent(3, quote=colored.green(' >> ')):
						puts("%s" % service['service_description'])

				for key, value in sorted(service.items()):
					if key != 'meta':
						if key in service['meta']['inherited_attributes']:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.green(value)))
						else:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.yellow(value)))
			else:
				services_filtered.append(service)

		if services_filtered:
			print
			with indent(3, quote=colored.white(' ==> ')):
				puts("Services filtered")

		for service_filtered in services_filtered:
			if service_filtered.has_key('register'):
				if service_filtered['register'] == '0':
					with indent(3, quote=colored.red('  >> ')):
						puts("%s (template)" % service_filtered['name'])
				else:
					with indent(3, quote=colored.green('  >> ')):
						puts("%s" % service_filtered['service_description'])
			else:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % service_filtered['service_description'])

def main():

	if debug:
		with indent(4, quote='>>>'):
			puts(colored.white('---------- DEBUG ----------'))
			puts(colored.red('Aruments passed in: ') + str(args.all))
			puts(colored.red('Flags detected: ') + str(args.flags))
			puts(colored.red('Files detected: ') + str(args.files))
			puts(colored.red('NOT Files detected: ') + str(args.not_files))
			puts(colored.red('Grouped Arguments: ') + str(dict(args.grouped)))
			puts(colored.white('---------- DEBUG ----------'))
		print

	mode = None
	what = None
	name = None
	options = []

	if '--options' in args.flags:
		try:
			for option in dict(args.grouped)['--options'][0].split(','):
				options.append(option)
		except:
			pass

	if '--list' in args.flags:
		mode = 'list'
		if 'host' in dict(args.grouped)['--list']:
			what = 'host'
			if 'verbose' in options:
				with indent(4, quote=colored.red('==>')):
					puts('Mode   : List Host')
		elif 'service' in dict(args.grouped)['--list']:
			what = 'service'
			if 'verbose' in options:
				with indent(4, quote='==>'):
					puts('Mode   : List Service')
		else:
			usage()
	else:
		usage()

	# Create filter
	filtre = {}
	for flag in args.flags:
		if flag == None:
			break
		if flag != '--list' and flag != '--options':
			if args.grouped[flag][0]:
				filtre[flag[2:]] = args.grouped[flag][0]


	# Parse nagator.cfg
	nagios_cfg = '/usr/local/nagios/etc/nagios.cfg'

	if os.path.isfile('/etc/nagator.cfg'):
		parser = SafeConfigParser()
		parser.read('/etc/nagator.cfg')
		try:
			nagios_cfg = parser.get('default', 'nagios_cfg')
		except:
			pass
		try:
			for option in parser.get('default', 'options').split(','):
				if option:
					options.append(option.strip())
		except:
			pass

	if not os.path.isfile(nagios_cfg):
		print('Nagios configuration not found (%s)' % nagios_cfg)
		print('Edit your configuration file (/etc/nagator.cfg)')
		sys.exit(1)
	
	options = list(set(options))

	nc = config(nagios_cfg)
	nc.parse()

	if 'verbose' in options:
		if options:
			with indent(4, quote=colored.red('==>')):
				puts('Options: %s' % ' '.join(options))

	if mode == 'list':
		mode_list(what, nc, filtre, options)
		if 'legend' in options:
			legend(what, options)
