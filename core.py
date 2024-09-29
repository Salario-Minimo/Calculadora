import streamlit as st

class Core:

  
  def __init__(self):
    
    self.datos = []

    st.header("Calculadora")
    st.radio("¿Qué figura vas a analizar?", ("Placa", "Cilindro", "Esfera", "Medio semi-infinito"), horizontal=True)
    
    


Core()
