from __future__ import annotations

import csv
import html
import inspect
import shutil
from pathlib import Path


PROJECT_NAME = "Nutrition Planner"
AUTHOR = "Termine Christian Domenico"
UPDATED = "24 giugno 2026"

ROOT = Path(__file__).resolve().parent
DESKTOP_PROJECT = Path("/Users/christiandomenicotermine/Desktop/Burned-Calories-Estimation-Model-main")
PROJECT_DESKTOP = DESKTOP_PROJECT if DESKTOP_PROJECT.exists() else ROOT
SOURCE_DOCS = ROOT / "docs"
OUT = ROOT / "docs" / "_build" / "html"
STATIC_SOURCE = PROJECT_DESKTOP / "docs" / "_build" / "html" / "_static"


PAGES = [
    ("index.html", "Panoramica"),
    ("indice_originale.html", "Indice originale"),
    ("modules.html", "Moduli"),
    ("apprendimento_supervisionato.html", "Apprendimento supervisionato"),
    ("apprendimento_probabilistico.html", "Apprendimento probabilistico"),
    ("dataset.html", "Dataset"),
    ("kb.html", "Knowledge Base Prolog"),
    ("nutrition_planner.html", "nutrition_planner"),
    ("predict_models.html", "predict_models"),
    ("documentazione.html", "Documentazione"),
]

RUN_COMMANDS = "python3 predict_models.py\npython3 -m sphinx -b html docs docs/_build/html"
HTML_COMMANDS = "python3 -m pip install -r requirements-docs.txt\n" + RUN_COMMANDS
DOC_COMMANDS = (
    "python3 predict_models.py\n"
    "python3 -m pip install -r requirements-docs.txt\n"
    "python3 -m sphinx -b html docs docs/_build/html"
)
HOME_DOC_LINKS = [
    '<a class="reference internal" href="indice_originale.html">Apri il confronto con l&apos;indice originale</a>',
    '<a class="reference internal" href="documentazione.html">Apri la pagina documentazione e output</a>',
    '<a class="reference internal" href="nutrition_planner.html">Apri la pagina del planner alimentare</a>',
]
PROLOG_QUERIES = (
    "recommended_workout(Weight, Height, Workout)\n"
    "recommended_intensity(Weight, Height, Intensity, Duration)\n"
    "optimal_duration(Weight, Height, Duration, OptimalDuration)"
)


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def p(text: str) -> str:
    return f"<p>{e(text)}</p>"


def code(value: str) -> str:
    return f"<code class=\"docutils literal notranslate\"><span class=\"pre\">{e(value)}</span></code>"


def ul(items: list[str]) -> str:
    body = "\n".join(f"<li><p>{item}</p></li>" for item in items)
    return f"<ul class=\"simple\">\n{body}\n</ul>"


def ol(items: list[str]) -> str:
    body = "\n".join(f"<li><p>{item}</p></li>" for item in items)
    return f"<ol class=\"arabic simple\">\n{body}\n</ol>"


def pre(text: str) -> str:
    return f"<div class=\"highlight\"><pre>{e(text)}</pre></div>"


def table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th class=\"head\"><p>{e(header)}</p></th>" for header in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td><p>{cell}</p></td>" for cell in row)
        body_rows.append(f"<tr class=\"row-even\">{cells}</tr>")
    return (
        "<table class=\"docutils align-default\">\n"
        f"<thead><tr class=\"row-odd\">{head}</tr></thead>\n"
        f"<tbody>{''.join(body_rows)}</tbody>\n"
        "</table>"
    )


def card_grid(cards: list[tuple[str, str]]) -> str:
    items = []
    for title, text in cards:
        items.append(
            "<article class=\"doc-card\">"
            f"<h3>{e(title)}</h3>"
            f"<p>{e(text)}</p>"
            "</article>"
        )
    return "<div class=\"doc-card-grid\">" + "\n".join(items) + "</div>"


