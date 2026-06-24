import os
import pandas as pd


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOOD_DATASET_PATH = os.path.join(BASE_DIR, "dataset", "alimenti.csv")
DAYS_OF_WEEK = ["Lunedi", "Martedi", "Mercoledi", "Giovedi", "Venerdi", "Sabato", "Domenica"]
# Percentuale indicativa delle calorie giornaliere assegnata a ogni pasto.
MEAL_DISTRIBUTION = {
    "colazione": 0.25,
    "pranzo": 0.35,
    "spuntino": 0.10,
    "cena": 0.30,
}


def parse_float(value):
    """
    Converte una stringa in float accettando sia il punto sia la virgola.
    """
    return float(value.replace(",", "."))


def ask_int(prompt, min_value=None, max_value=None, allowed_values=None):
    """
    Richiede un intero e ripete la domanda finche' l'input non e' valido.
    """
    while True:
        try:
            value = int(input(prompt))
            if allowed_values is not None and value not in allowed_values:
                print(f"Valore non valido. Valori ammessi: {sorted(allowed_values)}")
                continue
            if min_value is not None and value < min_value:
                print(f"Valore non valido. Inserisci un numero >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Valore non valido. Inserisci un numero <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Input non valido. Inserisci un numero intero.")


def ask_float(prompt, min_value=None, max_value=None, allow_zero=False):
    """
    Richiede un numero decimale e ripete la domanda finche' l'input non e' valido.
    """
    while True:
        try:
            value = parse_float(input(prompt))
            if value == 0 and allow_zero:
                return value
            if min_value is not None and value < min_value:
                print(f"Valore non valido. Inserisci un numero >= {min_value}.")
                continue
            if max_value is not None and value > max_value:
                print(f"Valore non valido. Inserisci un numero <= {max_value}.")
                continue
            return value
        except ValueError:
            print("Input non valido. Inserisci un numero, ad esempio 70 oppure 1,75.")


def ask_yes_no(prompt):
    """
    Richiede una risposta si/no.
    """
    while True:
        value = input(prompt).strip().lower()
        if value in {"s", "si", "y", "yes"}:
            return True
        if value in {"n", "no"}:
            return False
        print("Risposta non valida. Inserisci s oppure n.")


def load_food_dataset(file_path=FOOD_DATASET_PATH):
    """
    Carica il dataset degli alimenti.

    Returns:
        DataFrame: tabella con alimenti, categoria, pasti e valori nutrizionali.
    """
    foods = pd.read_csv(file_path)
    required_columns = {
        "alimento",
        "categoria",
        "pasti",
        "kcal_100g",
        "proteine_100g",
        "carboidrati_100g",
        "grassi_100g",
    }
    missing_columns = required_columns - set(foods.columns)

    if missing_columns:
        raise ValueError(f"Colonne mancanti nel dataset alimenti: {missing_columns}")

    foods = foods.copy()
    # Normalizza i campi testuali per rendere affidabili filtri e confronti.
    foods["categoria"] = foods["categoria"].str.strip().str.lower()
    foods["pasti"] = foods["pasti"].str.strip().str.lower()
    return foods


def get_user_input():
    """
    Richiede all'utente i dati necessari per generare il piano alimentare.

    Returns:
        tuple: sesso, eta, peso, altezza, ore_allenamento, massa_grassa_pct,
        massa_magra, giorni_piano, alternative_giornaliere.
    """
    sesso = ask_int("Inserisci il sesso (0 = Maschio, 1 = Femmina): ", allowed_values={0, 1})
    eta = ask_int("Inserisci l'eta': ", 10, 100)
    peso = ask_float("Inserisci il peso in kg: ", 30, 250)
    altezza = ask_float("Inserisci l'altezza in metri: ", 1.20, 2.30)
    ore_allenamento = ask_float("Inserisci le ore di allenamento settimanali: ", 0, 30, allow_zero=True)
    massa_grassa_pct = ask_float("Inserisci la percentuale di massa grassa: ", 1, 70)
    massa_magra = ask_float("Inserisci la massa magra in kg (0 se non la conosci): ", 0, peso, allow_zero=True)
    giorni_piano = ask_int("Quanti giorni vuoi pianificare (1-7): ", 1, 7)
    alternative_giornaliere = 1

    if giorni_piano == 1:
        alternative_giornaliere = ask_int("Quante alternative giornaliere vuoi generare (1-3): ", 1, 3)

    return (
        sesso,
        eta,
        peso,
        altezza,
        ore_allenamento,
        massa_grassa_pct,
        massa_magra,
        giorni_piano,
        alternative_giornaliere,
    )


