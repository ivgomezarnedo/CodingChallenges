import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Datos a representar
N_Dobles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
N_Triples = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Price = [0.75, 2.25, 6.75, 20.25, 60.75, 182.25, 546.75, 1640.25, 4920.75, 14762.25]
Expected_Value = [3.56, 10.22, 26.58, 69.94, 177.41, 430.79, 1023.72, 2195.26, 3893.73, 3979.95]

# Crear figura y ejes
fig = plt.figure()
ax = Axes3D(fig)

# Añadir datos al gráfico
ax.scatter(N_Dobles, N_Triples, Price, c=Expected_Value, cmap='RdYlBu')

# Añadir etiquetas a los ejes
ax.set_xlabel('N_Dobles')
ax.set_ylabel('N_Triples')
ax.set_zlabel('Price')

# Mostrar gráfico
plt.show()