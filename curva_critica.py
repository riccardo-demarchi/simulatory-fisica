import numpy as np
import matplotlib.pyplot as plt

# Impostazioni generali dei parametri
m1 = 2.0
m2 = 2.0

# --- GRAFICO 1: Sistema Switch (Toggle Switch / Feedback Negativo) ---
# Estendiamo molto il range di x per far continuare i rami oltre i bordi del grafico
x_min_switch = 1 / np.sqrt(m1 * m2 - 1) + 1e-4
x_switch = np.linspace(x_min_switch, 30.0, 5000)

a1_switch = (m1 * m2 * x_switch**(m2 + 1)) / (x_switch**m2 * (m2 * m1 - 1) - 1)
a2_switch = (1 + x_switch**m2) * ((1 + x_switch**m2) / ((m1 * m2 - 1) * x_switch**m2 - 1))**(1 / m1)

plt.figure(figsize=(7, 6))

# Curva critica
plt.plot(a1_switch, a2_switch, label='Curva critica', linewidth=2)

# Riempimento della regione bistabile (aggiungiamo un punto (100,100) per chiudere il poligono fuori dall'area visibile)
a1_fill = np.append(a1_switch, 100)
a2_fill = np.append(a2_switch, 100)
plt.fill(a1_fill, a2_fill, alpha=0.1, color='tab:blue')

# Limiti assi a 14 e griglia
plt.xlim(0, 14)
plt.ylim(0, 14)
plt.grid(True, which='both', linestyle='-', linewidth=0.5)

# Titoli ed Etichette con pedici formattati in LaTeX
plt.title(r'Regione di bistabilità per $m_1 = m_2 = 2$', fontsize=18)
plt.xlabel(r'Tasso di trascrizione gene 1, $a_1$', fontsize=17)
plt.ylabel(r'Tasso di trascrizione gene 2, $a_2$', fontsize=17)
# Impostazione della dimensione dei numeri sugli assi
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Testi interni (leggermente riposizionati per la scala a 14)
plt.text(8.0, 7.5, 'Regione\nbistabile', fontsize=14, ha='center', va='center')
plt.text(1.8, 0.8, 'Regione\nmonostabile', fontsize=14, ha='center', va='center')

plt.legend(loc='upper right', frameon=True, fontsize=15)
plt.tight_layout()
plt.show()


# --- GRAFICO 2: Sistema Positivo (Autoregolazione / Feedback Positivo) ---
x_pos = np.linspace(1e-4, np.sqrt(m1 * m2 - 1) - 1e-4, 5000)

a1_pos = (m1 * m2 * x_pos**m2) / (m1 * m2 - 1 - x_pos**m2)
a2_pos = (1 + 1 / (x_pos**m2)) * ((m1 * m2) / (1 + x_pos**m2) - 1)**(1 / m1)

plt.figure(figsize=(7, 6))

# Curva critica
plt.plot(a1_pos, a2_pos, label='Curva critica', linewidth=2)

# Riempimento della regione bistabile (area sopra la curva)
plt.fill_between(a1_pos, a2_pos, 15, alpha=0.1, color='tab:blue')

# Limiti assi a 14 e griglia
plt.xlim(0, 14)
plt.ylim(0, 14)
plt.grid(True, which='both', linestyle='-', linewidth=0.5)

# Titoli ed Etichette con pedici formattati in LaTeX
plt.title(r'Regione di bistabilità per $m_1 = m_2 = 2$', fontsize=18)
plt.xlabel(r'Tasso di trascrizione gene 1, $a_1$', fontsize=17)
plt.ylabel(r'Tasso di trascrizione gene 2, $a_2$', fontsize=17)
# Impostazione della dimensione dei numeri sugli assi
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Testi interni
plt.text(8.0, 7.5, 'Regione\nbistabile', fontsize=14, ha='center', va='center')
plt.text(1.8, 0.8, 'Regione\nmonostabile', fontsize=14, ha='center', va='center')

plt.legend(loc='upper right', frameon=True, fontsize=15)
plt.tight_layout()
plt.show()