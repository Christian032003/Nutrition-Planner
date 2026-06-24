nutrition\_planner module
=========================

Il modulo ``nutrition_planner.py`` gestisce la parte nutrizionale del progetto.
Carica il dataset ``dataset/alimenti.csv`` e usa i dati dell'utente per
calcolare:

- massa magra stimata;
- metabolismo basale;
- fabbisogno calorico giornaliero;
- obiettivo alimentare;
- macronutrienti giornalieri;
- piano alimentare suddiviso in colazione, pranzo, spuntino e cena;
- piu' alternative giornaliere;
- piano settimanale fino a 7 giorni.

Il modulo puo' essere eseguito anche singolarmente, ma nel flusso completo viene
richiamato da ``predict_models.py``.

Funzionalita' principali
------------------------

``nutrition_planner.py`` contiene funzioni per:

- validare input numerici interi e decimali;
- stimare la massa magra quando l'utente inserisce ``0``;
- calcolare BMR, TDEE, obiettivo calorico e macronutrienti;
- selezionare alimenti compatibili con il pasto dal file
  ``dataset/alimenti.csv``;
- bilanciare le grammature per avvicinare il totale calorico al target;
- generare varianti diverse usando un indice di variante;
- stampare il piano giornaliero, le alternative o il piano settimanale.

Il piano alimentare e' un supporto informativo: non sostituisce il parere di un
professionista della nutrizione.

.. automodule:: nutrition_planner
   :members:
   :undoc-members:
   :show-inheritance:
