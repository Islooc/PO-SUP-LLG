import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Définition des KPI à saisir
kpi_labels = [
    "Commandes totales",
    "Commandes livrées à temps",
    "Stock moyen (€)",
    "Ventes nettes (€)",
    "Coût des biens vendus (€)",
    "Taux de possession du stock (ex: 0.25)",
    "Commandes parfaites",
    "Coût total transport (€)",
    "Tonnage total (tonnes)",
    "Livraisons fournisseurs (10 valeurs : True/False séparées par virgules)"
]

# Fonction de traitement et affichage du radar
def generer_radar():
    try:
        # Récupérer les données saisies
        commandes = int(entries[0].get())
        commandes_livrees = int(entries[1].get())
        stock_moyen = float(entries[2].get())
        ventes_net = float(entries[3].get())
        cout_biens_vendus = float(entries[4].get())
        taux_possession = float(entries[5].get())
        commandes_parfaites = int(entries[6].get())
        cout_transport = float(entries[7].get())
        tonnage = float(entries[8].get())
        livraisons_fournisseurs = [val.strip().lower() == "true" for val in entries[9].get().split(",")]

        # Calculs KPI
        kpis = {
            "Ponctualité client (%)": (commandes_livrees / commandes) * 100,
            "ISR (Stock/Ventes)": stock_moyen / ventes_net,
            "Coût possession stock (€)": stock_moyen * taux_possession,
            "Ponctualité fournisseurs (%)": sum(livraisons_fournisseurs) / len(livraisons_fournisseurs) * 100,
            "DSI (jours)": (stock_moyen / cout_biens_vendus) * 365,
            "Coût transport/tonne (€)": cout_transport / tonnage,
            "Commandes parfaites (%)": commandes_parfaites / commandes * 100
        }

        # Seuils pour normalisation
        seuils_max = {
            "Ponctualité client (%)": 100,
            "ISR (Stock/Ventes)": 0.5,
            "Coût possession stock (€)": 50000,
            "Ponctualité fournisseurs (%)": 100,
            "DSI (jours)": 150,
            "Coût transport/tonne (€)": 100,
            "Commandes parfaites (%)": 100
        }

        # Normalisation
        normalized_kpis = []
        labels = list(kpis.keys())

        for label in labels:
            val = kpis[label]
            max_val = seuils_max[label]

            if "ISR" in label or "DSI" in label or "Coût" in label:
                normalized = max(0, 1 - (val / max_val))
            else:
                normalized = min(1, val / max_val)

            normalized_kpis.append(normalized)

        # Radar chart
        values = normalized_kpis + [normalized_kpis[0]]
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, values, color='blue', linewidth=2)
        ax.fill(angles, values, color='skyblue', alpha=0.4)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10)
        ax.set_ylim(0, 1)
        ax.set_title("Radar des KPI Supply Chain", size=15, pad=20)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue :\n{e}")

# Interface Tkinter
root = tk.Tk()
root.title("Analyse KPI Supply Chain")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

entries = []
for label in kpi_labels:
    tk.Label(frame, text=label).pack(anchor="w")
    entry = tk.Entry(frame, width=50)
    entry.pack()
    entries.append(entry)

tk.Button(frame, text="Générer le graphique radar", command=generer_radar, bg="green", fg="white").pack(pady=10)

root.mainloop()
