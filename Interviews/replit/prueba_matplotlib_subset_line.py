import matplotlib.pyplot as plt

# Datos a representar
N_Triples = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
Price = [0.75, 2.25, 6.75, 20.25, 60.75, 182.25, 546.75, 1640.25, 4920.75, 14762.25]
Expected_Value = [3.56, 10.22, 26.58, 69.94, 177.41, 430.79, 1023.72, 2195.26, 3893.73, 3979.95]

# Crear figura y ejes
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Añadir líneas al gráfico
ax.plot(N_Triples, Price, label='Price')
ax.plot(N_Triples, Expected_Value, label='Expected_Value')

# Añadir etiquetas a los ejes y leyenda
ax.set_xlabel('N_Triples')
ax.set_ylabel('Valor')
ax.legend()

# Mostrar gráfico
plt.show()