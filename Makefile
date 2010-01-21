
VERSION := $(shell cat csb.py | grep "version =" | grep -oE "[0-9\.]+")

all: csb_${VERSION}.deb

csb_${VERSION}.deb: csb.py csui.py Makefile
	rm -rf fs
	mkdir -p fs/DEBIAN
	mkdir -p fs/usr/bin
	mkdir -p fs/usr/share/man/man1
	cp csb.py fs/usr/bin/csb
	cat csb.1 | gzip > fs/usr/share/man/man1/csb.1.gz
	echo "Package: csb" >> fs/DEBIAN/control
	echo "Version: ${VERSION}" >> fs/DEBIAN/control
	echo "Section: misc" >> fs/DEBIAN/control
	echo "Priority: optional" >> fs/DEBIAN/control
	echo "Architecture: all" >> fs/DEBIAN/control
	echo "Depends: python (>=2.5)" >> fs/DEBIAN/control
	echo "Recommends: python-mysqldb" >> fs/DEBIAN/control
	echo "Maintainer: Shish Moom <shish@shishnet.org>" >> fs/DEBIAN/control
	echo "Description: Curses SQL Browser" >> fs/DEBIAN/control
	echo " A curses-based browser and editor for SQL databases" >> fs/DEBIAN/control
	fakeroot dpkg -b fs csb_${VERSION}.deb
	rm -rf fs
