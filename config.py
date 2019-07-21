import os
from dotenv import load_dotenv

load_dotenv()

verify_ssl = False
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')