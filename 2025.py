import fastf1
import fastf1.plotting
import matplotlib.pyplot as plt

# Configuration graphique
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

YEAR = 2025
drivers = ['VER', 'PER', 'LEC', 'HAM', 'NOR', 'PIA', 'RUS', 'ANT', 
           'ALO', 'STR', 'SAI', 'ALB', 'GAS', 'DOO', 'TSU', 'LAW', 
           'HUL', 'BEA', 'OCO', 'BOR', 'HAD']

all_standings = {d: [0] for d in drivers}
gp_names = ['Début']

# Récupération du calendrier
schedule = fastf1.get_event_schedule(YEAR)
completed_rounds = schedule[schedule['EventFormat'] != 'testing'].dropna(subset=['EventDate'])

print(f"--- GÉNÉRATION DU CLASSEMENT FINAL {YEAR} (Courses + Sprints) ---")

last_session = None

for i, round_data in completed_rounds.iterrows():
    gp_name = round_data['EventName']
    print(f"Traitement de {gp_name}...")
    
    try:
        # 1. On récupère les points du DIMANCHE (Race)
        sess_r = fastf1.get_session(YEAR, gp_name, 'R')
        sess_r.load(telemetry=False, weather=False, messages=False)
        res_r = sess_r.results
        last_session = sess_r
        
        # 2. On récupère les points du SAMEDI (Sprint) - La méthode qui marche !
        res_s = None
        # On ne cherche le sprint que si le format du weekend n'est pas conventionnel
        if 'sprint' in round_data['EventFormat'].lower():
            for s_name in ['Sprint', 'S']:
                try:
                    sess_s = fastf1.get_session(YEAR, gp_name, s_name)
                    sess_s.load(telemetry=False, weather=False, messages=False)
                    res_s = sess_s.results
                    break # Trouvé !
                except:
                    continue

        gp_names.append(gp_name)
        
        # 3. On additionne tout pour chaque pilote
        for d in drivers:
            # Points Dimanche
            row_r = res_r[res_r['Abbreviation'] == d]
            p_r = row_r['Points'].iloc[0] if not row_r.empty else 0
            
            # Points Samedi
            p_s = 0
            if res_s is not None:
                row_s = res_s[res_s['Abbreviation'] == d]
                p_s = row_s['Points'].iloc[0] if not row_s.empty else 0
            
            # Mise à jour du total cumulé
            all_standings[d].append(all_standings[d][-1] + p_r + p_s)

    except Exception:
        print(f"Fin des données à {gp_name}")
        break

# --- PARTIE GRAPHIQUE ---
plt.figure(figsize=(16, 9))

for d in drivers:
    try:
        team_color = fastf1.plotting.get_driver_color(d, session=last_session)
    except:
        team_color = 'gray'
    
    plt.plot(gp_names, all_standings[d], label=d, color=team_color, marker='o', markersize=4, linewidth=2)

plt.title(f'Championnat du Monde de F1 {YEAR}\n(Résultats Officiels : Courses + Sprints)', fontsize=16, fontweight='bold')
plt.xlabel('Grands Prix')
plt.ylabel('Points')
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', fontsize='small')
plt.grid(True, linestyle=':', alpha=0.6)
plt.xticks(rotation=35, ha='right')
plt.tight_layout()

# Sauvegarde propre
plt.savefig(f"F1_2025.png", dpi=300)
print(f"\nTerminé ! Lando Norris finit à {int(all_standings['NOR'][-1])} points.")
plt.show()

# Test de synchronisation avec GitHub Desktop