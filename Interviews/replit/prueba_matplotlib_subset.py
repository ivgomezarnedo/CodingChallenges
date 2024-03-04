import matplotlib.pyplot as plt

# Creamos una lista con los valores de "N_Dobles" y "N_Triples"
# en los datos proporcionados
#categories = [(0, 0), (0, 1), (0, 2), (0, 3)]
categories = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(8,0),(8,1),(8,2),(8,3),(8,4),(9,0),(9,1),(9,2),(9,3),(10,0),(10,1),(10,2),(10,3),(11,0),(11,1),(11,2),(12,0),(12,1),(13,0),(13,1),(14,0)]
values = [3.56,10.22,26.58,69.94,177.41,430.79,1023.72,2195.26,3893.73,3979.95,6.9,19.13,49.64,127.47,319.99,771.98,1638.82,3281.04,4288.26,12.92,35.0,90.6,230.38,552.51,1248.14,2486.44,3951.68,2481.62,23.64,63.46,163.99,399.06,897.89,1923.37,3110.99,3351.31,42.87,115.0,284.79,652.01,1394.59,2498.33,2972.65,77.72,200.08,467.28,1020.98,1844.84,2642.24,-592.73,135.27,329.3,736.37,1375.7,2040.23,545.89,222.81,521.29,1006.2,1587.43,760.19,-5799.14,353.12,719.37,1197.2,831.53,-3312.51,488.5,873.91,753.11,-1749.92,596.48,610.56,-885.22,-10277.29,426.76,-436.36,-6518.16,-263.38,-4162.77,-2743.53,-12360.56,-8206.38]

real_categories = []
real_values = []
for i in range(len(categories)):
    if i%6 == 0:
        real_categories.append(categories[i])
        real_values.append(values[i])

categories_str = [str(category) for category in real_categories]

# Creamos una lista con los valores de "Expected_Value" en los datos proporcionados
#values = [3.56, 10.22, 26.58, 69.94]

# For each bar in the bar chart, we add a text annotation with the value above it
for i in range(len(real_categories)):
    plt.annotate(real_values[i], (i, real_values[i]))


# Creamos el diagrama de barras
plt.bar(categories_str, real_values)

# Agregamos título y etiquetas a los ejes
plt.title("Expected value for different values of N_Dobles and N_Triples")
plt.xlabel("Values of N_Dobles and N_Triples")
plt.ylabel("Expected value (€)")



#plt.xticks(categories, ["(0, 0)", "(0, 1)", "(0, 2)", "(0, 3)"])


# Mostramos el diagrama de barras
plt.show()