import streamlit as st

class Core:

  def base_gui(self):
    iterable = ("Diametro", "Conductividad", "Difusividad", "Temperatura inicial", "Temperatura ambiente", "Coeficiente de transferencia",
                "Densidad", "Calor específico", "Distancia del centro", "Tiempo")
    datos = []

    for x in iterable:
      datos.append(st.number_input(x))
    print(datos)
      
  
  def __init__(self):
    
    self.datos = []

    st.header("Calculadora")
    st.radio("¿Qué figura vas a analizar?", ("Placa", "Cilindro", "Esfera", "Medio semi-infinito"), horizontal=True)
    self.base_gui()
    
    
    


Core()
