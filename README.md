For some reason, my interest was caught by this topic here:
https://www.stardot.org.uk/forums/viewtopic.php?p=418306

So I wrote a thing to (hopefully) decode the pages.

# git clone

This repo has submodules. Clone it with `--recursive`:

    git clone --recursive https://github.com/tom-seddon/beebfax82
	
Alternatively, if you already cloned it non-recursively, you can do
the following from inside the working copy:

    git submodule init
	git submodule update

(The code won't build without fiddling around if you download one of
the archive files from GitHub - a GitHub limitation. It's easiest to
clone it as above.)

# build prerequisites

* Python 3.x
* 7zip command line

# build steps

Type `make` from the root of the working copy.

The build output is a bunch of files in `build/output`: `*.raw.dat`
(RLE-encoded page data for each page), and `*.unpacked.dat` (40*25
teletext screen data for each page, suitable for displaying on a BBC
Micro or running through a teletext screen data conversion tool or
something). The name of each file is its page number.

There's also `build/beebfax82_unpacked.zip`, a zipped-up copy of the
unpacked data.
