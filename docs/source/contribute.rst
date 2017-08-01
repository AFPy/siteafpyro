.. _orga:

Organiser un AFPyro
=====================

* Trouver un bar sympa !

* :ref:`commit` les détails de l'évènement.

.. _commit:

Commiter sur afpyrosite
------------------------

 .. code-block:: bash

    # éventuellement dans un venv

    hg clone http://hg.afpy.org/siteafpyro/
    cd siteafpyro

    # D'un côté, lancez ceci, -la première fois, le bootstrap prend du temps
    python bootstrap.py
    ./update.py -s

    # pendant ce temps, modifiez ou créez le présent site (par exemple, ajoutez une
    # entrée dans docs/source/dates/2013/
    # Une fois le script 'update.py' lancé, vérifiez votre œuvre sur http://127.0.0.1:6671

    # committez
    hg add .
    hg commit -m"Annonce Afpyro le xx à tataouin"

    # invitez le monde
    hg push

    # lors du push vous sera demandé votre identifiant/password du site afpy.org
    # un hook rebuilde le site vos modifs sont en ligne

