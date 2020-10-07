# Pokemon w/ BCI

This is the github repo for our capstone project and should serve as the main source for completed work. This is also a great way for us to contribute to the project and test additions in new branchs.

## Getting Started

You should clone the master branch to your personal computer. Get a fresh install of python 3.8 if you don't already have one, the build script will assume that "python" in your terminal is mapped to Python 3.8 on your computer.

### Prerequisites

* Python 3.8
* 'python' command in terminal/cmd mapped to Python 3.8 exe
* SDL2 (more info in setup)

### Setting Up

Getting this onto you personal computer can be done by following the instructions below.

* Setting up Git to work with your terminal/cmd
* In terminal
  * Move to directory you want the folder to live in
  * run "git clone https://github.com/PeZeqo/capstone_pokemon_bci.git"

In order to run anything involving PyBoy you'll need SDL2. We'll also need to let your computer know where you have SDL2 if your on Windows, or you can just install the package if you're on a Unix based system.

* SDL2 dev lib installed and PYSDL2_DLL_PATH variable added as env variable (Windows)
  * Install the dev library zip at (https://www.libsdl.org/download-2.0.php)
  * Extract SDL2 folder somewhere you can navigate to
  * Open Environment Variables Window
  * "New..." System Variable
  * Variable name: "PYSDL2_DLL_PATH"
  * Variable value: "path_to_sdl_dir\lib\x64"
* SDL2 installed through package manager (Unix)
  * Ubuntu: sudo apt install libsdl2-dev
  * Fedora: sudo dnf install SDL2-devel
  * macOS: brew install sdl2


### Running

Please first ensure that you have all required libraries installed for Python. This can be done by running the following in cmd/terminal: 
* python -m pip install -r Requirement.txt

We currently only have a testing window coded, but that can be run through the launch scripts.

* Launch.sh  for Unix
* Launch.bat for Windows

You can also run any python file with:
* python -m FileName


### Contributing

We want to make sure that we keep the master branch clean, as in it will always contain functional, reviewed code. Contributing to this should be done by working and testing in sperate branches from master, and then creating pull requests to merge so that others can review before we update our master branch.

To do this locally you can follow this guide:

* In terminal move to the directory containing the repo
* git checkout -b new_branch_name
* Write code and make changes
* git add -A
* git commit -m "brief message about what this set of changes is doing"
* git push origin
  * if this branch has never been pushed back to the remote repo outside of your local PC run this:
  * git push --set-upstream origin new_branch_name
* From here you can come to this repo and move to your branch using the branch selector
* Make a new pull request from there to merge into master
* Have someone review it and approve it
* Merge and delete the branch
  
Small note: if you use a new library, make sure to update Requirement.txt to reflect that new dependency. You can do the following to check what to update the file too:

* in cmd/terminal run "python -m pip freeze"
* this should print the whole list of python libraries you have
* copy this into Requirement.txt
* make sure this update is pushed as part of your branch
