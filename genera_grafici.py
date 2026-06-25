import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. GENERAZIONE DEL GRAFICO: REAL vs PREDICTED
# ==========================================

# Nota: Sostituisci queste variabili simulate con i tuoi dati reali:
# y_test = le calorie reali del test set
# y_pred_gb = le calorie predette dal tuo Gradient Boosting
# y_pred_lr = le calorie predette dalla tua Regressione Lineare (opzionale, per confronto)

np.random.seed(42)
y_test = np.random.uniform(150, 800, 100)
y_pred_gb = y_test + np.random.normal(0, 15, 100)   # Modello preciso (Gradient Boosting)
y_pred_lr = y_test + np.random.normal(0, 75, 100)   # Modello meno preciso (Linear Regression)

plt.figure(figsize=(9, 6))

# Disegno dei punti del Gradient Boosting (Modello Scelto)
plt.scatter(y_test, y_pred_gb, color='#1f77b4', alpha=0.7, edgecolors='k', label='Gradient Boosting (Miglior Modello)')

# Disegno dei punti della Regressione Lineare (Baseline di confronto)
plt.scatter(y_test, y_pred_lr, color='#d62728', alpha=0.4, marker='x', label='Linear Regression (Baseline)')

# Linea ideale a 45 gradi (Predizione Perfetta)
lims = [min(y_test.min(), y_pred_gb.min()) - 20, max(y_test.max(), y_pred_gb.max()) + 20]
plt.plot(lims, lims, color='black', linestyle='--', linewidth=2, label='Predizione Perfetta (Y = X)')

plt.title('Valutazione dei Modelli: Calorie Reali vs Calorie Predette', fontsize=14, fontweight='bold', pad=15)
plt.xlabel('Valori Reali (Calories_Burned)', fontsize=12)
plt.ylabel('Valori Predetti dal Modello', fontsize=12)
plt.xlim(lims)
plt.ylim(lims)
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

# Salvataggio del primo grafico
plt.savefig('grafico_regressione_confronto.png', dpi=300)
plt.close()


# ==========================================
# 2. GENERAZIONE DEL GRAFICO: CONFRONTO METRICHE (R2 Score)
# ==========================================

# Inserisci qui i reali punteggi R² ottenuti dai tuoi tre modelli
modelli = ['Linear Regression', 'Random Forest', 'Gradient Boosting']
r2_scores = [0.68, 0.89, 0.94]  # Esempio di valori, inserisci i tuoi veri score dell'R²

plt.figure(figsize=(8, 5))

# Creazione del grafico a barre con colori personalizzati
colori = ['#e74c3c', '#f39c12', '#2ecc71'] # Rosso, Arancione, Verde
barre = plt.bar(modelli, r2_scores, color=colori, edgecolor='black', width=0.5)

# Configurazione dettagli assi e griglia
plt.title('Confronto delle Prestazioni dei Modelli ($R^2$ Score)', fontsize=14, fontweight='bold', pad=15)
plt.ylabel('$R^2$ Score (Più alto è migliore)', fontsize=12)
plt.ylim(0, 1.1)  # Estendiamo leggermente sopra 1.0 per lasciare spazio ai testi
plt.grid(axis='y', linestyle=':', alpha=0.6)

# Aggiunta del valore esatto sopra ogni barra
for barra in barre:
    altezza = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2.0, altezza + 0.02, f'{altezza:.2f}', 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()

# Salvataggio del secondo grafico
plt.savefig('confronto_metriche_r2.png', dpi=300)
plt.close()

print("Grafici generati con successo e salvati nella cartella corrente!")