# MONKFISH

<a href="url"><img src="https://upload.wikimedia.org/wikipedia/commons/3/30/Monkfish.jpg" align="center" height="300" width="400" ></a>

##About

__MONKFISH__ solves the wholly inane issue of fairly assigning interviewees to restaurants. Like the actual fish, this algorithm is ugly and surprisingly slimy.

__MONKFISH__ works by first assigning first choice dining establishments and then randomly selecting individuals to be removed. __MONKFISH__ also calculates a cumulative score to preferentially bump people who have not yet been bumped. This should maximize the number of people who receive at least one first choice meal, though this has not been at all tested or verified.

##Running MONKFISH

__MONKFISH__ expects a `preferences.csv` file to be stored in the same directory as the core `monkfish.py` file. I'm lazy, so this name must be precise. This file must be very particularly structured, exactly in the format of the `sampleData.csv` file included in this repository.

The attendance cap and data file name can be edited from within the `monkfish.py` file, again because I'm lazy. Don't break anything else trying to do this.

To download __MONKFISH__, execute `git clone https://github.com/ethanagbaker/monkfish.git`.
To run the algorithm, execute `python monkfish.py` in the chosen directory.

###Dependencies
__MONKFISH__ requires `numpy` and `pandas`, which can be installed using `pip install XXX` from the command line.
