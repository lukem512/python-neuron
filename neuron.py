#!/bin/python
# An Integrate and Fire model of a neuron
# Luke Mitchell, 2014

import numpy as np

class neuron:
  # ctor
  def __init__(self, V_initial, t_m, E_L, V_reset, V_th, R_m, I_e):
    self.t_m = t_m
    self.E_L = E_L
    self.V_reset = V_reset
    self.V_th = V_th
    self.R_m = R_m
    self.I_e = I_e
    self.reset(V_initial)

  # reset the voltage
  def reset(self, V):
    self.V = V

  # excite the neuron
  def excite(self, dT):
    dV =  dT * (1/self.t_m * (self.E_L - self.V + (self.R_m * self.I_e)))
    self.V = self.V + dV

    # reached action potential?
    fired = False
    if self.V > self.V_th:
      fired = True
      self.V = self.V_reset

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
  n1 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e)

  ### Part 1 ###
  # simulate for 1s
  T = 0
  while T < 1000:
    V, fired = n1.excite(dT)
    print ("(" + str(T) + "," + str(V) + ")")
    T = T + dT

  ### Part 2 ###
  # determine the minimum Ie required to reach AP
  I_e_cur = (V_th - E_L) / R_m

  # print
  print ("[Analytical] Action Potentials will occur when Ie > " + str(I_e_cur))

  # this can also be done numerically using the following code
  I_e_cur = I_e
  found = False
  while I_e_cur > 0 and found == False:
    # simulate for 1s
    n2 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e_cur)
    T = 0
    fired = False
    while T < 1000 and fired == False:
      V, fired = n2.excite(dT)
      T = T + dT

  # reached AP?
    if fired == False:
      found = True
    else:
      # reduce Ie
      I_e_cur = I_e_cur - 0.0001

  # print
  print ("[Numerical] Action Potentials will occur when Ie > " + str(I_e_cur))

  # simulate for 1s just under this value
  I_e = I_e_cur - 0.1
  n3 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e)
  T = 0
  while T < 1000:
    V, fired = n3.excite(dT)
    #print ("(" + str(T) + "," + str(V) + ")")
    T = T + dT

  ### Part 3 ###
  # simulate for different current values
  # determine the firing rate
  for I_e in np.arange(2.0, 5.1, 0.1):
    n4 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e)
    T = 0
    ap_count = 0
    while T < 1000:
      V, fired = n4.excite(dT)
      if fired == True:
        ap_count = ap_count + 1
      T = T + dT
    print ("(" + str(I_e) + "," + str(ap_count) + ")")

if __name__ == "__main__":
    main()
