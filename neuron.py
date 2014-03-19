#!/bin/python
# An Integrate and Fire model of a neuron
# Luke Mitchell, 2014

import numpy as np
import matplotlib.pyplot as plt
import random
import math

############################
###                      ###
### Global variables     ###
###                      ###
############################   


# The global time in ms
T = 0


############################
###                      ###
### Model Neuron         ###
###                      ###
############################   


class neuron:
  # ctor
  def __init__(self, V_initial, t_m, E_L, V_reset, V_th, R_m, I_e):
    self.t_m = t_m
    self.E_L = E_L
    self.V_reset = V_reset
    self.V_th = V_th
    self.R_m = R_m
    self.I_e = I_e
    self.outgoing_synapse = None
    self.incoming_synapse = None
    self.reset(V_initial)

  # reset the voltage
  def reset(self, V):
    self.V = V

  # add synapse connection
  def add_outgoing_synapse(self, synapse):
    self.outgoing_synapse = synapse

  def add_incoming_synapse(self, synapse):
    self.incoming_synapse = synapse

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

  # excite the neuron
  def synaptic_excite(self, R_mI_e, dT):
    if self.incoming_synapse == None:
      print ("No incoming synapse found. Reverting to stand-alone excite")
      return self.excite(dT)

    R_mG_s = self.incoming_synapse.conductance()
    t_s = self.incoming_synapse.constant()
    E_s = self.incoming_synapse.equilib()
    P_s = self.incoming_synapse.prob()

    dV = ((self.E_L - self.V - ((P_s * R_mG_s) * (self.V - E_s)) + (R_mI_e)) / self.t_m) * dT
    self.V = self.V + dV

    # reached action potential?
    fired = False
    if self.V > self.V_th:
      fired = True
      global T
      self.outgoing_synapse.set_fired(T)
      self.V = self.V_reset

    return self.V, fired


############################
###                      ###
### Model Synapse        ###
###                      ###
############################    


class synapse:
  #ctor
  def __init__(self, R_mG_s, P_max, t_s, E_s):
    self.R_mG_s = R_mG_s # conductance of synapse (synaptic weight)
    self.P_max = P_max
    self.t_s = t_s
    self.E_s = E_s # equilibrium potential
    self.T_f = 0;  # when did the presynaptic neuron last fire?

  # functions to return properties of the synapse
  def prob(self):
    global T
    return self.P_max * math.exp(-1 * ((T - self.T_f) / self.t_s))

  def conductance(self):
    return self.R_mG_s

  def constant(self):
    return self.t_s

  def equilib(self):
    return self.E_s

  def set_fired(self, T_f):
    self.T_f = T_f

  # connect it to two neurons
  def connect(self, presynaptic_neuron, postsynaptic_neuron):
    if presynaptic_neuron == postsynaptic_neuron:
      print ("Error: a synapse cannot connect a neuron to itself")
    else:
      presynaptic_neuron.add_outgoing_synapse(self)
      postsynaptic_neuron.add_incoming_synapse(self)


############################
###                      ###
### Main Assignment Code ###
###                      ###
############################

