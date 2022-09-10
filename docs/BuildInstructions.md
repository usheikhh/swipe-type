# Swipe-Type build instructions

## Required Interpreters

You need Python >= 3 and NodeJS >= 10 interpreters.

## Javascript

## Prerequisites

Make sure you have all the dependencies installed:

### MacOS

The [Homebrew](https://brew.sh) package manager will make the installation easier

```console
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install node with Homebrew:

```console
brew install node
```

Install python3 with Homebrew:

```console
brew install python
```

Install prerequisite dependencies to the node canvas package

```console
brew install pkg-config cairo pango libpng jpeg giflib librsvg
```

Export the package configuration path

```console
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:/opt/X11/lib/pkgconfig
```

Install dependencies in `package.json`

**NOTE**: This command must be run when in the `js` directory

```console
npm install
```

### Windows

The dependencies can be installed directly with:

```console
npm install
```

**NOTE**: This command must be run when in the `js` directory

### Plot swiped words

The `plotlog.js` file renders a swipe trajectory as a PNG file.

```sh
~$ node plotlog.js -h
Usage:
  node plotlog.js [OPTION]
Options:
  -l, --logFile=ARG Log file
  -w, --word=ARG    Word to plot
  -f, --failed      Show failed word, if present
  -v, --verbose     Display debug info
  -h, --help        Display this help
```

Example: assuming that the word "hello" is in `somefile.log` file,
this will create the file `somefile-hello-0.png`:

```sh
~$ node plotlog.js -l /path/to/somefile.log -w hello
```

The output filename pattern in always "username-word-flag.png", where "username" is the user ID (swipe log filename), "word" is the swiped word, and "flag" is either 0 (default) or 1 if the argument `-f` (or `--failed`) is provided.

## Python

Create a virtual environment in the project root:

```console
python3 -m venv env
```

Activate the virtual environment

```console
source env/bin/activate
```

Install libenchant for PyEnchant

```console
brew update
brew install enchant
```

Install the dependencies

```console
pip3 install -r src/core/requirements.txt
```
