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
		puts('Usage: nagator --list [OBJECT] [OPTIONS] [FILTERS]')
		print
		puts('Modes')
		with indent(2, quote=' '):
			puts('--list <object>')
		with indent(6):
			puts('hosts,hostgroups,services,servicegroups')
			puts('commands,contacts,contactgroups,timeperiods')
		print
		puts('Filters')
		with indent(2, quote=' '):
			puts('You can use every nagios configuration option')
		print
		puts('Options')
		with indent(2, quote=' '):
			puts('--options <option,option,..>')
		with indent(6):
			puts('legend              Legend at the end of output')
			puts('small               Smaller output')
			puts('show_filtered       Show filtered objects')
			puts('verbose             More verbose')
		print
		puts('Examples')
		with indent(2, quote=' '):
			puts(':: Hosts with host_name = "socket-server" and address = "127.0.0.1"')
			puts(' --list hosts --host_name \"socket-server\" --address \"127.0.0.1\"')
			print
			puts(':: Some filters with some options')
			puts(' --list hosts --flap_detection_enabled 1 \\')
			puts('			  --process_perf_data 0	  \\')
			puts('			  --options legend,small')
		print
		puts('You can edit /etc/nagator.cfg for more configuration')
	sys.exit(0)

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
		try:
			object_module = __import__("nagator.views.%s" % dict(args.grouped)['--list'][0], globals(), locals(), ['list', 'legend'], -1)
			if 'verbose' in options:
				with indent(4, quote=colored.red('==>')):
					puts('Mode   : List %s' % dict(args.grouped)['--list'][0])
		except Exception as err:
			print(' Error: Mode "%s" not available (%s)' % (dict(args.grouped)['--list'][0], err))
			usage()
			sys.exit(1)
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
		# Verbose
		if 'verbose' in options:
			if filtre:
				with indent(4, quote=colored.red('==>')):
					puts("Filter :")
				for key, value in sorted(filtre.items()):
					with indent(1, quote=colored.white('	 + ')):
						puts("%s: %s" % (key, value))
		print

		# List
		object_module.list(nc, filtre, options)
		
		# Legend
		if 'legend' in options:
			object_module.legend(options)
