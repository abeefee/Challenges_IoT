import matplotlib.pyplot as plt

# Dati calcolati
r1_values = [1, 2, 3, 4, 5, 6]
eta_values = [0.407, 0.417, 0.447, 0.453, 0.443, 0.423]

# Creazione del plot
plt.figure(figsize=(8, 5))
plt.plot(r1_values, eta_values, marker='o', linestyle='-', color='b', linewidth=2, markersize=8)

# Formattazione come richiesto dalla traccia
plt.title('Efficiency over values of initial frame size')
plt.xlabel('Initial frame size r1')
plt.ylabel('Efficiency $\eta$')
plt.ylim(0.0, 1.0) # Il prof ha messo l'asse Y da 0.0 a 1.0
plt.grid(True, linestyle='-', color='gray', alpha=0.7)

# Mostra o salva l'immagine
plt.savefig('grafico_esercizio3.png', dpi=300)
plt.show()