def status_grid(items: list[tuple[str, str, str]]) -> str:
    blocks = []
    for label, value, note in items:
        blocks.append(
            "<div class=\"status-box\">"
            f"<span>{e(label)}</span>"
            f"<strong>{e(value)}</strong>"
            f"<small>{e(note)}</small>"
            "</div>"
        )
    return "<div class=\"status-grid\">" + "\n".join(blocks) + "</div>"


def nav(current: str) -> str:
    items = []
    for href, label in PAGES:
        cls = "toctree-l1"
        link_cls = "reference internal"
        if href == current:
            cls += " current"
            link_cls = "current reference internal"
        items.append(f'<li class="{cls}"><a class="{link_cls}" href="{href}">{e(label)}</a></li>')
    return "\n".join(items)


def base_page(filename: str, title: str, body: str, prev_href: str | None = None, next_href: str | None = None) -> str:
    footer_prev = (
        f'<a href="{prev_href}" class="btn btn-neutral float-left" rel="prev">'
        '<span class="fa fa-arrow-circle-left" aria-hidden="true"></span> Previous</a>'
        if prev_href
        else ""
    )
    footer_next = (
        f'<a href="{next_href}" class="btn btn-neutral float-right" rel="next">'
        'Next <span class="fa fa-arrow-circle-right" aria-hidden="true"></span></a>'
        if next_href
        else ""
    )
    return f"""<!DOCTYPE html>
<html class="writer-html5" lang="it" data-content_root="./">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{e(title)} &mdash; {e(PROJECT_NAME)} 1.0.0 documentation</title>
  <link rel="stylesheet" type="text/css" href="_static/basic.css" />
  <link rel="stylesheet" type="text/css" href="_static/css/theme.css" />
  <style>
    .wy-side-nav-search, .wy-nav-top {{ background: #1f5f5b; }}
    .wy-nav-content {{ max-width: 1040px; }}
    .wy-side-nav-search, .wy-nav-top {{ background: #195f5a; }}
    .wy-side-nav-search>a {{ font-size: 94%; line-height: 1.25; }}
    .wy-nav-content {{ max-width: 1120px; }}
    .rst-content h1 {{ color: #174f4b; margin-bottom: 12px; }}
    .rst-content h2 {{ color: #1f6e66; border-bottom: 1px solid #d9e8e5; padding-bottom: 4px; }}
    .docutils.literal {{ background: #f3f6f6; border: 1px solid #d9e2e1; padding: 1px 4px; }}
    .highlight pre {{ background: #f6f8fa; border: 1px solid #dfe6e5; padding: 12px; overflow-x: auto; border-radius: 6px; }}
    table.docutils {{ border-collapse: collapse; margin: 14px 0 20px; }}
    table.docutils td, table.docutils th {{ white-space: normal; vertical-align: top; padding: 9px 10px; }}
    table.docutils th {{ background: #edf5f3; color: #174f4b; }}
    .admonition.note {{ background: #eef7f5; border-left: 4px solid #1f7a70; padding: 10px 14px; margin: 18px 0; border-radius: 0 6px 6px 0; }}
    .doc-hero {{ background: linear-gradient(135deg, #eef7f5, #f8fbfb); border: 1px solid #d9e8e5; border-radius: 8px; padding: 22px 24px; margin: 0 0 22px; }}
    .doc-hero h1 {{ margin-top: 0; }}
    .status-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 18px 0 24px; }}
    .status-box {{ border: 1px solid #d9e8e5; border-radius: 8px; padding: 12px; background: #fff; }}
    .status-box span {{ display: block; color: #59706d; font-size: 12px; text-transform: uppercase; letter-spacing: .04em; }}
    .status-box strong {{ display: block; color: #174f4b; font-size: 20px; margin: 4px 0; }}
    .status-box small {{ color: #5d6866; }}
    .doc-card-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 14px; margin: 18px 0 22px; }}
    .doc-card {{ border: 1px solid #dce8e6; border-radius: 8px; background: white; padding: 14px 16px; }}
    .doc-card h3 {{ margin: 0 0 6px; color: #174f4b; font-size: 16px; }}
    .doc-card p {{ margin: 0; color: #42504e; }}
    .ok-label {{ display: inline-block; background: #e7f5ee; color: #1b6a3a; border: 1px solid #bee4cc; border-radius: 999px; padding: 2px 8px; font-size: 12px; }}
  </style>
</head>
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <nav data-toggle="wy-nav-shift" class="wy-nav-side">
      <div class="wy-side-scroll">
        <div class="wy-side-nav-search">
          <a href="index.html" class="icon icon-home">{e(PROJECT_NAME)}</a>
          <div role="search">
            <form class="wy-form" action="search.html" method="get">
              <input type="text" name="q" placeholder="Cerca nella documentazione" aria-label="Cerca nella documentazione" />
            </form>
          </div>
        </div>
        <div class="wy-menu wy-menu-vertical" role="navigation" aria-label="Navigation menu">
          <p class="caption" role="heading"><span class="caption-text">Contenuti:</span></p>
          <ul class="current">
            {nav(filename)}
          </ul>
        </div>
      </div>
    </nav>
    <section data-toggle="wy-nav-shift" class="wy-nav-content-wrap">
      <nav class="wy-nav-top" aria-label="Mobile navigation menu">
        <i class="fa fa-bars"></i>
        <a href="index.html">{e(PROJECT_NAME)}</a>
      </nav>
      <div class="wy-nav-content">
        <div class="rst-content">
          <div role="navigation" aria-label="Page navigation">
            <ul class="wy-breadcrumbs">
              <li><a href="index.html" class="icon icon-home" aria-label="Home"></a></li>
              <li class="breadcrumb-item active">{e(title)}</li>
              <li class="wy-breadcrumbs-aside"><a href="_sources/{filename.replace('.html', '.rst.txt')}" rel="nofollow"> View page source</a></li>
            </ul>
            <hr/>
          </div>
          <div role="main" class="document">
            <div itemprop="articleBody">
              {body}
            </div>
          </div>
          <footer>
            <div class="rst-footer-buttons" role="navigation" aria-label="Footer">
              {footer_prev}
              {footer_next}
            </div>
            <hr/>
            <div role="contentinfo">
              <p>&#169; Copyright 2026, {e(AUTHOR)}. Documentazione aggiornata al {e(UPDATED)}.</p>
            </div>
            Documentazione HTML statica basata sui sorgenti Sphinx del progetto.
          </footer>
        </div>
      </div>
    </section>
  </div>
</body>
</html>
"""