def calculate_lean_mass(peso, massa_grassa_pct, massa_magra):
    """
    Restituisce la massa magra. Se non viene inserita, la stima dal peso.
    """
    if massa_magra > 0:
        return massa_magra

    # Se l'utente non conosce la massa magra, viene stimata dalla massa grassa.
    return peso * (1 - massa_grassa_pct / 100)


def calculate_bmr(sesso, eta, peso, altezza, massa_magra):
    """
    Calcola il metabolismo basale.

    Usa Katch-McArdle quando e' disponibile la massa magra,
    altrimenti usa Mifflin-St Jeor.
    """
    if massa_magra > 0:
        return 370 + (21.6 * massa_magra)

    altezza_cm = altezza * 100
    if sesso == 0:
        return (10 * peso) + (6.25 * altezza_cm) - (5 * eta) + 5

    return (10 * peso) + (6.25 * altezza_cm) - (5 * eta) - 161


def calculate_activity_factor(ore_allenamento):
    """
    Determina il fattore di attivita' in base alle ore di allenamento settimanali.
    """
    if ore_allenamento <= 1:
        return 1.2
    if ore_allenamento <= 3:
        return 1.375
    if ore_allenamento <= 5:
        return 1.55
    if ore_allenamento <= 7:
        return 1.725
    return 1.9


def calculate_tdee(bmr, ore_allenamento):
    """
    Calcola il fabbisogno calorico giornaliero totale.
    """
    return bmr * calculate_activity_factor(ore_allenamento)


def infer_goal(sesso, massa_grassa_pct):
    """
    Deduce l'obiettivo alimentare dalla percentuale di massa grassa.
    """
    if sesso == 0:
        if massa_grassa_pct > 20:
            return "dimagrimento"
        if massa_grassa_pct < 12:
            return "aumento massa"
        return "mantenimento"

    if massa_grassa_pct > 30:
        return "dimagrimento"
    if massa_grassa_pct < 20:
        return "aumento massa"
    return "mantenimento"


def calculate_target_calories(tdee, goal):
    """
    Adatta le calorie giornaliere in base all'obiettivo.
    """
    if goal == "dimagrimento":
        return tdee * 0.85
    if goal == "aumento massa":
        return tdee * 1.10
    return tdee


def calculate_macros(peso, massa_magra, target_calories, goal):
    """
    Calcola i macronutrienti giornalieri.
    """
    if goal == "dimagrimento":
        proteine_g = massa_magra * 2.2
        grassi_g = peso * 0.8
    elif goal == "aumento massa":
        proteine_g = massa_magra * 2.0
        grassi_g = peso * 1.0
    else:
        proteine_g = massa_magra * 1.8
        grassi_g = peso * 0.9

    calorie_proteine = proteine_g * 4
    calorie_grassi = grassi_g * 9
    # I carboidrati coprono le calorie rimanenti dopo proteine e grassi.
    carboidrati_g = max((target_calories - calorie_proteine - calorie_grassi) / 4, 0)

    return {
        "proteine_g": proteine_g,
        "carboidrati_g": carboidrati_g,
        "grassi_g": grassi_g,
    }


def filter_foods(foods, meal_name, category):
    """
    Filtra gli alimenti compatibili con uno specifico pasto e categoria.
    """
    meal_name = meal_name.lower()
    return foods[
        foods["pasti"].str.contains(meal_name, case=False)
        & (foods["categoria"] == category)
    ]


