#!/usr/bin/env python
import os
import sys
import re
from clint.textui import colored, indent, puts
from clint import args
from pynag.Parsers import config
from pynag import Model
from ConfigParser import SafeConfigParser

from nagator.usage import usage

debug = False

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
	options = []

	if '--options' in args.flags:
		try:
			for option in dict(args.grouped)['--options'][0].split(','):
				options.append(option)
		except:
			pass

	if '-o' in args.flags:
		try:
			for option in dict(args.grouped)['-o'][0].split(','):
				options.append(option)
		except:
			pass

	if '--list' in args.flags or '-l' in args.flags:
		mode = 'list'
		if '--list' in args.flags:
			_mode = '--list'
		elif '-l' in args.flags:
			_mode = '-l'
		try:
			object_module = __import__("nagator.views.%s" % dict(args.grouped)[_mode][0], globals(), locals(), ['list', 'legend'], -1)
			if 'verbose' in options:
				with indent(4, quote=colored.red('==>')):
					puts('Mode   : List %s' % dict(args.grouped)[_mode][0])
		except Exception as err:
			print(' Error: Mode "%s" not available (%s)' % (dict(args.grouped)[_mode][0], err))
			usage()
			sys.exit(1)
	else:
		usage()

	# Create filter
	filtre = {}
	for flag in args.flags:
		if flag == None:
			break
		if flag not in ['--list', '-l', '--options', '-o']:
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