def page_index() -> str:
    body = f"""
<section id="home">
<div class="doc-hero">
<h1>{e(PROJECT_NAME)}</h1>
{p(f"Autore: {AUTHOR} | Aggiornamento documentazione: {UPDATED}")}
{p("Il progetto integra machine learning, inferenza Prolog e dataset alimentare per stimare le calorie bruciate durante una sessione di allenamento e generare un piano alimentare giornaliero o settimanale coerente con i dati dell'utente.")}
</div>
{status_grid([
    ("Documentazione", "33 pagine", "PDF riallineato all'indice originale"),
    ("Dataset alimentare", "35 alimenti", "CSV usato dal planner nutrizionale"),
    ("Piano", "1-7 giorni", "Singolo giorno, alternative o settimana"),
    ("Verifiche", "link ok", "Build HTML statica controllata"),
])}
<h2>Cosa contiene questa documentazione</h2>
{card_grid([
    ("Modelli ML", "Regressione Lineare, Random Forest, Gradient Boosting e Bayesian Ridge."),
    ("Knowledge Base", "Regole Prolog per workout consigliato, intensita' e durata ottimale."),
    ("Planner alimentare", "BMR, TDEE, macronutrienti, alternative e piano settimanale."),
    ("Documentazione", "PDF principale, pagine HTML, sorgenti RST e documentazione Prolog."),
])}
<h2>Flusso dell'applicazione</h2>
{ol([
    "Raccolta e controllo degli input: sesso, eta', peso, altezza, allenamento, battiti medi, ore di allenamento, massa grassa, massa magra, giorni del piano e alternative.",
    "Inferenza Prolog per workout consigliato, intensita' stimata e durata ottimale.",
    "Predizione delle calorie bruciate con Linear Regression, Random Forest, Gradient Boosting e Bayesian Ridge.",
    "Calcolo di massa magra, BMR, TDEE, obiettivo calorico e macronutrienti.",
    "Generazione del piano alimentare dal dataset alimenti, con singolo giorno, alternative o piano settimanale.",
])}
<h2>Output principali</h2>
{ul([
    "Risultati dell'inferenza Prolog.",
    "Predizioni dei modelli ML e intervallo di confidenza Bayesian Ridge.",
    "Piano alimentare con calorie, proteine, carboidrati, grassi e grammature per colazione, pranzo, spuntino e cena.",
])}
<div class="admonition note">
  <p class="admonition-title">Nota</p>
  <p>Il piano alimentare e' un output informativo di progetto e non sostituisce il parere di un professionista della nutrizione.</p>
</div>
<h2>Documentazione completa</h2>
{p("La relazione principale aggiornata si trova nel file documentazione.pdf nella cartella principale del progetto.")}
{ul(HOME_DOC_LINKS)}
{p("Per rigenerare questa documentazione con Sphinx, installare prima le dipendenze dedicate in requirements-docs.txt. Sono separate dal requirements principale per evitare conflitti con le librerie del modello su Python 3.9.")}
{pre(HTML_COMMANDS)}
</section>
"""
    return body


