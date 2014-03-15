#!/bin/python
# An Integrate and Fire model of a neuron
# Luke Mitchell, 2014

class neuron:
  # ctor
  def __init__(self, V):
    self.V = V

  # excite the neuron
  def excite(self, t_m, E_L, V_reset, V_th, R_m, I_e, dT):
    dV =  dT * (1/t_m * (E_L - self.V + (R_m * I_e)))
    self.V = self.V + dV

    # reached action potential?
    fired = False
    if self.V > V_th:
      fired = True
      self.V = V_reset

    return self.V, fired
       

def main():
  t_m = 10.0       # ms
  E_L = -70.0      # mV
  V_reset = -70.0  # mV
  V_th = -40.0     # mV
  R_m = 10.0       # Mohm
  I_e = 3.1        # nA
  dT = 1.0         # ms
  
  # instantiate a neuron
  n1 = neuron(V_reset)

  ### Part 1 ###
  # simulate for 1s
  T = 0
  while T < 1000:
    V, fired = n1.excite(t_m, E_L, V_reset, V_th, R_m, I_e, dT)
    # print ("(" + str(T) + "," + str(V) + ")")
    T = T + dT

  ### Part 2 ###
  # determine the minimum Ie required to reach AP
  I_e_cur = I_e
  found = False
  while I_e_cur > 0 and found == False:
    # simulate for 1s
    T = 0
    fired = False
    while T < 1000 and fired == False:
      V, fired = n1.excite(t_m, E_L, V_reset, V_th, R_m, I_e_cur, dT)
      T = T + dT

    # reached AP?
    if fired == False:
      found = True
    else:
      # reduce Ie
      I_e_cur = I_e_cur - 0.0001

  # minimum value
  print (I_e_cur)

  # simulate for 1s just under this value
  I_e = I_e_cur - 0.1
  T = 0
  while T < 1000:
    V, fired = n1.excite(t_m, E_L, V_reset, V_th, R_m, I_e, dT)
    # print ("(" + str(T) + "," + str(V) + ")")
    T = T + dT

if __name__ == "__main__":
    main()
