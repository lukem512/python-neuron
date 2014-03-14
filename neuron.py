#!/bin/python

class neuron:
  # ctor
  def __init__(self, V):
    self.V = V

  # excite the neuron
  def excite(self, t_m, E_L, V_reset, V_th, R_m, I_e, DT):
    # dV/dt = 1/t_m (E_L - V + R_m . I_e)
    dV =  DT * (1/t_m * (E_L - self.V + (R_m * I_e)))
    self.V = self.V + dV

    # if V > V_th then V = V_reset
    if self.V > V_th:
      self.V = V_reset

    print self.V
       

def main():
  t_m = 10.0       # ms
  E_L = -70.0      # mV
  V_reset = -70.0  # mV
  V_th = -40.0     # mV
  R_m = 10.0       # Mohm
  I_e = 3.1        # nA
  DT = 1.0         # ms
  
  ### Part 1 ###
  n1 = neuron(V_reset)

  # simulate for 1s
  T = 0
  while T < 100:
    n1.excite(t_m, E_L, V_reset, V_th, R_m, I_e, DT)
    T = T + DT
  

if __name__ == "__main__":
    main()
