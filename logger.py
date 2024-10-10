import logging

# Configure the logging settings
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler
file_handler = logging.FileHandler('alpha.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create a formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Get the root logger and add the handlers
logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
