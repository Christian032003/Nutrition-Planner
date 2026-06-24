dataset package
===============

Dataset del progetto
--------------------

Il progetto utilizza due file CSV principali:

``dataset/gym_members_exercise_tracking.csv``
   Contiene i dati relativi agli allenamenti ed e' usato nella fase di
   addestramento dei modelli di regressione.

``dataset/alimenti.csv``
   Contiene il dataset alimentare usato da ``nutrition_planner.py``. Ogni riga
   descrive un alimento con categoria, pasti compatibili, calorie e
   macronutrienti per 100 grammi. Il dataset e' stato ampliato con piu'
   alternative proteiche, fonti di carboidrati, frutta, verdura e grassi per
   permettere piani giornalieri multipli e piani settimanali piu' vari.

Struttura di ``dataset/alimenti.csv``:

.. code-block:: text

   alimento,categoria,pasti,kcal_100g,proteine_100g,carboidrati_100g,grassi_100g

Il campo ``pasti`` puo' contenere piu' valori separati da ``|``: in questo modo
lo stesso alimento puo' essere usato, ad esempio, sia a pranzo sia a cena.

Submodules
----------

dataset.dataset\_utils module
-----------------------------

.. automodule:: dataset.dataset_utils
   :members:
   :undoc-members:
   :show-inheritance:

Module contents
---------------

.. automodule:: dataset
   :members:
   :undoc-members:
   :show-inheritance:
