import re
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	commands_founded = []
	commands_filtered = []

	try:
		commands = nc['all_command']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No command")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for command in commands:
   		filtered = False
	   	for element in filtre:
			if element in command.keys():
   				try:
	   			   filtre_pattern = re.compile(filtre[element])
				except:
		   			with indent(3, quote=colored.red(' >> ')):
			   			puts('Regexp error')
				   	sys.exit(1)
				if not filtre_pattern.match(command[element]):
   					filtered = True
	   				break
				else:
		   			filtered = False
			else:
   				filtered = True
	   			break

		if not filtered:
   			commands_founded.append(command)
	   	else:
			commands_filtered.append(command)

	with indent(3, quote=colored.white(' ====> ')):
		puts("Commands founded")

	if commands_founded:
		for command in commands_founded:
			with indent(3, quote=colored.green(' >> ')):
			  	puts("%s" % command['command_name'])

			if not 'small' in options:
			   	with indent(3, quote=colored.white('    | ')):
					puts("%s: %s" % (colored.blue("command_line"), colored.yellow(command['meta']['defined_attributes']['command_line'])))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % len(commands_founded))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Commands filtered")

		if commands_filtered:
			for command in commands_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % command['command_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % len(commands_filtered))

def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')
	with indent(2, quote=colored.white('     + ')):
		puts('titles after \">>\" are command_name')
