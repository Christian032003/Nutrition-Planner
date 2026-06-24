import os

import joblib
import pandas as pd

from nutrition_planner import (
    ask_float,
    ask_int,
    build_nutrition_plan,
    print_meal_plan,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def model_path(*parts):
    """
    Costruisce percorsi assoluti a partire dalla cartella principale del progetto.
    """
    return os.path.join(BASE_DIR, *parts)


def load_models():
    """
    Carica i modelli di machine learning e lo scaler da file salvati.

    Returns:
        dict: un dizionario contenente i modelli caricati.
        scaler: lo scaler per la normalizzazione dei dati.
        workout_mapping: una mappatura dei tipi di allenamento.
    """
    supervised_learn_path = model_path("apprendimento_supervisionato", "modelli")
    probabilistic_learn_path = model_path("apprendimento_probabilistico", "modelli")
    gradient_boosting_path = os.path.join(supervised_learn_path, "modello_Gradient Boosting.pkl")

    # Mantiene compatibilita' con salvataggi precedenti del modello.
    if not os.path.exists(gradient_boosting_path):
        gradient_boosting_path = os.path.join(supervised_learn_path, "modello_Gradient boosting.pkl")

    models = {
        "linear": joblib.load(os.path.join(supervised_learn_path, "modello_Linear Regression.pkl")),
        "random_forest": joblib.load(os.path.join(supervised_learn_path, "modello_Random Forest.pkl")),
        "gradient_boosting": joblib.load(gradient_boosting_path),
        "bayesian_ridge": joblib.load(os.path.join(probabilistic_learn_path, "modello_bayesian_ridge.pkl")),
    }
    scaler = joblib.load(os.path.join(supervised_learn_path, "scaler.pkl"))
    workout_mapping = joblib.load(os.path.join(supervised_learn_path, "workout_mapping.pkl"))

    return models, scaler, workout_mapping


def query_prolog(weight, height, duration):
    """
    Interroga la base di conoscenza Prolog per inferire il tipo di allenamento,
    l'intensita' e la durata ottimale in base ai parametri di input.

    Parameters:
        weight (float): il peso dell'utente in kg.
        height (float): l'altezza dell'utente in metri.
        duration (float): la durata della sessione di allenamento in ore.

    Returns:
        tuple: workout consigliato, intensita' e durata ottimale.
    """
    from pyswip import Prolog

    current_dir = os.getcwd()
    kb_dir = model_path("kb")
    kb_file = model_path("kb", "kb.pl")

    try:
        # pyswip consulta la knowledge base in modo piu' stabile dalla cartella kb.
        os.chdir(kb_dir)
        prolog = Prolog()
        prolog.consult(kb_file)

        workout_result = list(prolog.query(f"recommended_workout({weight}, {height}, Workout)"))
        workout_type = workout_result[0]["Workout"] if workout_result else None

        intensity_result = list(
            prolog.query(f"recommended_intensity({weight}, {height}, Intensity, {duration})")
        )
        intensity = intensity_result[0]["Intensity"] if intensity_result else None

        duration_result = list(
            prolog.query(f"optimal_duration({weight}, {height}, {duration}, OptimalDuration)")
        )
        optimal_duration = duration_result[0]["OptimalDuration"] if duration_result else None
    finally:
        os.chdir(current_dir)

    return workout_type, intensity, optimal_duration


def print_prolog_results(workout_mapping, workout_type, intensity, optimal_duration):
    """
    Stampa i risultati dell'inferenza fatta dalla base di conoscenza Prolog.
    """
    print("\n=== Risultati dell'Inferenza Prolog ===")
    print(f"Workout consigliato: {workout_mapping.get(workout_type, 'Sconosciuto')}")
    print(f"Intensita' stimata: {intensity}")
    print(f"Durata ottimale: {optimal_duration} ore")


def get_user_input(workout_mapping):
    """
    Richiede all'utente i dati necessari per predizioni e piano alimentare.

    Returns:
        tuple: dati anagrafici, dati allenamento e composizione corporea.
    """
    gender = ask_int("Inserisci il genere (0 = Maschio, 1 = Femmina): ", allowed_values={0, 1})
    age = ask_int("Inserisci l'eta': ", 10, 100)
    weight = ask_float("Inserisci il peso in kg: ", 30, 250)
    height = ask_float("Inserisci l'altezza in metri: ", 1.20, 2.30)

    print("\nSeleziona il tipo di allenamento tra i seguenti:")
    for code, workout in workout_mapping.items():
        print(f"{code}: {workout}")
    workout_type = ask_int(
        "Inserisci il codice del tipo di allenamento: ",
        allowed_values=set(workout_mapping.keys()),
    )

    session_duration = ask_float("Inserisci la durata della sessione in ore: ", 0.1, 8)
    weekly_training_hours = ask_float("Inserisci le ore di allenamento settimanali: ", 0, 30, allow_zero=True)
    avg_bpm = ask_float("Inserisci la media dei battiti per minuto a fine allenamento: ", 40, 220)
    body_fat_pct = ask_float("Inserisci la percentuale di massa grassa: ", 1, 70)
    lean_mass = ask_float("Inserisci la massa magra in kg (0 se non la conosci): ", 0, weight, allow_zero=True)
    plan_days = ask_int("Quanti giorni vuoi pianificare (1-7): ", 1, 7)
    daily_alternatives = 1

    if plan_days == 1:
        daily_alternatives = ask_int("Quante alternative giornaliere vuoi generare (1-3): ", 1, 3)

    return (
        gender,
        age,
        weight,
        height,
        avg_bpm,
        workout_type,
        session_duration,
        weekly_training_hours,
        body_fat_pct,
        lean_mass,
        plan_days,
        daily_alternatives,
    )


def scale_data(data, scaler):
    """
    Scala i dati forniti utilizzando lo scaler fornito.
    """
    scaled_values = scaler.transform(data)
    return pd.DataFrame(scaled_values, columns=data.columns)


def make_predictions(models, scaled_data):
    """
    Effettua le predizioni sui dati scalati utilizzando i vari modelli.
    """
    predictions = {
        "Regressione Lineare": models["linear"].predict(scaled_data)[0],
        "Random Forest": models["random_forest"].predict(scaled_data)[0],
        "Gradient Boosting": models["gradient_boosting"].predict(scaled_data)[0],
        "Bayesian Ridge": models["bayesian_ridge"].predict(scaled_data.to_numpy())[0],
    }

    # Bayesian Ridge restituisce anche l'incertezza, usata per l'intervallo al 95%.
    mean_bayesian, std_bayesian = models["bayesian_ridge"].predict(
        scaled_data.to_numpy(),
        return_std=True,
    )
    variance_bayesian = std_bayesian[0]
    conf_interval = 1.96 * variance_bayesian
    predictions["Intervallo di Confidenza Bayesian Ridge"] = (
        mean_bayesian[0] - conf_interval,
        mean_bayesian[0] + conf_interval,
    )

    return predictions


def print_predictions(predictions):
    """
    Stampa i risultati delle predizioni effettuate.
    """
    print("\n=== Risultati delle Predizioni ===")
    for model, value in predictions.items():
        if isinstance(value, tuple):
            print(f"{model}: [{value[0]:.2f}, {value[1]:.2f}] kcal")
        else:
            print(f"{model}: {value:.2f} kcal")


def main():
    """
    Funzione principale che gestisce il flusso dell'applicazione.

    1. Carica modelli ML, scaler e mappatura workout.
    2. Raccoglie dati utente, allenamento e composizione corporea.
    3. Usa Prolog per workout, intensita' e durata ottimale.
    4. Predice le calorie bruciate.
    5. Genera il piano alimentare dal dataset alimenti.
    """
    models, scaler, workout_mapping = load_models()
    (
        gender,
        age,
        weight,
        height,
        avg_bpm,
        workout_type,
        session_duration,
        weekly_training_hours,
        body_fat_pct,
        lean_mass_input,
        plan_days,
        daily_alternatives,
    ) = get_user_input(workout_mapping)

    recommended_workout_type, intensity, optimal_duration = query_prolog(weight, height, session_duration)
    print_prolog_results(workout_mapping, recommended_workout_type, intensity, optimal_duration)

    # Se Prolog non produce una raccomandazione, resta valido il workout inserito dall'utente.
    model_workout_type = recommended_workout_type if recommended_workout_type is not None else workout_type
    user_data = pd.DataFrame(
        [[gender, model_workout_type, session_duration, weight, age, avg_bpm]],
        columns=[
            "Gender",
            "Workout_Type",
            "Session_Duration_(hours)",
            "Weight_(kg)",
            "Age",
            "Avg_BPM",
        ],
    )

    scaled_data = scale_data(user_data, scaler)
    predictions = make_predictions(models, scaled_data)
    print_predictions(predictions)

    nutrition_data = build_nutrition_plan(
        gender,
        age,
        weight,
        height,
        weekly_training_hours,
        body_fat_pct,
        lean_mass_input,
        plan_days,
        daily_alternatives,
    )
    print_meal_plan(*nutrition_data)

    input("\nPremi invio per uscire...")


if __name__ == "__main__":
    main()
