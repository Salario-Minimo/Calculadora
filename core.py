import streamlit as st
import numpy as np
from scipy.special import jv
from scipy.optimize import fsolve

class Core:

  def base_gui(self):
    iterable = ("Diametro", "Conductividad", "Difusividad", "Temperatura inicial", "Temperatura ambiente", "Coeficiente de transferencia",
                "Densidad", "Calor especifico", "Distancia del centro", "Tiempo")
    datos = []

    if not st.toggle("Solver"):
      for x in iterable:
        datos.append(float(st.text_input(x, value="0")))
      if st.button("Calcular"):
        self.selector[self.figura](*datos)
        
    else:
      temp = iterable
      selección = st.selectbox("¿Qué variable buscas?",iterable)

      for x in temp:
        datos.append(float(st.text_input(x, value="0")))

      if st.button("Calcular"):
        "uwu"
      
      st.write(iterable.index(selección))
      st.write("uwu")

      
  
  def __init__(self):
    
    self.datos = []
    self.selector = {"Placa":self.placa, "Esfera":self.esfera, "Cilindro":self.cilindro}

    st.header("Calculadora")
    self.figura = st.radio("¿Qué figura vas a analizar?", ("Placa", "Cilindro", "Esfera", "Medio semi-infinito"), horizontal=True)
    self.base_gui()
    
  def placa(self, Espesor, Conductividad, Difusividad, T_inicial, T_ambiente, Coeficiente_transferencia, Densidad, Calor_especifico, Distancia, Tiempo):
    
    Longitud_caracteristica = Espesor / 2
    Distancia_adimensional = Distancia / Longitud_caracteristica
    Tiempo_adimensional = (Difusividad * Tiempo) / Longitud_caracteristica**2
    Numero_biot = (Coeficiente_transferencia * Longitud_caracteristica) / Conductividad
    
    Lambdas = [1,1,1]
    
    for n in range(3):
      Lambda_temp = 1
      while True:
        Lambda_final = np.arctan(Numero_biot/Lambda_temp) + np.pi*n
        if np.around(Lambda_temp, decimals=12) == np.around(Lambda_final, decimals=12):
          break
        else:
          Lambda_temp = Lambda_final
      Lambdas[n] = Lambda_final
    
    theta_temp = []
    calor_temp = []
    for n in Lambdas:
      a = (4*np.sin(n))/(2*n + np.sin(2*n))
      b = np.exp(- n**2 * Tiempo_adimensional)
      c = np.cos(n*Distancia_adimensional)
      Calor = a*b * (np.sin(n)/n)
      theta_temp.append(a*b*c)
      calor_temp.append(Calor)
    
    Theta = np.sum(theta_temp)
    Calor = np.sum(calor_temp)
    
    Temperatura_final = Theta * (T_inicial - T_ambiente) + T_ambiente

    Calor_maximo = Densidad * (Espesor * Calor_especifico * (T_ambiente - T_inicial))
    Calor_final = (1 - Calor) * Calor_maximo
    
    st.write("Temperatura_final:", Temperatura_final, "°C")
    st.write("Calor_final:", Calor_final, "J")

    return (Temperatura_final, Calor_final)

  def esfera(self, Diametro, Conductividad, Difusividad, T_inicial, T_ambiente, Coeficiente_transferencia, Densidad, Calor_especifico, Distancia, Tiempo):
    Longitud_caracteristica = Diametro / 2
    Distancia_adimensional = Distancia / Longitud_caracteristica
    Tiempo_adimensional = (Difusividad * Tiempo) / Longitud_caracteristica**2
    Numero_biot = (Coeficiente_transferencia * Longitud_caracteristica) / Conductividad
    
    Lambdas = [1,1,1]
    
    for n in range(3):
      Lambda_temp = 1
      while True:
        Lambda_final = ((np.pi/2) - np.arctan((1-Numero_biot)/Lambda_temp)) + np.pi*n
        if np.around(Lambda_temp, decimals=12) == np.around(Lambda_final, decimals=12):
          break
        else:
          Lambda_temp = Lambda_final
      Lambdas[n] = Lambda_final
    
    theta_temp = []
    calor_temp = []
    for n in Lambdas:
      a = (4*(np.sin(n) - n*np.cos(n)))/(2*n - np.sin(2*n))
      b = np.exp(- n**2 * Tiempo_adimensional)
      c = np.sin(n*Distancia_adimensional)/(n*Distancia_adimensional)
      Calor = 3*a*b*((np.sin(n)-n*np.cos(n))/n**3)
      theta_temp.append(a*b*c)
      calor_temp.append(Calor)
    
    Theta = np.sum(theta_temp)
    Calor = np.sum(calor_temp)
    
    Temperatura_final = Theta * (T_inicial - T_ambiente) + T_ambiente
    print(Temperatura_final)
    
    Calor_maximo = Densidad * ((4/3)*np.pi*(Diametro/2)**3) * Calor_especifico * (T_ambiente - T_inicial)
    Calor_final = (1 - Calor) * Calor_maximo
  
    st.write("Temperatura_final:", Temperatura_final, "°C")
    st.write("Calor_final", Calor_final, "J")

    return (Temperatura_final, Calor_final)
    
  
  def cilindro(self, Diametro, Conductividad, Difusividad, T_inicial, T_ambiente, Coeficiente_transferencia, Densidad, Calor_especifico, Distancia, Tiempo):

    Longitud_caracteristica = Diametro / 2
    Distancia_adimensional = Distancia / Longitud_caracteristica
    Tiempo_adimensional = (Difusividad * Tiempo) / Longitud_caracteristica**2
    Numero_biot = (Coeficiente_transferencia * Longitud_caracteristica) / Conductividad
    
    Lambdas = [1,4,7]
    
    for n in range(3):
      Lambda_temp = Lambdas[n]
      while True:
        Lambda_final = Lambda_temp - (Lambda_temp*jv(1, Lambda_temp) - Numero_biot*jv(0, Lambda_temp))/(Lambda_temp*jv(0, Lambda_temp) + Numero_biot*jv(1, Lambda_temp))
        if np.around(Lambda_temp, decimals=12) == np.around(Lambda_final, decimals=12):
          break
        else:
          Lambda_temp = Lambda_final
      Lambdas[n] = Lambda_final
    
    theta_temp = []
    calor_temp = []
    for n in Lambdas:
      a = (2/n) * (jv(1,n) / (jv(0,n)**2 + jv(1,n)**2))
      b = np.exp(- n**2 * Tiempo_adimensional)
      c = jv(0, n*Distancia_adimensional)
      Calor = 2*a*b*(jv(1,n)/n)
      theta_temp.append(a*b*c)
      calor_temp.append(Calor)
    
    Theta = np.sum(theta_temp)
    Calor = np.sum(calor_temp)
    
    Temperatura_final = Theta * (T_inicial - T_ambiente) + T_ambiente
    Calor_maximo = Densidad * (np.pi*(Longitud_caracteristica)**2) * Calor_especifico * (T_ambiente - T_inicial)
    
    Calor_final = (1 - Calor) * Calor_maximo
    
    st.write("Temperatura_final:", Temperatura_final, "°C")
    st.write("Calor_final", Calor_final, "J")

    return (Temperatura_final, Calor_final)

  def solver(self):
    

  def funcion_error(self):
    return
    
Core()
