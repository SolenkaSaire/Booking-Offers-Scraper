import pandas as pd
import matplotlib.pyplot as plt

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv('src/data/hotels_data.csv')

# Convertir la columna 'Precio' a un valor numérico
df['Precio'] = df['Precio'].str.replace('COP ', '').str.replace('.', '').astype(float)

# Ordenar el DataFrame por precio
df_sorted = df.sort_values(by='Precio')

# Generar el gráfico de barras
plt.figure(figsize=(10, 8))
plt.barh(df_sorted['Hotel'], df_sorted['Precio'], color='skyblue')
plt.xlabel('Precio (COP)')
plt.ylabel('Hotel')
plt.title('Alojamientos por Localización del Más Barato al Más Caro')
plt.tight_layout()

# Mostrar el gráfico
plt.show()