import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

# On active le design "spécial F1" de FastF1
fastf1.plotting.setup_mpl()

# 1. Chargement de la session (Année, Grand Prix, Session)
session = fastf1.get_session(2023, 'Monaco', 'R')
session.load()

# 2. Sélection des pilotes à comparer
driver_1 = 'VER'
driver_2 = 'ALO'

# 3. Récupération des tours pour chaque pilote
laps_driver_1 = session.laps.pick_driver(driver_1)
laps_driver_2 = session.laps.pick_driver(driver_2)

# 4. Création du graphique
plt.figure(figsize=(12, 6))

# On trace les temps au tour (en secondes)
plt.plot(laps_driver_1['LapNumber'], laps_driver_1['LapTime'].dt.total_seconds(), 
         color='blue', label=driver_1)
plt.plot(laps_driver_2['LapNumber'], laps_driver_2['LapTime'].dt.total_seconds(), 
         color='green', label=driver_2)

# Personnalisation
plt.title(f"Comparaison des temps au tour : {driver_1} vs {driver_2}\n{session.event['EventName']} {session.event.year}")
plt.xlabel("Numéro du tour")
plt.ylabel("Temps au tour (s)")
plt.legend()
plt.grid(True, linestyle='--', alpha=0.6)

plt.show()