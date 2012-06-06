import sys
from clint.textui import colored, indent, puts

def usage():
	with indent(1, quote=' '):
		puts('Usage: nagator --list [OBJECT] [OPTIONS] [FILTERS]')
		print
		puts('Modes')
		with indent(2, quote=' '):
			puts('--list, -l <object>')
		with indent(6):
			puts('hosts,hostgroups,services,servicegroups,')
			puts('contacts,contactgroups,commands,timeperiods')
		print
		puts('Filters')
		with indent(2, quote=' '):
			puts('You can use every nagios configuration option')
		print
		puts('Options')
		with indent(2, quote=' '):
			puts('--options, -o <option,option,..>')
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
			puts('            --process_perf_data 0   \\')
			puts('            --options legend,small')
		print
		puts('You can edit /etc/nagator.cfg for more configuration')
	sys.exit(0)