def main():
  t_m = 10.0       # ms
  E_L = -70.0      # mV
  V_reset = -70.0  # mV
  V_th = -40.0     # mV
  R_m = 10.0       # Mohm
  I_e = 3.1        # nA
  dT = 1.0         # ms

  # global instance of time
  global T
  
  # instantiate a neuron
  n1 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e)

  ### Part 1 ###
  # simulate for 1s
  print ("Part 1.")

  times = []
  voltages = []

  T = 0
  while T < 1000:
    V, fired = n1.excite(dT)
    times.append(T)
    voltages.append(V)
    T = T + dT
    
  plt.figure(1)
  plt.xlabel('Time (mS)')
  plt.ylabel('Voltage (mV)')
  plt.title('Integrate and Fire Simulation of a Single Neuron')
  plt.plot(times, voltages, 'b')
  plt.show()

  ### Part 2 ###
  # determine the minimum Ie required to reach AP
  print ("Part 2.")
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
  times = []
  voltages = []
  
  I_e = I_e_cur
  n3 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e)
  T = 0
  while T < 1000:
    V, fired = n3.excite(dT)
    T = T + dT
    times.append(T)
    voltages.append(V)
    T = T + dT
    
  plt.figure(2)
  plt.xlabel('Time (mS)')
  plt.ylabel('Voltage (mV)')
  plt.title('Integrate and Fire Simulation of a Single Neuron with Injected Current 3.0 nA')
  plt.plot(times, voltages, 'b')
  plt.show()

  ### Part 3 ###
  # simulate for different current values
  # determine the firing rate
  print ("Part 3.")

  currents = []
  firing_rates = []

  for I_e in np.arange(2.0, 5.1, 0.1):
    n4 = neuron(V_reset, t_m, E_L, V_reset, V_th, R_m, I_e)
    T = 0
    ap_count = 0
    while T < 1000:
      V, fired = n4.excite(dT)
      if fired == True:
        ap_count = ap_count + 1
      T = T + dT
    currents.append(I_e)
    firing_rates.append(ap_count)
    
  plt.figure(3)
  plt.xlabel('Injected Current (nA)')
  plt.ylabel('Firing Rate (Hz)')
  plt.title('Comparison of Neuron Firing Rates for Varying Injected Currents')
  plt.plot(currents, firing_rates, 'b')
  plt.show()

  ### Part 4 ###
  # simulate two neurons, connected by a synapse
  t_m = 20.0       # ms
  E_L = -70.0      # mV
  V_reset = -80.0  # mV
  V_th = -54.0     # mV
  dT = 1.0         # ms  

  R_mG_s = 0.15
  R_mI_e = 18.0 #mV
  P_max = 0.5
  t_s = 10.0

  # a) excitatory
  print ("Part 4. (a)")
  E_s = 0.0 # mV

  V5 = random.uniform(V_reset, V_th)
  V6 = random.uniform(V_reset, V_th)
  n5 = neuron(V5, t_m, E_L, V_reset, V_th, R_m, I_e)
  n6 = neuron(V6, t_m, E_L, V_reset, V_th, R_m, I_e)

  s1 = synapse(R_mG_s, P_max, t_s, E_s)
  s1.connect(n5, n6)
  s2 = synapse(R_mG_s, P_max, t_s, E_s)
  s2.connect(n6, n5)
  
  # simulate for 1s
  # simulate the two neurons with a synapse
  times = []
  voltages_a = []
  voltages_b = []

  T = 0
  while T < 1000:
    times.append(T)
    V, fired = n5.synaptic_excite(R_mI_e, dT)
    voltages_a.append(V)
    V, fired = n6.synaptic_excite(R_mI_e, dT)
    voltages_b.append(V)
    T = T + dT
    
  plt.figure(4)
  plt.xlabel('Time (mS)')
  plt.ylabel('Voltage (mV)')
  plt.title('Excitatory Synapse with Equilibrium Potential 0.0')
  plt.plot(times, voltages_a, 'b')
  plt.plot(times, voltages_b, 'r')
  plt.show()
  
  # b) inhibitory
  print ("Part 4. (b)")

  E_s = -80.0 # mV

  V7 = random.uniform(V_reset, V_th)
  V8 = random.uniform(V_reset, V_th)
  n7 = neuron(V5, t_m, E_L, V_reset, V_th, R_m, I_e)
  n8 = neuron(V6, t_m, E_L, V_reset, V_th, R_m, I_e)

  s3 = synapse(R_mG_s, P_max, t_s, E_s)
  s3.connect(n7, n8)
  s4 = synapse(R_mG_s, P_max, t_s, E_s)
  s4.connect(n8, n7)
  
  # simulate for 1s
  # simulate the two neurons with a synapse
  times = []
  voltages_a = []
  voltages_b = []

  T = 0
  while T < 1000:
    times.append(T)
    V, fired = n7.synaptic_excite(R_mI_e, dT)
    voltages_a.append(V)
    V, fired = n8.synaptic_excite(R_mI_e, dT)
    voltages_b.append(V)
    T = T + dT
    
  plt.figure(5)
  plt.xlabel('Time (mS)')
  plt.ylabel('Voltage (mV)')
  plt.title('Excitatory Synapse with Equilibrium Potential -80.0')
  plt.plot(times, voltages_a, 'b')
  plt.plot(times, voltages_b, 'r')
  plt.show()

if __name__ == "__main__":
    main()
