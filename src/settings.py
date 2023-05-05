def init():
    global secret_key
    secret_key = 0x000102030405060708090a0b0c0d0e0f

    if type(secret_key) == int:
        if secret_key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
    else:
        raise TypeError()