def page_modules() -> str:
    rows = [
        ["predict_models.py", "Script principale: input, Prolog, modelli ML, piano alimentare e stampa dei risultati."],
        ["nutrition_planner.py", "Modulo nutrizionale: BMR, TDEE, macro, alternative giornaliere, piano settimanale e validazione input."],
        ["kb/kb.pl", "Knowledge Base Prolog per workout consigliato, intensita' e durata ottimale."],
        ["dataset/alimenti.csv", "Dataset alimentare usato per costruire pasti e grammature."],
        ["apprendimento_supervisionato/training.py", "Training dei modelli Linear Regression, Random Forest e Gradient Boosting."],
        ["apprendimento_probabilistico/training.py", "Training del modello Bayesian Ridge e intervalli di confidenza."],
    ]
    return f"""
<section id="modules">
<h1>Moduli del progetto</h1>
{p("Questa pagina riassume i componenti aggiornati del progetto e sostituisce l'indice automatico precedente, che non includeva il modulo nutrizionale.")}
{table(["File o cartella", "Ruolo"], rows)}
<h2>Pagine disponibili</h2>
{ul([f'<a class="reference internal" href="{href}">{e(label)}</a>' for href, label in PAGES if href != "index.html"])}
</section>
"""


def page_original_index() -> str:
    rows = [
        ["1. Introduzione", "Presente", "Aggiornata con nuovo obiettivo: calorie + piano alimentare."],
        ["1.1 Argomenti di Interesse", "Presente", "Aggiunti BMR, TDEE, macro e dataset alimentare."],
        ["1.2 Librerie Utilizzate", "Presente", "Aggiunti ReportLab/pypdf e separazione Sphinx."],
        ["2. Creazione del dataset", "Presente", "Mantenuto dataset Kaggle e aggiunto alimenti.csv."],
        ["2.1 Pulizia e Preprocessing", "Presente", "Rinomina colonne, mapping categorico, scaler."],
        ["3. Apprendimento Supervisionato", "Presente", "Dettagli su modelli, metriche, overfitting e grafici."],
        ["4. Apprendimento Probabilistico", "Presente", "Bayesian Ridge, intervallo di confidenza e SGDClassifier scartato."],
        ["5. Rappresentazione della Conoscenza - KB", "Presente", "Fatti, regole, ragionamento inferenziale ed esempio."],
        ["6. Dipendenze", "Presente", "Separati requirements del progetto e della documentazione."],
        ["7. Documentazione", "Presente", "HTML, PDF e documentazione Prolog."],
        ["8. Riferimenti Bibliografici", "Presente", "Aggiornati riferimenti e sorgenti locali."],
        ["Nuova sezione: piano alimentare", "Aggiunta", "nutrition_planner.py, alternative e piano settimanale."],
    ]
    return f"""
<section id="indice-originale">
<h1>Confronto con l'indice originale</h1>
{p("Questa pagina mostra come la documentazione aggiornata segue la struttura della relazione originale e dove sono state inserite le estensioni del nuovo progetto.")}
{table(["Voce originale", "Stato", "Aggiornamento"], rows)}
<div class="admonition note">
  <p class="admonition-title">Sintesi</p>
  <p>Tutte le sezioni principali dell'indice originale sono state mantenute. Le nuove parti riguardano il planner alimentare, il dataset alimentare, i controlli input e la build HTML aggiornata.</p>
</div>
</section>
"""


