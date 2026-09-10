import matplotlib.pyplot as plt
import numpy as np

# Dati aggiornati
livelli = [1, 2, 3, 4]
# Per topics_A.txt il Livello 1 non è stato specificato, quindi lo impostiamo a 0
messaggi_A = [0, 154, 131, 154] 
messaggi_B = [21, 172, 162, 179]

# Impostazioni grafiche
x = np.arange(len(livelli))  # Posizioni delle etichette
width = 0.35  # Larghezza delle barre

fig, ax = plt.subplots(figsize=(10, 6))

# Creazione delle barre
rects1 = ax.bar(x - width/2, messaggi_A, width, label='A.pcapng', color='tab:blue')
rects2 = ax.bar(x + width/2, messaggi_B, width, label='B.pcapng', color='tab:orange')

# Etichette, titolo e legenda
ax.set_title('Distribution of MQTT topic depth for local broker')
ax.set_xlabel('Number of topic levels')
ax.set_ylabel('Number of PUBLISH messages')
ax.set_xticks(x)
ax.set_xticklabels(livelli)
ax.legend()

# Griglia orizzontale tratteggiata (stile screenshot)
ax.yaxis.grid(True, linestyle='--', alpha=0.6)
ax.set_axisbelow(True)

# Ottimizzazione layout e salvataggio
plt.tight_layout()
plt.savefig('mqtt_distribution_v2.png')
plt.show()