def select_food(foods, meal_name, category, macro_column, variant_index=0):
    """
    Seleziona un alimento variando la scelta in base all'indice della variante.
    """
    available_foods = filter_foods(foods, meal_name, category)

    if available_foods.empty and category == "proteina":
        available_foods = filter_foods(foods, meal_name, "misto")

    if available_foods.empty:
        return None

    available_foods = available_foods.copy()
    # Per le proteine privilegia alimenti con piu' proteine per kcal.
    if category == "proteina":
        available_foods["macro_score"] = available_foods["proteine_100g"] / available_foods["kcal_100g"]
        available_foods = available_foods.sort_values("macro_score", ascending=False)
    else:
        available_foods = available_foods.sort_values(macro_column, ascending=False)

    index = variant_index % len(available_foods)
    return available_foods.iloc[index]


def select_dense_food(foods, meal_name, category, exclude_alimento=None):
    """
    Seleziona un alimento piu' denso per completare un pasto se resta budget calorico.
    """
    available_foods = filter_foods(foods, meal_name, category).copy()

    if exclude_alimento is not None:
        available_foods = available_foods[available_foods["alimento"] != exclude_alimento]

    if available_foods.empty:
        return None

    return available_foods.sort_values("kcal_100g", ascending=False).iloc[0]


def calculate_food_grams_by_calories(food, target_calories, min_g=20, max_g=250):
    """
    Calcola i grammi di un alimento in base a un budget calorico.
    """
    kcal_per_gram = food["kcal_100g"] / 100

    if kcal_per_gram <= 0:
        return 0

    grams = target_calories / kcal_per_gram
    return round(min(max(grams, min_g), max_g))


def calculate_food_values(food, grams):
    """
    Calcola calorie e macronutrienti di un alimento in base ai grammi.
    """
    factor = grams / 100
    return {
        "alimento": food["alimento"],
        "grammi": grams,
        "kcal": food["kcal_100g"] * factor,
        "proteine_g": food["proteine_100g"] * factor,
        "carboidrati_g": food["carboidrati_100g"] * factor,
        "grassi_g": food["grassi_100g"] * factor,
    }


def add_food_to_meal(daily_plan, meal_name, food_values):
    """
    Aggiunge un alimento a un pasto e aggiorna i totali del pasto.
    """
    daily_plan[meal_name]["alimenti"].append(food_values)
    for key in ["kcal", "proteine_g", "carboidrati_g", "grassi_g"]:
        daily_plan[meal_name]["totali"][key] += food_values[key]


def balance_daily_plan(foods, daily_plan, target_calories):
    """
    Avvicina il totale giornaliero al target calorico con piccole aggiunte finali.
    """
    totals = calculate_plan_totals(daily_plan)
    deficit = target_calories - totals["kcal"]

    if deficit <= target_calories * 0.08:
        return daily_plan

    extra_carb_food = select_dense_food(foods, "cena", "carboidrato")
    if extra_carb_food is not None:
        grams = calculate_food_grams_by_calories(extra_carb_food, deficit * 0.75, 20, 180)
        add_food_to_meal(daily_plan, "cena", calculate_food_values(extra_carb_food, grams))

    totals = calculate_plan_totals(daily_plan)
    deficit = target_calories - totals["kcal"]

    if deficit > 80:
        extra_fat_food = select_dense_food(foods, "cena", "grasso")
        if extra_fat_food is not None:
            grams = calculate_food_grams_by_calories(extra_fat_food, deficit, 5, 20)
            add_food_to_meal(daily_plan, "cena", calculate_food_values(extra_fat_food, grams))

    return daily_plan


