# Nutrition Planner

Autore: Termine Christian Domenico

## Descrizione

Il progetto integra tecniche di machine learning, inferenza Prolog e gestione di dataset alimentari per stimare le calorie bruciate durante una sessione di allenamento e generare un piano alimentare giornaliero o settimanale coerente con i dati fisici dell'utente.

Il flusso principale e' gestito da `predict_models.py`, che:

1. raccoglie i dati dell'utente;
2. interroga la base di conoscenza Prolog;
3. predice le calorie bruciate tramite modelli di regressione;
4. calcola metabolismo basale, fabbisogno calorico e macronutrienti;
5. genera un piano alimentare usando il dataset `dataset/alimenti.csv`, con possibilita' di ottenere piu' alternative giornaliere o un piano settimanale.

## Moduli principali

- `predict_models.py`: script principale che integra inferenza Prolog, modelli ML e piano alimentare.
- `nutrition_planner.py`: modulo dedicato al calcolo nutrizionale e alla generazione dei pasti.
- `kb/kb.pl`: base di conoscenza Prolog per workout consigliato, intensita' e durata ottimale.
- `apprendimento_supervisionato/training.py`: addestramento dei modelli supervisionati.
- `apprendimento_probabilistico/training.py`: addestramento del modello Bayesian Ridge.
- `dataset/dataset_utils.py`: funzioni di caricamento e preparazione del dataset di allenamento.

## Dataset

Il progetto utilizza due dataset principali:

- `dataset/gym_members_exercise_tracking.csv`: dataset usato per addestrare i modelli predittivi delle calorie bruciate.
- `dataset/alimenti.csv`: dataset alimentare usato per costruire piano giornaliero, alternative e piano settimanale.

Il file `dataset/alimenti.csv` contiene alimenti classificati per categoria e pasto:

```csv
alimento,categoria,pasti,kcal_100g,proteine_100g,carboidrati_100g,grassi_100g
```

## Esecuzione

Per eseguire il programma completo:

```bash
python3 predict_models.py
```

Il programma richiede:

- sesso;
- eta';
- peso;
- altezza;
- tipo di allenamento;
- durata della sessione;
- ore di allenamento settimanali;
- battiti medi;
- percentuale di massa grassa;
- massa magra;
- numero di giorni del piano alimentare;
- numero di alternative giornaliere, se si sceglie un piano di un solo giorno.

Se la massa magra non e' nota, e' possibile inserire `0`: il programma la stima usando peso e percentuale di massa grassa.
Gli input numerici sono controllati con limiti minimi e massimi, e i valori decimali possono essere inseriti anche con la virgola.

## Output

L'esecuzione produce tre blocchi principali:

- risultati dell'inferenza Prolog;
- predizione delle calorie bruciate tramite modelli ML;
- piano alimentare consigliato con calorie, macronutrienti e alimenti per colazione, pranzo, spuntino e cena.

Il piano puo' essere generato in tre modalita':

- singolo giorno;
- piu' alternative per lo stesso giorno;
- piano settimanale fino a 7 giorni.

## Grafici e modelli

I grafici presenti nelle cartelle `apprendimento_supervisionato/grafici/` e `apprendimento_probabilistico/grafici/` non vengono aggiornati da `predict_models.py`.

Per aggiornare grafici, modelli `.pkl` e tabelle degli iperparametri bisogna rilanciare gli script di training:

```bash
python3 apprendimento_supervisionato/training.py
python3 apprendimento_probabilistico/training.py
```

## Documentazione HTML

La documentazione Sphinx usa dipendenze separate per evitare problemi con le librerie del modello su Python 3.9:

```bash
python3 -m pip install -r requirements-docs.txt
python3 -m sphinx -b html docs docs/_build/html
```

Il file iniziale da aprire nel browser e':

```text
docs/_build/html/index.html
```
