
VERSION := $(shell cat csb.py | grep "version =" | grep -oE "[0-9\.]+")

all: csb_${VERSION}.deb

csb_${VERSION}.deb: csb.py csui.py Makefile
	rm -rf fs
	mkdir -p fs/DEBIAN
	mkdir -p fs/usr/bin
	mkdir -p fs/usr/share/man/man1
	mkdir -p fs/usr/share/doc/csb
	cp csb.py fs/usr/bin/csb
	cat csb.1 | gzip -9 > fs/usr/share/man/man1/csb.1.gz
	cp control fs/DEBIAN/control
	sed -i s/VERSION/${VERSION}/ fs/DEBIAN/control
	cp copyright fs/usr/share/doc/csb/copyright
	fakeroot dpkg -b fs csb_${VERSION}.deb
	rm -rf fs