def generate_meal_plan(foods, target_calories, macros, variant_index=0):
    """
    Genera un piano alimentare giornaliero usando il dataset alimenti.
    """
    meal_plan = {}

    for meal_offset, (meal_name, percentage) in enumerate(MEAL_DISTRIBUTION.items()):
        local_variant = variant_index + meal_offset
        meal_targets = {
            "kcal": target_calories * percentage,
            "proteine_g": macros["proteine_g"] * percentage,
            "carboidrati_g": macros["carboidrati_g"] * percentage,
            "grassi_g": macros["grassi_g"] * percentage,
        }
        meal_foods = []

        protein_food = select_food(foods, meal_name, "proteina", "proteine_100g", local_variant)
        carb_food = select_food(foods, meal_name, "carboidrato", "carboidrati_100g", local_variant)
        fat_food = select_food(foods, meal_name, "grasso", "grassi_100g", local_variant)
        vegetable_food = select_food(foods, meal_name, "verdura", "carboidrati_100g", local_variant)

        protein_calories = meal_targets["proteine_g"] * 4
        carb_calories = meal_targets["carboidrati_g"] * 4
        fat_calories = meal_targets["grassi_g"] * 9

        if vegetable_food is not None and meal_name in {"pranzo", "cena"}:
            vegetable_values = calculate_food_values(vegetable_food, 200)
            meal_foods.append(vegetable_values)
            carb_calories = max(carb_calories - vegetable_values["kcal"], 0)

        if protein_food is not None:
            grams = calculate_food_grams_by_calories(protein_food, protein_calories)
            meal_foods.append(calculate_food_values(protein_food, grams))

        if carb_food is not None:
            max_carb_grams = 400 if meal_name in {"pranzo", "cena"} else 300
            grams = calculate_food_grams_by_calories(carb_food, carb_calories, 20, max_carb_grams)
            carb_values = calculate_food_values(carb_food, grams)
            meal_foods.append(carb_values)

            remaining_carb_calories = carb_calories - carb_values["kcal"]
            if remaining_carb_calories > carb_calories * 0.25:
                extra_carb_food = select_dense_food(
                    foods,
                    meal_name,
                    "carboidrato",
                    exclude_alimento=carb_food["alimento"],
                )
                if extra_carb_food is not None:
                    extra_max_grams = 250 if meal_name in {"pranzo", "cena"} else 150
                    grams = calculate_food_grams_by_calories(
                        extra_carb_food,
                        remaining_carb_calories,
                        20,
                        extra_max_grams,
                    )
                    meal_foods.append(calculate_food_values(extra_carb_food, grams))

        if fat_food is not None:
            grams = calculate_food_grams_by_calories(fat_food, fat_calories, 5, 35)
            meal_foods.append(calculate_food_values(fat_food, grams))

        meal_totals = {
            "kcal": sum(item["kcal"] for item in meal_foods),
            "proteine_g": sum(item["proteine_g"] for item in meal_foods),
            "carboidrati_g": sum(item["carboidrati_g"] for item in meal_foods),
            "grassi_g": sum(item["grassi_g"] for item in meal_foods),
        }

        meal_plan[meal_name] = {
            "target": meal_targets,
            "totali": meal_totals,
            "alimenti": meal_foods,
        }

    # Ultimo aggiustamento: se il piano e' troppo sotto target, aggiunge piccole quote.
    return balance_daily_plan(foods, meal_plan, target_calories)


def generate_daily_alternatives(foods, target_calories, macros, alternatives_count=1):
    """
    Genera piu' alternative giornaliere.
    """
    return [
        generate_meal_plan(foods, target_calories, macros, variant_index=index)
        for index in range(alternatives_count)
    ]


def generate_weekly_meal_plan(foods, target_calories, macros, days=7):
    """
    Genera un piano alimentare settimanale o comunque multi-giorno.
    """
    return {
        DAYS_OF_WEEK[index]: generate_meal_plan(foods, target_calories, macros, variant_index=index)
        for index in range(days)
    }


def calculate_plan_totals(daily_plan):
    """
    Calcola i totali di un piano giornaliero.
    """
    return {
        "kcal": sum(meal["totali"]["kcal"] for meal in daily_plan.values()),
        "proteine_g": sum(meal["totali"]["proteine_g"] for meal in daily_plan.values()),
        "carboidrati_g": sum(meal["totali"]["carboidrati_g"] for meal in daily_plan.values()),
        "grassi_g": sum(meal["totali"]["grassi_g"] for meal in daily_plan.values()),
    }


def print_daily_plan(daily_plan):
    """
    Stampa un piano alimentare giornaliero.
    """
    for meal_name, meal_data in daily_plan.items():
        totals = meal_data["totali"]
        print(f"\n{meal_name.capitalize()}")
        print(
            f"Totale stimato: {totals['kcal']:.2f} kcal | "
            f"P {totals['proteine_g']:.2f} g | "
            f"C {totals['carboidrati_g']:.2f} g | "
            f"G {totals['grassi_g']:.2f} g"
        )

        for food in meal_data["alimenti"]:
            print(f"- {food['alimento']}: {food['grammi']} g")