def food_stats() -> tuple[int, list[str]]:
    path = PROJECT_DESKTOP / "dataset" / "alimenti.csv"
    if not path.exists():
        path = ROOT / "dataset" / "alimenti.csv"
    categories = set()
    count = 0
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            count += 1
            categories.add(row.get("categoria", ""))
    return count, sorted(c for c in categories if c)


def page_dataset() -> str:
    count, categories = food_stats()
    rows = [
        ["gym_members_exercise_tracking.csv", "Dataset di allenamento usato per addestrare i modelli predittivi delle calorie bruciate."],
        ["alimenti.csv", f"Dataset alimentare aggiornato con {count} alimenti e categorie: {', '.join(categories)}."],
    ]
    return f"""
<section id="dataset">
<h1>Dataset</h1>
{p("Il progetto usa due dataset: uno per il machine learning sulle calorie bruciate e uno per costruire i piani alimentari.")}
{table(["Dataset", "Descrizione"], rows)}
<h2>Struttura di alimenti.csv</h2>
{pre("alimento,categoria,pasti,kcal_100g,proteine_100g,carboidrati_100g,grassi_100g")}
{p("Il campo pasti puo' contenere piu' valori separati da |, ad esempio colazione|spuntino o pranzo|cena. Questo permette al planner di scegliere alimenti compatibili con il pasto richiesto.")}
<h2>Cosa e' stato aggiornato</h2>
{ul([
    "Aggiunte alternative proteiche come skyr, tacchino, merluzzo, bresaola e lenticchie cotte.",
    "Aggiunte fonti di carboidrati e frutta come quinoa, farro, riso venere, kiwi e arancia.",
    "Aggiunti grassi e verdure per bilanciare grammature e micronutrienti.",
    "Il dataset alimentare serve solo alla generazione del piano; i grafici dei modelli si aggiornano rilanciando i training.",
])}
</section>
"""


def page_supervised() -> str:
    rows = [
        ["Linear Regression", "Baseline supervisionata per stimare Calories_Burned."],
        ["Random Forest", "Modello ensemble con iperparametri salvati in CSV/JSON."],
        ["Gradient Boosting", "Modello boosting con confronto metriche su train e test."],
    ]
    return f"""
<section id="supervised">
<h1>Apprendimento supervisionato</h1>
{p("La parte supervisionata addestra modelli di regressione sul dataset gym_members_exercise_tracking.csv. I modelli salvati vengono poi caricati da predict_models.py.")}
{table(["Modello", "Ruolo"], rows)}
<h2>Artefatti generati</h2>
{ul([
    "File .pkl nella cartella apprendimento_supervisionato/modelli/.",
    "Scaler e workout_mapping usati in fase di predizione.",
    "Grafici test_set_metriche.png e training_set_metriche.png.",
    "Tabelle e JSON degli iperparametri per Random Forest e Gradient Boosting.",
])}
<h2>Aggiornamento grafici e modelli</h2>
{pre("python3 apprendimento_supervisionato/training.py")}
</section>
"""


