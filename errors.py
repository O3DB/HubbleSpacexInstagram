from merry import Merry
from requests.exceptions import ConnectionError, HTTPError 


merry = Merry()


@merry._except(HTTPError)
def httperror():
    print('HTTP Error')


@merry._except(ConnectionError)
def connectionerror():
    print('Connection Error')