def print_meal_plan(goal, bmr, tdee, target_calories, macros, meal_plan, plan_days=1, alternatives_count=1):
    """
    Stampa il piano alimentare finale.
    """
    print("\n=== Piano Alimentare Consigliato ===")
    print(f"Obiettivo stimato: {goal}")
    print(f"Metabolismo basale: {bmr:.2f} kcal")
    print(f"Fabbisogno calorico totale: {tdee:.2f} kcal")
    print(f"Calorie giornaliere consigliate: {target_calories:.2f} kcal")

    print("\n=== Macronutrienti Giornalieri ===")
    print(f"Proteine: {macros['proteine_g']:.2f} g")
    print(f"Carboidrati: {macros['carboidrati_g']:.2f} g")
    print(f"Grassi: {macros['grassi_g']:.2f} g")

    if plan_days > 1:
        print(f"\n=== Piano Alimentare per {plan_days} Giorni ===")
        for day_name, daily_plan in meal_plan.items():
            totals = calculate_plan_totals(daily_plan)
            print(
                f"\n--- {day_name} | {totals['kcal']:.2f} kcal | "
                f"P {totals['proteine_g']:.2f} g | "
                f"C {totals['carboidrati_g']:.2f} g | "
                f"G {totals['grassi_g']:.2f} g ---"
            )
            print_daily_plan(daily_plan)
        return

    if alternatives_count > 1:
        print(f"\n=== Alternative Giornaliere ({alternatives_count}) ===")
        for index, daily_plan in enumerate(meal_plan, start=1):
            totals = calculate_plan_totals(daily_plan)
            print(
                f"\n--- Alternativa {index} | {totals['kcal']:.2f} kcal | "
                f"P {totals['proteine_g']:.2f} g | "
                f"C {totals['carboidrati_g']:.2f} g | "
                f"G {totals['grassi_g']:.2f} g ---"
            )
            print_daily_plan(daily_plan)
        return

    print("\n=== Piano per Pasti ===")
    print_daily_plan(meal_plan)


def build_nutrition_plan(sesso, eta, peso, altezza, ore_allenamento, massa_grassa_pct, massa_magra_input, giorni_piano=1, alternative_giornaliere=1):
    """
    Costruisce i dati nutrizionali e il piano alimentare.
    """
    foods = load_food_dataset()
    massa_magra = calculate_lean_mass(peso, massa_grassa_pct, massa_magra_input)
    bmr = calculate_bmr(sesso, eta, peso, altezza, massa_magra)
    tdee = calculate_tdee(bmr, ore_allenamento)
    goal = infer_goal(sesso, massa_grassa_pct)
    target_calories = calculate_target_calories(tdee, goal)
    macros = calculate_macros(peso, massa_magra, target_calories, goal)

    # La stessa pipeline genera un giorno singolo, alternative o piu' giorni.
    if giorni_piano > 1:
        meal_plan = generate_weekly_meal_plan(foods, target_calories, macros, giorni_piano)
    elif alternative_giornaliere > 1:
        meal_plan = generate_daily_alternatives(foods, target_calories, macros, alternative_giornaliere)
    else:
        meal_plan = generate_meal_plan(foods, target_calories, macros)

    return goal, bmr, tdee, target_calories, macros, meal_plan, giorni_piano, alternative_giornaliere


def main():
    """
    Flusso principale:
    1. Raccoglie i dati dell'utente.
    2. Calcola metabolismo, fabbisogno e obiettivo.
    3. Calcola i macronutrienti.
    4. Genera e stampa piano giornaliero, alternative o piano settimanale.
    """
    (
        sesso,
        eta,
        peso,
        altezza,
        ore_allenamento,
        massa_grassa_pct,
        massa_magra_input,
        giorni_piano,
        alternative_giornaliere,
    ) = get_user_input()

    nutrition_data = build_nutrition_plan(
        sesso,
        eta,
        peso,
        altezza,
        ore_allenamento,
        massa_grassa_pct,
        massa_magra_input,
        giorni_piano,
        alternative_giornaliere,
    )
    print_meal_plan(*nutrition_data)
    input("\nPremi invio per uscire...")


if __name__ == "__main__":
    main()