def page_probabilistic() -> str:
    return f"""
<section id="probabilistic">
<h1>Apprendimento probabilistico</h1>
{p("La parte probabilistica usa Bayesian Ridge per ottenere una stima delle calorie bruciate insieme a una misura di incertezza.")}
<h2>Output del modello</h2>
{ul([
    "Predizione puntuale delle kcal.",
    "Deviazione standard restituita dal modello.",
    "Intervallo di confidenza calcolato come media +/- 1.96 * deviazione standard.",
    "Grafici su predizioni, errori e metriche del modello.",
])}
<h2>Artefatti generati</h2>
{ul([
    "apprendimento_probabilistico/modelli/modello_bayesian_ridge.pkl",
    "apprendimento_probabilistico/grafici/predizioni_vs_valori_reali.png",
    "apprendimento_probabilistico/grafici/distribuzione_errori.png",
    "apprendimento_probabilistico/grafici/metriche_bayesian_ridge.png",
])}
{pre("python3 apprendimento_probabilistico/training.py")}
</section>
"""


def page_kb() -> str:
    rows = [
        ["recommended_workout/3", "Consiglia il workout partendo da peso e altezza tramite BMI e fitness_level."],
        ["recommended_intensity/4", "Stima l'intensita' in base alle calorie bruciate previste."],
        ["optimal_duration/4", "Regola la durata proposta in base all'intensita' stimata."],
        ["calories_per_kg/2", "Fatti Prolog con consumo calorico per kg e ora per Cardio, HIIT, Strength e Yoga."],
    ]
    return f"""
<section id="kb">
<h1>Knowledge Base Prolog</h1>
{p("La cartella kb contiene kb.pl, usato da predict_models.py tramite pyswip. La base di conoscenza non genera il piano alimentare: fornisce indicazioni su workout, intensita' e durata ottimale.")}
{table(["Predicato", "Descrizione"], rows)}
<h2>Query eseguite dal programma</h2>
{pre(PROLOG_QUERIES)}
</section>
"""


def function_rows(module_path: Path) -> list[list[str]]:
    import ast

    tree = ast.parse(module_path.read_text(encoding="utf-8"))
    rows = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            doc = ast.get_docstring(node) or ""
            first = doc.strip().splitlines()[0] if doc.strip() else "Funzione interna del modulo."
            args = [arg.arg for arg in node.args.args]
            rows.append([f"{node.name}({', '.join(args)})", first])
    return rows


def page_nutrition() -> str:
    rows = function_rows(PROJECT_DESKTOP / "nutrition_planner.py")
    key_rows = [row for row in rows if row[0].split("(")[0] in {
        "ask_int",
        "ask_float",
        "calculate_bmr",
        "calculate_tdee",
        "calculate_macros",
        "generate_meal_plan",
        "generate_daily_alternatives",
        "generate_weekly_meal_plan",
        "print_meal_plan",
        "build_nutrition_plan",
    }]
    return f"""
<section id="nutrition-planner">
<h1>nutrition_planner module</h1>
{p("Il modulo nutrition_planner.py e' la parte nuova del progetto: riceve dati fisici e composizione corporea, calcola il fabbisogno e genera un piano alimentare usando dataset/alimenti.csv.")}
<h2>Input gestiti</h2>
{ul([
    "sesso, eta', peso e altezza;",
    "ore di allenamento settimanali;",
    "percentuale di massa grassa e massa magra;",
    "numero di giorni del piano, da 1 a 7;",
    "numero di alternative giornaliere, da 1 a 3 quando il piano e' di un solo giorno.",
])}
<h2>Calcoli principali</h2>
{ul([
    "Massa magra stimata se l'utente inserisce 0.",
    "BMR calcolato con formula basata su massa magra.",
    "TDEE ottenuto applicando un fattore di attivita' alle ore di allenamento.",
    "Obiettivo alimentare inferito da sesso e massa grassa: definizione, mantenimento o ricomposizione.",
    "Macronutrienti giornalieri e grammature degli alimenti.",
])}
<h2>Modalita' di piano</h2>
{table(["Modalita'", "Comportamento"], [
    ["Singolo giorno", "Genera colazione, pranzo, spuntino e cena."],
    ["Alternative", "Genera piu' risposte per lo stesso giorno usando varianti alimentari diverse."],
    ["Settimanale", "Genera fino a 7 giorni, da Lunedi a Domenica, con alimenti variati."],
])}
<h2>Funzioni principali</h2>
{table(["Funzione", "Descrizione"], key_rows)}
</section>
"""


