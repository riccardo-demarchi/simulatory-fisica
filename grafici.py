import matplotlib.pyplot as plt
import numpy as np

# Parametri
m1 = 2
m2 = 2

x_min = (1/(m1 * m2-1))**(1/m2)
# Valori di x
print("Valore di x_min:", x_min)
x = np.linspace(x_min + 1e-4, 15, 2000)

# Equazioni della curva critica
a1 = m1 * m2 * x**(m2+1) / (x**m2 * (m2 * m1 - 1) - 1)

a2 = (1+ x**m2) * ((1 + x**m2) / ((m1 * m2 - 1) * x**m2 - 1))**(1/m1)

# Creazione del grafico
plt.figure(figsize=(8, 7))

# Curva critica
plt.plot(a1, a2, label="Curva critica", linewidth=2)

# Regione di bistabilità
plt.fill_between(a1, a2, 15, alpha=0.1)

# Scritta nelle regioni
plt.text(0.2, 0.2, "Regione\nmonostabile", fontsize=16)
plt.text(7.5, 7.5, "Regione\nbistabile", fontsize=16)

# Limiti degli assi
plt.xlim(0, 15)
plt.ylim(0, 15)

# Nomi degli assi
plt.xlabel("Tasso di trascrizione gene 1, a1", fontsize=20)
plt.ylabel("Tasso di trascrizione gene 2, a2", fontsize=20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
# Titolo
plt.title("Regione di bistabilità per m1 = m2 = 2", fontsize=22)

plt.grid(True)
plt.legend()

plt.show()