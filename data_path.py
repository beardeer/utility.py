# from os import getcwd
import os
from getpass import getuser
import platform

USER_NAME = getuser()

if platform.system() == 'Windows':
	DROPBOX_FOLDER = os.path.join("C:\\", 'Users', USER_NAME, 'Dropbox')
else:
	raise NotImplementedError()

DROPBOX_DATA_FOLDER = os.path.join(DROPBOX_FOLDER, 'Data')

CURRENT_DEVELOPMENT_FOLDER = os.getcwd()

# CURRENT_DEVELOPMENT_DATA_FOLDER = CURRENT_DEVELOPMENT_FOLDER + "/Data/"

if __name__ == "__main__":
    print DROPBOX_FOLDER
    print DROPBOX_DATA_FOLDER
    print CURRENT_DEVELOPMENT_FOLDER
