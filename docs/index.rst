Nutrition Planner
=================

Autore: Termine Christian Domenico

Descrizione
-----------

Il progetto integra machine learning, inferenza Prolog e un dataset alimentare
per stimare le calorie bruciate durante una sessione di allenamento e generare
un piano alimentare giornaliero o settimanale coerente con i dati fisici
dell'utente.

Il programma principale e' ``predict_models.py``. Lo script carica i modelli
addestrati, interroga la base di conoscenza Prolog, predice le calorie bruciate
e richiama il modulo ``nutrition_planner.py`` per costruire il piano alimentare.

Flusso dell'applicazione
------------------------

1. Raccolta dei dati dell'utente: sesso, eta', peso, altezza, allenamento,
   battiti medi, massa grassa, massa magra, giorni del piano e alternative
   giornaliere.
2. Inferenza Prolog per workout consigliato, intensita' e durata ottimale.
3. Predizione delle calorie bruciate tramite modelli di regressione.
4. Calcolo di metabolismo basale, fabbisogno calorico e macronutrienti.
5. Generazione del piano alimentare usando ``dataset/alimenti.csv``.

Gli input sono validati con controlli su intervalli ammessi e conversione dei
decimali inseriti con virgola o punto.

Dataset utilizzati
------------------

``dataset/gym_members_exercise_tracking.csv``
   Dataset usato per l'addestramento dei modelli predittivi delle calorie
   bruciate.

``dataset/alimenti.csv``
   Dataset alimentare che contiene calorie, proteine, carboidrati e grassi
   per 100 grammi di alimento. Viene usato per generare colazione, pranzo,
   spuntino e cena, con variazioni tra alternative e giorni della settimana.

Esecuzione
----------

Per eseguire il programma completo dalla cartella principale del progetto:

.. code-block:: bash

   python3 predict_models.py

I grafici e i modelli salvati vengono aggiornati solo rilanciando gli script di
training nelle cartelle ``apprendimento_supervisionato`` e
``apprendimento_probabilistico``.

Per generare la documentazione HTML:

.. code-block:: bash

   python3 -m pip install -r requirements-docs.txt
   python3 -m sphinx -b html docs docs/_build/html

Link GitHub
-----------

La documentazione Prolog della Knowledge Base e' disponibile anche online:

``https://github.com/Christian032003/Nutrition-Planner/tree/main/kb/doc``

.. toctree::
   :maxdepth: 2
   :caption: Contenuti:

   modules
