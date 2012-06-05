import re
from clint.textui import colored, indent, puts

def list(nc, filtre, options):
	contacts_founded = []
	contacts_template_founded = []

	contacts_filtered = []
	contacts_template_filtered = []

	try:
		contacts = nc['all_contact']
	except KeyError:
		with indent(3, quote=colored.white(' ==> ')):
			puts("No contact")
		sys.exit(0)
	except Exception as err:
		with indent(3, quote=colored.white(' ==> ')):
			puts("Something went wront (%)" % err)
		sys.exit(1)

	for contact in contacts:
		filtered = False
		for element in filtre:
			if element in contact.keys():
				try:
					filtre_pattern = re.compile(filtre[element])
				except:
					with indent(3, quote=colored.red(' >> ')):
						puts('Regexp error')
					sys.exit(1)
				if not filtre_pattern.match(contact[element]):
					filtered = True
					break
				else:
					filtered = False
			else:
				filtered = True
				break

		if not filtered:
			if contact.has_key('register'):
				if contact['register'] == 0:
					contacts_founded.append(contact)
				else:
					contacts_template_founded.append(contact)
			else:
				contacts_founded.append(contact)
		else:
			if contact.has_key('register'):
				if contact['register'] == 0:
					contacts_filtered.append(contact)
				else:
					contacts_template_filtered.append(contact)
			else:
				contacts_filtered.append(contact)

	contacts_founded = sorted(
						contacts_founded,
						key=lambda k: k['meta']['defined_attributes']['contact_name']) 
	contacts_template_founded = sorted(
						contacts_template_founded,
						key=lambda k: k['name']) 

	contacts_filtered = sorted(
						contacts_filtered,
						key=lambda k: k['meta']['defined_attributes']['contact_name']) 
	contacts_template_filtered = sorted(
						contacts_template_filtered,
						key=lambda k: k['name']) 


	with indent(3, quote=colored.white(' ====> ')):
		puts("Contacts founded")

	if contacts_template_founded:
		for contact in contacts_template_founded:
			with indent(3, quote=colored.red(' >> ')):
				puts("%s" % contact['name'])
			if not 'small' in options:
				for key, value in sorted(contact.items()):
					if key != 'meta':
						if key in contact['meta']['inherited_attributes']:
							with indent(3, quote=colored.white('    | ')):
							   puts("%s: %s" % (colored.blue(key), colored.green(value)))
						else:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	if contacts_founded:
		for contact in contacts_founded:
			with indent(3, quote=colored.green(' >> ')):
				puts("%s" % contact['contact_name'])
			if not 'small' in options:
				for key, value in sorted(contact.items()):
					if key != 'meta':
						if key in contact['meta']['inherited_attributes']:
							with indent(3, quote=colored.white('    | ')):
							   puts("%s: %s" % (colored.blue(key), colored.green(value)))
						else:
							with indent(3, quote=colored.white('    | ')):
								puts("%s: %s" % (colored.blue(key), colored.yellow(value)))

	with indent(3, quote=colored.white(' ==> ')):
		puts("Total: %s" % (len(contacts_founded) + len(contacts_template_founded)))

	if 'show_filtered' in options:
		print('')
		with indent(3, quote=colored.white(' ====> ')):
			puts("Contacts filtered")

		if contacts_template_filtered:
			for contact in contacts_template_filtered:
				with indent(3, quote=colored.red(' >> ')):
					puts("%s" % contact['name'])

		if contacts_filtered:
			for contact in contacts_filtered:
				with indent(3, quote=colored.green(' >> ')):
					puts("%s" % contact['contact_name'])

		with indent(3, quote=colored.white(' ==> ')):
			puts("Total: %s" % (len(contacts_filtered) + len(contacts_template_filtered)))


def legend(options):
	print
	with indent(3, quote=colored.white(' ==> ')):
		puts('Legend')

	with indent(2, quote=colored.white('   - ')):
		puts(colored.white('Titles'))
	with indent(2, quote=colored.white('     + ')):
		puts(colored.red('red \">>\" are templates (name atttribute)'))
		puts(colored.green('green \">>\" are not templates (contact_name attribute)'))
	if not 'small' in options:
		with indent(2, quote=colored.white('   - ')):
			puts(colored.white('Attributes'))
		with indent(2, quote=colored.white('     + ')):
			puts(colored.green('green values are inherited attributes'))
			puts(colored.yellow('yellow values are defined attributes'))
