# Developping with unix micropython version

## Developping with the unix version is very conveniant.

To be able to build stubs are needed for device modules.

These stubs can be found in the current directory

# Most conveniant way to build is with Sublime 3.

Sublime 3 packages dir: ~/.config/sublime-text-3/Packages/

Place in dir ~/.config/sublime-text-3/Packages/user next file:

name: micropython.build.sublime-build
content:

	{
	    "cmd": ["<your path to executable of>/micropython", "$file"],
	    "file_regex": "^[ ]*File \"(...*?)\", line ([0-9]*)",
	    "selector": "py",
	    "env":{"MICROPYPATH":"<workspace>/esp32/stub:<workspace>/esp32/lib"}

	}

<workspace> must be replaced by the location where esp32 is checked out.

In the python path first the stub is added and then the lib path.

In Sublime 3 select the build system, and select micropython.

Now you with <ctrl-B> the python file will run on the host.

