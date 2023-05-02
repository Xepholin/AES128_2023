from utilities import *
from encrypt import *
from decrypt import *
from square import *

if __name__ == "__main__":
    subKeys = KeyScheduler("0123456789abcd")
    #0x565fffcc4e021c7add6910cc13ee5df1
    #0x02
    delta_set = setup("0123456789abcd")
    reverse_set = reverseState(0x02, 5, delta_set)

    print(checkKeyGuess(0x02, reverse_set))