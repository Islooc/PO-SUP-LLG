# 📦 Imports
import matplotlib.pyplot as plt
import seaborn as sns

# ✅ Données simulées
data = {
    'commandes': 500,
    'commandes_livrees_a_temps': 420,
    'stock_moyen': 120000,  # en €
    'ventes_net': 600000,   # en €
    'cout_biens_vendus': 450000,
    'taux_possession': 0.25,
    'commandes_parfaites': 385,
    'cout_total_transport': 75000,  # en €
    'tonnage_total': 1500,  # en tonnes
    'delais_livraisons_fournisseurs': [True, True, False, True, False, True, True, True, False, True],
}

# 📊 Calculs des KPI

ponctualite_client = (data['commandes_livrees_a_temps'] / data['commandes']) * 100
ISR = data['stock_moyen'] / data['ventes_net']
cout_possession_stock = data['stock_moyen'] * data['taux_possession']
ponctualite_fournisseurs = (sum(data['delais_livraisons_fournisseurs']) / len(data['delais_livraisons_fournisseurs'])) * 100
DSI = (data['stock_moyen'] / data['cout_biens_vendus']) * 365
cout_transport_tonne = data['cout_total_transport'] / data['tonnage_total']
perfect_order_rate = (data['commandes_parfaites'] / data['commandes']) * 100

# 📦 Résumé des KPI
kpis = {
    "Ponctualité client (%)": ponctualite_client,
    "ISR (Stock/Ventes)": ISR,
    "Coût possession stock (€)": cout_possession_stock,
    "Ponctualité fournisseurs (%)": ponctualite_fournisseurs,
    "DSI (jours)": DSI,
    "Coût transport/tonne (€)": cout_transport_tonne,
    "Commandes parfaites (%)": perfect_order_rate
}

# 🔎 Seuils critiques de référence
seuils = {
    "Ponctualité client (%)": 95,
    "ISR (Stock/Ventes)": 0.2,
    "Ponctualité fournisseurs (%)": 90,
    "DSI (jours)": 60,
    "Commandes parfaites (%)": 98,
    "Coût transport/tonne (€)": 50,  # Seuil indicatif
}

# 🛑 Détection des alertes
alertes = {
    k: "🔴" if (
        (k in seuils and (
            (v < seuils[k] and '%' in k) or
            (v > seuils[k] and ('ISR' in k or 'DSI' in k or '€' in k))
        ))
        ) else "🟢"
    for k, v in kpis.items()
}

# 🖨️ Affichage des KPI et alertes
print("📌 Résultats des KPI logistiques :\n")
for k, v in kpis.items():
    print(f"{k:<35} : {v:>6.2f} {alertes[k]}")

# 📈 Visualisation des KPI
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))

labels = list(kpis.keys())
values = list(kpis.values())
colors = ['green' if alertes[k] == "🟢" else 'red' for k in labels]

sns.barplot(x=values, y=labels, palette=colors)
plt.title("KPI Logistiques - Analyse annuelle", fontsize=16)
plt.xlabel("Valeurs")
plt.tight_layout()
plt.show()
