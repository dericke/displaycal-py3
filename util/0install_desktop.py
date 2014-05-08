#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from __future__ import with_statement
from glob import glob
import os
import re
import shutil
import sys

from dispcalGUI.meta import name as appname, domain


def zeroinstall_desktop(datadir="/usr/share"):
	""" Install icon and desktop files for 0install implementation """
	appdir = os.path.join(datadir, "applications")
	if not os.path.isdir(appdir):
		os.makedirs(appdir)
	feeduri = "http://%s/0install/%s.xml" % (domain.lower(), appname)
	for desktopfilename in glob(os.path.join("misc", "%s*.desktop" % appname)):
		desktopbasename = os.path.basename(desktopfilename)
		scriptname = re.sub("\.desktop$", "", desktopbasename)
		for size in [16, 22, 24, 32, 48, 128, 256]:
			icondir = os.path.join(datadir, "icons", "hicolor",
								   "%sx%s" % (size, size), "apps")
			if not os.path.isdir(icondir):
				os.makedirs(icondir)
			shutil.copy(os.path.join(appname, "theme", "icons",
									 "%sx%s" % (size, size),
									 scriptname + ".png"), icondir)
		with open(desktopfilename) as desktopfile:
			contents = desktopfile.read()
		cmd = re.sub("^%s" % appname, "run", scriptname)
		for pattern, repl in [("Exec=.+",
							   "Exec=/usr/bin/0launch --command=%s -- %s %%f" %
							   (cmd, feeduri))]:
			contents = re.sub(pattern, repl, contents)
		with open(os.path.join(appdir, desktopbasename), "w") as desktopfile:
			desktopfile.write(contents)


if __name__ == "__main__":
	zeroinstall_desktop(*sys.argv[1:])
