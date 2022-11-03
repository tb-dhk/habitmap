install:
	chmod +x hbmp
	pip install ansi-colors
	pip install toml
	pip install python-dateutil
setup:
	hbmp habit -a exercise
	hbmp habit -a meditate
	hbmp habit -a hydrate
	hbmp help
