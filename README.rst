Description
-----------

Nagator is a command line Nagios configuration viewer written in Python.  
It use `pynag <http://code.google.com/p/pynag/>`_ and `clint <https://github.com/kennethreitz/clint>`_ as dependencies.

Installation
------------

Install with pip:::

	pip install nagator

Usage
-----

Print list of every hosts (templates not include) with legend:::

	nagator --list host --options small,legend --address '(.*)'

Print service templates:::

	nagator --list service --register 0

Aliases
-------

There are some aliases examples.::

	# Print pretty list of every hosts (templates not include)
	alias nagator-hosts="nagator --list host --options small --address '(.*)'"

	# Same with services
	alias nagator-services="nagator --list service --options small --host_name '(.*)'"

Todo
----

- If service or host have no register option and give filter with register 1, print it
- Implement hostdependency, hostdependency
- Better view for timeperiods

See `LICENSE <https://github.com/Socketubs/Nagator/blob/master/LICENSE>`_.
