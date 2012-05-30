Nagator
=======

Nagator is a command line Nagios configuration viewer written in Python.  
It use [pynag](http://code.google.com/p/pynag/) and [clint](https://github.com/kennethreitz/clint) as dependencies.

Installation
------------
<pre>
sudo pip install nagator
</pre>
or get the sources like that:
<pre>
git clone git://github.com/Socketubs/Nagator.git
cd Nagator
sudo python setup.py install
</pre>

Usage
-----
Print list of every hosts (templates not include) with legend
<pre>
nagator --list host --options small,legend --address '(.*)'
</pre>

Print service templates
<pre>
nagator --list service --register 0
</pre>

Aliases
-------
There are some aliases examples.
<pre>
# Print pretty list of every hosts (templates not include)
alias nagator-hosts="nagator --list host --options small --address '(.*)'"

# Same with services
alias nagator-services="nagator --list service --options small --host_name '(.*)'"
</pre>

Todo
----

 * If service or host have no register option and give filter with register 1, print it
 * Convert Readme to Rst
 * List sorted Hosts/Services
 * Implement Contacts, ContactGroups... listing
 * Create Python package

No licence, copy it.
