# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 19:22:13 2026

DJ Algorithm
"""
#%% Imports
import qiskit
import random
import matplotlib.pyplot as plt
from qiskit_aer import AerSimulator

backend = AerSimulator(method="statevector")

plt.rcParams.update({"font.family": "Times New Roman", "mathtext.fontset": "cm"})

#%% Functions
def prepare_states(N, x: str):
    qcircuit = qiskit.QuantumCircuit(N + 1)
    for i, xi in enumerate(x):
        if xi == "1": qcircuit.x(i)
    qcircuit.barrier()
    return qcircuit

def measure_N(N):
    qcircuit = qiskit.QuantumCircuit(N + 1, 1)
    qcircuit.measure(N, 0)
    return qcircuit

def DJ_init(N):
    qcircuit = qiskit.QuantumCircuit(N + 1)
    
    qcircuit.x(N)
    for i in range(N + 1): qcircuit.h(i)
    qcircuit.barrier()
    return qcircuit

def DJ_finish(N):
    qcircuit = qiskit.QuantumCircuit(N + 1, N)
    for i in range(N): qcircuit.h(i)
    qcircuit.measure(range(N), range(N))
    return qcircuit

def projector(N, j):
    qcircuit = qiskit.QuantumCircuit(N + 1)
    qcircuit.cx(j, N)
    qcircuit.barrier()
    return qcircuit

def self_dot_product(N):
    qcircuit = qiskit.QuantumCircuit(N + 1)
    for i in range(N): qcircuit.cx(i, N)
    qcircuit.barrier()
    return qcircuit

def CNOT_function(N, k, i):
    qcircuit = qiskit.QuantumCircuit(N + 1)
    qcircuit.cx(k, N)
    qcircuit.cx(i, N)
    qcircuit.barrier()
    return qcircuit


#%% Project
a, b = 2, 10
N = random.choice(range(a, b))
j = random.choice(range(N))
DJ = DJ_init(N).compose(projector(N, j).compose(DJ_finish(N)))
fig = plt.figure(DJ.draw(output='mpl'))

# Simulationion function
shots = 1000
counts = backend.run(DJ, shots=shots).result().get_counts()
func_name = f"Projector Function: $f_{j}:\\{{0, 1\\}}^{N}"
func_name += "\\rightarrow \\{{0, 1\\}}$"
fig.suptitle(f"{func_name}\nCounts (out of {shots}) = {counts}",
             fontsize=20)

#%% Self dot product function
a, b = 2, 10
N = random.choice(range(a, b))
j = random.choice(range(N))
DJ = DJ_init(N).compose(self_dot_product(N).compose(DJ_finish(N)))
fig = plt.figure(DJ.draw(output='mpl'))

# Simulation
shots = 1000
counts = backend.run(DJ, shots=shots).result().get_counts()
func_name = f"Self-dot product Function: $g:\\{{0, 1\\}}^{N}$"
func_name += "$\\rightarrow \\{{0, 1\\}}$"
fig.suptitle(f"{func_name}\nCounts (out of {shots}) = {counts}",
             fontsize=20)

#%% CNOT function
a, b = 2, 10
N = random.choice(range(a, b))
k = random.choice(range(N))
i = random.choice(range(N))
DJ = DJ_init(N).compose(CNOT_function(N, k, i).compose(DJ_finish(N)))
fig = plt.figure(DJ.draw(output='mpl'))

# Simulation
shots = 1000
counts = backend.run(DJ, shots=shots).result().get_counts()
func_name = f"CNOT Function: $h_{{{k}{i}}}:\\{{0, 1\\}}^{N}"
func_name += "\\rightarrow \\{{0, 1\\}}$"
fig.suptitle(f"{func_name}\nCounts (out of {shots}) = {counts}",
             fontsize=20)

#%% Self dot product function test
x = "101111"
N = len(x)
# 
qcircuit = prepare_states(N, x).compose(self_dot_product(N).compose(measure_N(N)))
fig = plt.figure(qcircuit.draw(output='mpl'))

shots = 1000
counts = backend.run(qcircuit, shots=shots).result().get_counts()
fig.suptitle(f"Counts (out of {shots}) = {counts}",
             fontsize=20)