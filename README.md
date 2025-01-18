# Robot2025 (BUT PYTHON)
this is basically our current drivetrain code in the main branch...BUT PYTHON
_______________________________________________________________________________

this branch is here for reference if anyone wants to know what a drivetrain code template looks like in python.

## For more information, visit the python wpilib documentation at https://robotpy.readthedocs.io/projects/robotpy/en/stable/

## For information on the phoenix6 library, visit https://api.ctr-electronics.com/phoenix6/release/python/autoapi/phoenix6/index.html

### Deployment (for windows bc I don't know how to do on mac or linux) (follow instructions on https://docs.wpilib.org/ for other os installations):

#### run the following command in the selected folder:

py -3 -m pip install robotpy

#### to check if robotpy was installed, run:

py -3 -m robotpy init

#### this will create a robot.py and pyproject.toml

#### then, create a virtual environment with the following command:

py -3 -m venv .venv

#### then, run the following commands:

.venv\Scripts\Activate

robotpy sync

pip install phoenix6

#### the above commands should activate the virtual environment, download the required robotpy libraries, and install the phoenix6 library. For further info, refer to the documentation linked above.
