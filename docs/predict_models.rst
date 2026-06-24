predict\_models module
======================

Il modulo ``predict_models.py`` e' lo script principale del progetto. Integra:

- caricamento dei modelli di machine learning gia' addestrati;
- interrogazione della base di conoscenza Prolog;
- predizione delle calorie bruciate;
- raccolta e controllo degli input dell'utente;
- generazione del piano alimentare tramite ``nutrition_planner.py``.

L'esecuzione del modulo produce un output composto dai risultati Prolog, dalle
predizioni dei modelli e dal piano alimentare giornaliero, con alternative, o
settimanale.

Input richiesti
---------------

Lo script richiede sesso, eta', peso, altezza, tipo di allenamento, durata della
sessione, ore di allenamento settimanali, battiti medi, percentuale di massa
grassa, massa magra, giorni del piano e numero di alternative giornaliere.

I valori vengono controllati prima di essere usati dai modelli, dalla base
Prolog e dal modulo nutrizionale.

.. automodule:: predict_models
   :members:
   :undoc-members:
   :show-inheritance:
