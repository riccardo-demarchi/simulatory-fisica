import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from scipy.optimize import root


# ============================================================
# PARAMETRI
# ============================================================

m1 = 2
m2 = 2


# ============================================================
# FUNZIONI DI FEEDBACK
# ============================================================

def positive(x, y, a1, a2):
    f = a1 * y / (1 + y**m1)
    g = a2 * x / (1 + x**m2)
    return f, g


def negative(x, y, a1, a2):
    f = a1 / (1 + y**m1)
    g = a2 / (1 + x**m2)
    return f, g


# ============================================================
# SISTEMA DINAMICO
# ============================================================

def sistema_pos(x, y, a1, a2):
    dxdt = a1 * y**m1 / (1 + y**m1) - x
    dydt = a2 * x**m2 / (1 + x**m2) - y

    return dxdt, dydt


def sistema_neg(x, y, a1, a2):
    dxdt = a1 / (1 + y**m1) - x
    dydt = a2 / (1 + x**m2) - y

    return dxdt, dydt


# ============================================================
# JACOBIANA
# ============================================================

def jacobian(x, y, a1, a2, system_type):

    if system_type == "positive":

        # dx/dt = a1*y^m1/(1+y^m1) - x
        dfdx = -1
        dfdy = a1 * m1 * y**(m1 - 1) / (1 + y**m1)**2

        # dy/dt = a2*x^m2/(1+x^m2) - y
        dgdx = a2 * m2 * x**(m2 - 1) / (1 + x**m2)**2
        dgdy = -1

    elif system_type == "negative":

        # dx/dt = a1/(1+y^m1) - x
        dfdx = -1
        dfdy = -a1 * m1 * y**(m1 - 1) / (1 + y**m1)**2

        # dy/dt = a2/(1+x^m2) - y
        dgdx = -a2 * m2 * x**(m2 - 1) / (1 + x**m2)**2
        dgdy = -1

    else:
        raise ValueError("system_type deve essere 'positive' o 'negative'")

    return np.array([
        [dfdx, dfdy],
        [dgdx, dgdy]
    ])


# ============================================================
# RICERCA DEI PUNTI DI EQUILIBRIO
# ============================================================

def trova_equilibri(a1, a2, system_type,
                    x_range=(0, 12),
                    y_range=(0, 12),
                    n_start=20):

    if system_type == "positive":
        sistema = lambda z: sistema_pos(z[0], z[1], a1, a2)

    elif system_type == "negative":
        sistema = lambda z: sistema_neg(z[0], z[1], a1, a2)

    else:
        raise ValueError("system_type deve essere 'positive' o 'negative'")

    # Punti iniziali distribuiti sul piano
    x0_values = np.linspace(x_range[0], x_range[1], n_start)
    y0_values = np.linspace(y_range[0], y_range[1], n_start)

    equilibri = []

    for x0 in x0_values:
        for y0 in y0_values:

            sol = root(sistema, [x0, y0])

            if sol.success:

                x_eq, y_eq = sol.x

                # Controlliamo che sia dentro il grafico
                if (
                    x_range[0] <= x_eq <= x_range[1]
                    and y_range[0] <= y_eq <= y_range[1]
                ):

                    # Controlliamo che sia effettivamente un equilibrio
                    dx, dy = sistema([x_eq, y_eq])

                    if np.sqrt(dx**2 + dy**2) < 1e-7:

                        # Evitiamo duplicati
                        gia_presente = False

                        for xe, ye in equilibri:
                            if np.sqrt(
                                (x_eq - xe)**2 +
                                (y_eq - ye)**2
                            ) < 1e-5:
                                gia_presente = True
                                break

                        if not gia_presente:
                            equilibri.append((x_eq, y_eq))

    # Ordiniamo i punti per x
    equilibri.sort(key=lambda p: p[0])

    return equilibri


# ============================================================
# CLASSIFICAZIONE DELLA STABILITÀ
# ============================================================

def classifica_equilibrio(x_eq, y_eq, a1, a2, system_type):

    J = jacobian(
        x_eq,
        y_eq,
        a1,
        a2,
        system_type
    )

    autovalori = np.linalg.eigvals(J)

    # Sistema stabile se tutti gli autovalori
    # hanno parte reale negativa
    if np.all(np.real(autovalori) < 0):
        return "stable"

    elif np.any(np.real(autovalori) > 0):
        return "unstable"

    else:
        return "non-hyperbolic"


# ============================================================
# PIANO DELLE NULLCLINE
# ============================================================

def piano_fase(u, v, x, y, a1, a2,
               system_type="negative",
               x_range=(0, 4),
               y_range=(0, 4)):

    plt.figure(figsize=(8, 6))

    if system_type == "negative":

        plt.plot(
            x,
            a2 / (1 + x**m2),
            label=r'Nullcline $\dot{y}=0$',
            color='orange',
            linewidth=2
        )

        plt.plot(
            a1 / (1 + y**m1),
            y,
            label=r'Nullcline $\dot{x}=0$',
            color='blue',
            linewidth=2
        )

        title = f"Doppio feedback negativo: $a_1$ ={a1}, $a_2$ ={a2}"

    elif system_type == "positive":

        plt.plot(
            x,
            a2 * x**m2 / (1 + x**m2),
            label=r'Nullcline $\dot{y}=0$',
            color='orange',
            linewidth=2
        )

        plt.plot(
            a1 * y**m1 / (1 + y**m1),
            y,
            label=r'Nullcline $\dot{x}=0$',
            color='blue',
            linewidth=2
        )

        title = f"Doppio feedback positivo: $a_1$ ={a1}, $a_2$ ={a2}"

    else:
        title = f"Sistema: $a_1$ ={a1}, $a_2$ ={a2}"

    plt.xlabel('x', fontsize=20)
    plt.ylabel('y', fontsize=20)

    plt.title(title, fontsize=22)

    plt.xlim(x_range)
    plt.ylim(y_range)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    plt.grid()
    plt.legend(fontsize=18)

    plt.show()


# ============================================================
# CAMPO VETTORIALE + NULLCLINE + EQUILIBRI
# ============================================================

def vector_field(X, Y, u, v, a1, a2,
                 system_type,
                 x_range=(0, 4),
                 y_range=(0, 4)):

    # ========================================================
    # NORMALIZZAZIONE CAMPO VETTORIALE
    # ========================================================

    norm = np.sqrt(u**2 + v**2)

    U_norm = u / (norm + 1e-10)
    V_norm = v / (norm + 1e-10)

    # ========================================================
    # FIGURA
    # ========================================================

    plt.figure(figsize=(8, 6))

    # ========================================================
    # CAMPO VETTORIALE
    # ========================================================

    plt.quiver(
        X,
        Y,
        U_norm,
        V_norm,
        color='gray',
        alpha=0.6
    )

    # ========================================================
    # NULLCLINE
    # ========================================================

    k = np.linspace(
        x_range[0],
        x_range[1],
        500
    )

    h = np.linspace(
        y_range[0],
        y_range[1],
        500
    )

    if system_type == "negative":

        # Nullcline dy/dt = 0
        plt.plot(
            k,
            a2 / (1 + k**m2),
            label=r'Nullcline $\dot{y}=0$',
            color='orange',
            linewidth=2
        )

        # Nullcline dx/dt = 0
        plt.plot(
            a1 / (1 + h**m1),
            h,
            label=r'Nullcline $\dot{x}=0$',
            color='blue',
            linewidth=2
        )

        title = f"Doppio feedback negativo: $a_1$ ={a1}, $a_2$ ={a2}"

    elif system_type == "positive":

        # Nullcline dy/dt = 0
        plt.plot(
            k,
            a2 * k**m2 / (1 + k**m2),
            label=r'Nullcline $\dot{y}=0$',
            color='orange',
            linewidth=2
        )

        # Nullcline dx/dt = 0
        plt.plot(
            a1 * h**m1 / (1 + h**m1),
            h,
            label=r'Nullcline $\dot{x}=0$',
            color='blue',
            linewidth=2
        )

        title = f"Doppio feedback positivo: $a_1$ ={a1}, $a_2$ ={a2}"

    else:
        title = f"Sistema: a1={a1}, a2={a2}"

    # ========================================================
    # TROVIAMO I PUNTI DI EQUILIBRIO
    # ========================================================

    equilibri = trova_equilibri(
        a1,
        a2,
        system_type,
        x_range,
        y_range
    )

    print("\nPUNTI DI EQUILIBRIO:")

    stable_points = []
    unstable_points = []
    nonhyp_points = []

    for x_eq, y_eq in equilibri:

        stability = classifica_equilibrio(
            x_eq,
            y_eq,
            a1,
            a2,
            system_type
        )

        print(
            f"  ({x_eq:.5f}, {y_eq:.5f}) -> {stability}"
        )

        if stability == "stable":

            stable_points.append(
                (x_eq, y_eq)
            )

            # clip_on=False: se il punto cade esattamente sul bordo
            # del grafico (es. l'origine), il marker non viene tagliato
            # dagli assi ma puo' "sconfinare" leggermente oltre il bordo,
            # restando comunque centrato sul vero punto di equilibrio.
            plt.scatter(
                x_eq,
                y_eq,
                s=100,
                marker='o',
                color='green',
                zorder=5,
                clip_on=False
            )

        elif stability == "unstable":

            unstable_points.append(
                (x_eq, y_eq)
            )

            plt.scatter(
                x_eq,
                y_eq,
                s=100,
                marker='o',
                color='red',
                zorder=5,
                clip_on=False
            )

        else:

            # Caso non iperbolico
            nonhyp_points.append(
                (x_eq, y_eq)
            )

            plt.scatter(
                x_eq,
                y_eq,
                s=100,
                marker='o',
                color='black',
                zorder=5,
                clip_on=False
            )

    # ========================================================
    # ETICHETTE
    # ========================================================

    plt.xlabel('x', fontsize=25)
    plt.ylabel('y', fontsize=25)

    plt.title(title, fontsize=25)

    plt.xlim(x_range)
    plt.ylim(y_range)

    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)

    plt.grid()

    # ========================================================
    # LEGENDA
    # ========================================================

    vector_legend = Line2D(
        [0],
        [0],
        color='gray',
        linewidth=2,
        label='Campo vettoriale'
    )

    stable_legend = Line2D(
        [0],
        [0],
        marker='o',
        color='w',
        markerfacecolor='green',
        markersize=10,
        label='Punto stabile'
    )

    unstable_legend = Line2D(
        [0],
        [0],
        marker='o',
        color='w',
        markerfacecolor='red',
        markersize=10,
        label='Punto instabile'
    )

    nonhyp_legend = Line2D(
        [0],
        [0],
        marker='o',
        color='w',
        markerfacecolor='black',
        markersize=10,
        label='Punto non iperbolico'
    )

    # Recuperiamo nullcline dalla legenda
    handles, labels = plt.gca().get_legend_handles_labels()

    handles.append(vector_legend)
    labels.append('Campo vettoriale')

    # Le voci "Punto stabile" / "Punto instabile" / "Punto non
    # iperbolico" compaiono in legenda solo se esiste almeno
    # un punto di quel tipo nel grafico corrente.
    # Le voci "Punto stabile" e "Punto instabile"
# compaiono solo se ci sono almeno 2 intersezioni.
    if len(equilibri) > 1:

        if stable_points:
            handles.append(stable_legend)
            labels.append('Punto stabile')

        if unstable_points:
            handles.append(unstable_legend)
            labels.append('Punto instabile')

    if nonhyp_points:
        handles.append(nonhyp_legend)
        labels.append('Punto non iperbolico')

    plt.legend(
        handles=handles,
        labels=labels,
        fontsize=19
    )

    plt.show()


# ============================================================
# MAIN
# ============================================================

def main():

    # Range del piano di fase: modificato a (0,4) in x e y
    x_range = (0, 4)
    y_range = (0, 4)

    a1 = 1
    a2 = 2

    # Griglia
    x = np.linspace(
        x_range[0],
        x_range[1],
        20
    )

    y = np.linspace(
        y_range[0],
        y_range[1],
        20
    )

    X, Y = np.meshgrid(x, y)

    # ========================================================
    # FEEDBACK NEGATIVO
    # ========================================================


    '''U, V = sistema_neg(X, Y, a1, a2)
    vector_field(
         X, Y, U, V,
         a1, a2,
         "negative",
         x_range,
         y_range
     )

    # ========================================================
    # FEEDBACK POSITIVO
    # ========================================================

    '''

    W, R = sistema_pos(X,Y,a1,a2)

    vector_field(
        X,
        Y,
        W,
        R,
        a1,
        a2,
        "positive",
        x_range,
        y_range
    )
    
    


# ============================================================
# ESECUZIONE
# ============================================================

if __name__ == "__main__":
    main()