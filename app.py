from microphone import *
from connect_database import *

if __name__ == "__main__":
    # Start microphone
    listen(old=0, error_count=0,min_decibel=50, max_decibel=100)
    # connect to database
