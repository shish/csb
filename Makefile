
VERSION := $(shell cat csb.py | grep "version =" | grep -oE "[0-9\.]+")
#SPLIT := $(shell nl -b a csb.py | grep "version = " | cut -f 1 | grep -oE "[0-9]+")

all: csb_${VERSION}.deb

csb_${VERSION}.deb: csb.py csui.py Makefile control copyright changelog
	rm -rf fs
	mkdir -p fs/DEBIAN
	mkdir -p fs/usr/bin
	mkdir -p fs/usr/share/man/man1
	mkdir -p fs/usr/share/doc/csb
	mkdir -p fs/usr/share/csb/
	cp csb.py fs/usr/bin/csb
	cp csui.py fs/usr/share/csb/csui.py
	cat csb.1 | gzip -9 > fs/usr/share/man/man1/csb.1.gz
	cp control fs/DEBIAN/control
	sed -i s/VERSION/${VERSION}/ fs/DEBIAN/control
	cp copyright fs/usr/share/doc/csb/copyright
	cat changelog | gzip -9 > fs/usr/share/doc/csb/changelog.gz
	fakeroot dpkg -b fs csb_${VERSION}.deb
	rm -rf fs
