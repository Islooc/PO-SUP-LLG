import matplotlib.pyplot as plt
import numpy as np

# Reprise des KPI calculés
kpis = {
    "Ponctualité client (%)": 84.0,
    "ISR (Stock/Ventes)": 0.2,
    "Coût possession stock (€)": 30000.0,
    "Ponctualité fournisseurs (%)": 70.0,
    "DSI (jours)": 97.33,
    "Coût transport/tonne (€)": 50.0,
    "Commandes parfaites (%)": 77.0
}

# Seuils maximums pour normaliser (1 = bon, 0 = critique)
seuils_max = {
    "Ponctualité client (%)": 100,
    "ISR (Stock/Ventes)": 0.5,   # 0.2 est idéal, mais 0.5 reste acceptable
    "Coût possession stock (€)": 50000,  # arbitraire pour échelle
    "Ponctualité fournisseurs (%)": 100,
    "DSI (jours)": 150,  # plus c’est bas, mieux c’est (donc inverse plus tard)
    "Coût transport/tonne (€)": 100,
    "Commandes parfaites (%)": 100
}

# Normalisation des KPI (entre 0 et 1)
normalized_kpis = []
labels = list(kpis.keys())

for label in labels:
    val = kpis[label]
    max_val = seuils_max[label]

    if "ISR" in label or "DSI" in label or "Coût" in label:
        # KPI où une valeur plus basse est meilleure
        normalized = max(0, 1 - (val / max_val))
    else:
        # KPI où une valeur plus haute est meilleure
        normalized = min(1, val / max_val)

    normalized_kpis.append(normalized)

# Bouclage pour le radar
values = normalized_kpis + [normalized_kpis[0]]
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

# 🎯 Création du radar chart
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

ax.plot(angles, values, color='blue', linewidth=2, linestyle='solid')
ax.fill(angles, values, color='skyblue', alpha=0.4)

# 🏷️ Étiquettes
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels, fontsize=10)

# ✅ Axe de 0 à 1
ax.set_ylim(0, 1)
ax.set_title("Radar des KPI Supply Chain (Normalisés)", size=15, pad=20)

plt.tight_layout()
plt.show()
