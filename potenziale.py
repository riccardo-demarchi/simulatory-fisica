import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import cumulative_trapezoid


# Parametri
m1 = 2
m2 = 2


# Funzioni
def G_neg(x, a2):
    return a2 / (1 + x**m2)


def F_neg(y, a1):
    return a1 / (1 + y**m1)


def h(x, a1, a2):
    return F_neg(G_neg(x, a2), a1) - x


# Intervallo
x = np.linspace(0, 18, 2000)

a1 = [10, 12, 15]
a2 = [10, 12, 15]

plt.figure()

# Calcolo del potenziale
for i, j in zip(a1, a2):
    V = -cumulative_trapezoid(h(x, i, j), x, initial=0)

    plt.plot(x, V, label=fr"$a_1 = {i},\ a_2 = {j}$")


# Grafico del potenziale
plt.xlabel("x", fontsize=23)
plt.ylabel("$V_{eff}(x)$", fontsize=23)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.legend(fontsize=16)
plt.title("Potenziale efficace", fontsize=22)
plt.grid()

plt.show()