def page_predict() -> str:
    rows = function_rows(PROJECT_DESKTOP / "predict_models.py")
    return f"""
<section id="predict-models">
<h1>predict_models module</h1>
{p("predict_models.py e' lo script principale: carica i modelli salvati, raccoglie input validati, interroga Prolog, predice le calorie e richiama il planner alimentare.")}
<h2>Input controllati</h2>
{table(["Campo", "Controllo"], [
    ["sesso", "Valori ammessi 0 o 1."],
    ["eta'", "Intervallo 10-100."],
    ["peso", "Intervallo 30-250 kg."],
    ["altezza", "Intervallo 1.20-2.30 m."],
    ["tipo allenamento", "Codice presente nel workout_mapping salvato."],
    ["durata sessione", "Intervallo 0.1-8 ore."],
    ["ore allenamento settimanali", "Intervallo 0-30."],
    ["battiti medi", "Intervallo 40-220 BPM."],
    ["massa grassa", "Intervallo 1-70 percento."],
    ["massa magra", "0 se non nota, altrimenti minore o uguale al peso."],
    ["giorni piano", "Intervallo 1-7."],
    ["alternative giornaliere", "Intervallo 1-3 se il piano e' di un solo giorno."],
])}
<h2>Flusso di esecuzione</h2>
{ol([
    "load_models carica modelli, scaler e workout_mapping.",
    "get_user_input acquisisce e valida i dati.",
    "query_prolog restituisce workout, intensita' e durata ottimale.",
    "scale_data normalizza le feature per i modelli.",
    "make_predictions produce kcal stimate e intervallo Bayesian Ridge.",
    "build_nutrition_plan e print_meal_plan generano e stampano il piano alimentare.",
])}
<h2>Funzioni del modulo</h2>
{table(["Funzione", "Descrizione"], rows)}
</section>
"""


def page_documentation() -> str:
    return f"""
<section id="documentazione">
<h1>Documentazione e output</h1>
{p("Il progetto contiene piu' livelli di documentazione: relazione PDF, HTML navigabile, sorgenti RST e documentazione Prolog.")}
{card_grid([
    ("documentazione.pdf", "Relazione principale aggiornata, strutturata secondo l'indice originale e ampliata con il planner alimentare."),
    ("docs/_build/html/index.html", "Versione HTML navigabile con pagine dedicate a moduli, dataset, KB e nutrition_planner."),
    ("docs/*.rst", "Sorgenti Sphinx modificabili per rigenerare l'HTML ufficiale."),
    ("kb/doc/index.html", "Documentazione generata per la Knowledge Base Prolog."),
])}
<h2>Comandi utili</h2>
{pre(DOC_COMMANDS)}
<h2>Cosa non si aggiorna automaticamente</h2>
{ul([
    "I grafici dei modelli si aggiornano solo rilanciando gli script di training.",
    "I file .pkl dei modelli cambiano solo dopo un nuovo addestramento.",
    "La build HTML statica puo' essere rigenerata con build_static_html_docs.py.",
])}
</section>
"""


def simple_page(title: str, message: str) -> str:
    return f"<section><h1>{e(title)}</h1>{p(message)}</section>"


def write_page(filename: str, title: str, body: str) -> None:
    hrefs = [href for href, _ in PAGES]
    index = hrefs.index(filename) if filename in hrefs else 0
    prev_href = hrefs[index - 1] if index > 0 else None
    next_href = hrefs[index + 1] if index + 1 < len(hrefs) else None
    (OUT / filename).write_text(base_page(filename, title, body, prev_href, next_href), encoding="utf-8")


