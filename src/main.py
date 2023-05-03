from utilities import *
from encrypt import *
from decrypt import *
from square import *

if __name__ == "__main__":
    subKeys = KeyScheduler("0123456789abcd")
    #0x565fffcc4e021c7add6910cc13ee5df1

    subKey4 = find_subKey4("0123456789abcd")

    print(hex(subKey4))