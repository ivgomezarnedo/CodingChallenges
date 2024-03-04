# Importamos las librerías necesarias
import matplotlib.pyplot as plt

# Creamos una lista con los valores de "N_Dobles" en los datos proporcionados
n_doubles = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Creamos una lista con los valores de "N_Triples" en los datos proporcionados
n_triples = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Creamos una lista con los valores de "Expected_Value" en los datos proporcionados
values = [3.56, 10.22, 26.58, 69.94, 177.41, 430.79, 1023.72, 2195.26, 3893.73, 3979.95]

# Creamos el diagrama de dispersión
plt.scatter(n_doubles, n_triples)

# Agregamos etiquetas con los valores de "Expected_Value" a cada punto en el diagrama
for i in range(len(n_doubles)):
    plt.annotate(values[i], (n_doubles[i], n_triples[i]))

# Agregamos título y etiquetas a los ejes
plt.title("Expected value for different values of N_Dobles and N_Triples")
plt.xlabel("Values of N_Dobles")
plt.ylabel("Values of N_Triples")

# Mostramos el diagrama de dispersión
plt.show()
