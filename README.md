# Projet_Crypto_2023

Dans le cadre de notre UE Projet, nous avons dû implémenté l'AES128 afin de faire une attaque intégrale.
Bien-sûr, l'attaque est effectué sur une version réduite de l'AES, et plus précisément, nous faisons une attaque sur l'AES à 4 tours.

**Version de Python utilisée : Python 3.10**

Les fonctions possèdent tous un description placé dans chacuns d'entre eux.
Un Makefile est disponible pour faire les commandes par défaut, utiliser la commande ``make``.

    Pour lancer les tests unitaires:
        make test | python src/unittests.py

Sinon pour l'usage:

    Pour chiffrer un message:
        python src/main.py encrypt "message à chiffrer" "clé à utiliser"

    Pour déchiffrer un message:
        python src/main.py decrypt "message à déchiffrer" "clé à utiliser"

    Pour l'attaque:
        python src/main.py attack
    L'attaque utilise la clé secrète présent dans le fichier settings.py, si vous voulez la modifier, changer simplement la valeur de la variable "secret_key" à la ligne 8.


Lien du répertoire Github: https://github.com/Xepholin/AES128_2023

