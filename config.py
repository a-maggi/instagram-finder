'''
Config functions such as read settings from file, logging, etc.
'''
import logging
import shutil
import os, sys
from configparser import SafeConfigParser
import ast

def Config_file(section, option):
	config = SafeConfigParser()
	config.read('config.conf')
	try:
		value = config.get(section, option)
	except Exception as e:
		logging.error('Error reading config file!')
		logging.error(e)
		sys.exit(1)
	return value

def Logging():
        if Debugging == True:
                Logging_level = logging.DEBUG
        else:
                Logging_level = logging.INFO
        logging.basicConfig(filename=Log_file,level=Logging_level, format='%(asctime)s %(levelname)s:%(message)s', datefmt='%d/%m/%Y %I:%M:%S %p')

        log = logging.getLogger(__name__)                                  
        log.setLevel(Logging_level)
        handler = logging.StreamHandler(sys.stdout)                             
        handler.setLevel(logging.INFO)                                        
        handler.setFormatter('%(asctime)s %(levelname)s:%(message)s')                                        
        log.addHandler(handler)
        logging.info('Starting application: version %s' %Version)

def Remove_folder(folder):
    if (os.path.exists(folder) == True):
        try:
            shutil.rmtree(folder)
            logging.debug("Removing folder: " + folder)
        except IOError as e:
            logging.error(e)

def Preconditions(folder):
	if (os.path.exists(folder) == False):
		try:
			os.mkdir(folder)
			logging.debug("Creating folder: " + folder)
		except IOError as e:
			logging.error(e)

# Setup options
TOKEN = Config_file('api','TOKEN')
Time_delay = Config_file('delays','Time_delay')
Log_file = Config_file('files','Log_file')
API_USER = Config_file('api','API_USER')
Version = Config_file('version','Version')
# Enable storing html to debug.log file + set logging level
Debugging = ast.literal_eval(Config_file('debug','Debugging'))
