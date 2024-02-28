# -*- mode:makefile-gmake; -*-

ifeq ($(OS),Windows_NT)
PYTHON:=py -3
else
PYTHON:=/usr/bin/python3
endif

SHELLCMD:=$(PYTHON) submodules/shellcmd.py/shellcmd.py

.PHONY:test
test:
	$(SHELLCMD) rm-tree build/
	$(SHELLCMD) mkdir build/output/
	$(PYTHON) submodules/beeb/bin/ssd_extract.py -o build/ orig/beebfax82.ssd
	$(PYTHON) tools/extract.py -o build/output/ build/beebfax82/0/$$.FAX1982 orig/beebfax82.ssd
	cd build/output && 7z a -mx=9 ../beebfax82_unpacked.zip *.unpacked.dat
