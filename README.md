# Chiffrement par bloc AES128 et Attaque intégrale contre une version réduite de l'AES128

Dans le cadre de notre UE de Projet en L3 pour l'année 2023, nous avons dû implémenter l'AES128 afin de faire une attaque intégrale.<br />
Bien sûr, l'attaque est effectuée sur une version réduite de l'AES, et plus précisément, nous faisons une attaque sur l'AES à 4 tours.

**Version de Python utilisée : Python 3.10**

Les fonctions possèdent toute une description placée dans chacun d'entre eux.
Un Makefile est disponible pour faire les commandes par défaut, utiliser la commande ``make``.

    Pour lancer les tests unitaires:
        make test | python src/unittests.py

Sinon, pour l'utilisation du programme:

    Pour chiffrer un message:
        python src/main.py encrypt "message à chiffrer" "clé à utiliser"

    Pour déchiffrer un message:
        python src/main.py decrypt "message à déchiffrer" "clé à utiliser"

    Pour l'attaque:
        python src/main.py attack
L'attaque utilise la clé secrète présente dans le fichier ``settings.py``, si vous voulez la modifier, changer simplement la valeur de la variable "secret_key" à la ligne 8.<br />

La clé secrète doit être un entier, équivalent à un hexadécimal possédant 32 bits ou moins, vous pouvez prendre comme exemple les clés ci-dessous, qui sont des clés possibles:
    
    0x2b7e151628aed2a6abf7158809cf4f3c
    0x4D6251655468576D5A7134743777217A
    0x28472B4B6250655368566D5971337436
    0x413F442A472D4B6150645367566B5970
    0x3778214125442A462D4A614E64526755
    0x7134743777217A25432A46294A404E63
    0x566D597133743677397A244326452948
    0x645367566B5970337336763979244226
    0x4A614E645267556B5870327335763879
    0x2646294A404E635266556A586E327235
    0x7A244226452948404D635166546A576E


<ins>Lien du répertoire Github: https://github.com/Xepholin/AES128_2023<ins>

