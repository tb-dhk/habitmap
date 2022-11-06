install:
	pip install ansicolors
	pip install toml
	pip install python-dateutil
setup:
	hbmp habit -a exercise
	hbmp habit -a meditate
	hbmp habit -a hydrate
	hbmp
