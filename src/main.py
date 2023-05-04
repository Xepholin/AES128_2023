from utilities import *
from encrypt import *
from decrypt import *
from square import *

import settings

if __name__ == "__main__":
    settings.init()

    masterKey = square4()

    print(masterKey)