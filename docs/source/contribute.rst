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

    git clone https://github.com/AFPy/siteafpyro
    cd siteafpyro
    pip install -r requirements.txt

    # Faites vous une branche
    git checkout -b afpyro-a-tataouin

    # Modifiez ce que vous vouliez (par exemple, ajoutez une
    # entrée dans docs/source/dates/2020/)

    # Testez avec
    ./update.sh
    FLASK_APP=afpyro FLASK_ENV=development flask run

    # committez
    git add -u
    git commit -m "Annonce Afpyro le xx à tataouin"

    # Rendez ça public
    git push origin

    # Cliquez sur le lien pour ouvrir la pull request, une fois
    acceptée un script mettra ça en prod.