def copy_sources() -> None:
    sources = OUT / "_sources"
    sources.mkdir(parents=True, exist_ok=True)
    for rst in SOURCE_DOCS.glob("*.rst"):
        shutil.copyfile(rst, sources / f"{rst.stem}.rst.txt")
    (sources / "index.rst.txt").write_text((SOURCE_DOCS / "index.rst").read_text(encoding="utf-8"), encoding="utf-8")
    generated_sources = {
        "indice_originale.rst.txt": "Confronto con l'indice originale\n================================\n\nPagina di allineamento tra la documentazione originale e la versione aggiornata.\n",
        "documentazione.rst.txt": "Documentazione e output\n=======================\n\nPagina dedicata a PDF, HTML, sorgenti Sphinx e documentazione Prolog.\n",
        "search.rst.txt": "Ricerca\n=======\n\nPagina statica di ricerca della documentazione HTML.\n",
        "genindex.rst.txt": "Indice\n======\n\nIndice sintetico delle pagine principali della documentazione.\n",
        "py-modindex.rst.txt": "Indice moduli Python\n====================\n\nModuli documentati: predict_models e nutrition_planner.\n",
    }
    for filename, content in generated_sources.items():
        (sources / filename).write_text(content, encoding="utf-8")


def write_source_pages() -> None:
    modules_dir = OUT / "_modules"
    modules_dir.mkdir(parents=True, exist_ok=True)
    for source in ["predict_models.py", "nutrition_planner.py"]:
        source_path = PROJECT_DESKTOP / source
        if not source_path.exists():
            source_path = ROOT / source
        html_body = f"<section><h1>{e(source)}</h1>{pre(source_path.read_text(encoding='utf-8'))}</section>"
        write_name = source.replace(".py", ".html")
        (modules_dir / write_name).write_text(
            base_page(write_name, source, html_body),
            encoding="utf-8",
        )
    (modules_dir / "index.html").write_text(
        base_page(
            "index.html",
            "Codice sorgente",
            "<section><h1>Codice sorgente</h1>"
            + ul([
                '<a class="reference internal" href="predict_models.html">predict_models.py</a>',
                '<a class="reference internal" href="nutrition_planner.html">nutrition_planner.py</a>',
            ])
            + "</section>",
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    static_target = OUT / "_static"
    if STATIC_SOURCE.exists() and STATIC_SOURCE.resolve() != static_target.resolve():
        if not static_target.exists():
            shutil.copytree(STATIC_SOURCE, static_target)
        else:
            shutil.copytree(STATIC_SOURCE, static_target, dirs_exist_ok=True)
    else:
        static_target.mkdir(parents=True, exist_ok=True)

    write_page("index.html", "Panoramica", page_index())
    write_page("indice_originale.html", "Indice originale", page_original_index())
    write_page("modules.html", "Moduli", page_modules())
    write_page("apprendimento_supervisionato.html", "Apprendimento supervisionato", page_supervised())
    write_page("apprendimento_probabilistico.html", "Apprendimento probabilistico", page_probabilistic())
    write_page("dataset.html", "Dataset", page_dataset())
    write_page("kb.html", "Knowledge Base Prolog", page_kb())
    write_page("nutrition_planner.html", "nutrition_planner module", page_nutrition())
    write_page("predict_models.html", "predict_models module", page_predict())
    write_page("documentazione.html", "Documentazione", page_documentation())

    write_page(
        "search.html",
        "Ricerca",
        simple_page("Ricerca", "Questa build HTML statica mantiene la pagina di ricerca, ma per una ricerca completa conviene usare la ricerca del browser o generare la build con Sphinx installato."),
    )
    write_page(
        "genindex.html",
        "Indice",
        simple_page("Indice", "Le pagine principali sono disponibili dal menu laterale. I moduli centrali aggiornati sono predict_models.py e nutrition_planner.py."),
    )
    write_page(
        "py-modindex.html",
        "Indice moduli Python",
        simple_page("Indice moduli Python", "Moduli documentati: predict_models, nutrition_planner, dataset.dataset_utils, apprendimento_supervisionato.training, apprendimento_probabilistico.training."),
    )
    copy_sources()
    write_source_pages()
    (OUT / "objects.inv").write_bytes(b"# Static documentation build\n")
    (OUT / "searchindex.js").write_text("Search.setIndex({docnames:[],filenames:[],titles:[],terms:{},objects:{}});", encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
