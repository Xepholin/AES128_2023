def init():

    """
    Initialisation de la clé secrèete pour l'attaque.
    """

    global secret_key
    secret_key = 0x2b7e151628aed2a6abf7158809cf4f3c

    if type(secret_key) == int:
        if secret_key > 2**128:
            raise ValueError("Le bloc de lettres fait plus de 16 caractères.")
    else:
        raise TypeError()