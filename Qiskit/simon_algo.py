# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 20:46:32 2026

@author: Emilio Moreno
"""
#%% Imports
import matplotlib.pyplot as plt
import numpy as np
import random
from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
backend = AerSimulator(method='statevector')


#%% Functions

def get_simon_oracle(maximum_integer, secret_period, offset=0):
    '''Generates a periodic oracle. This may be broken.'''
    binary_str = format(maximum_integer, 'b')
    if '0' in format(maximum_integer - 1, 'b'):
        raise ValueError('maximum_integer must be a power of 2.')
    nbits = len(binary_str) - 1
    
    function_values = []
    for x in range(maximum_integer):
        function_values.append(
            (format((x + offset) % maximum_integer,
                    f'0{nbits}b'),
             format((x % secret_period + offset) % maximum_integer,
                    f'0{nbits}b')))
    
    oracle_table = []
    for y in range(maximum_integer):
        for x, f_x in function_values:
            input_ = x + format(y, f'0{nbits}b')
            output = y ^ int(f_x, 2)
            output = format(output, f'0{nbits}b')
            output = x + output
            oracle_table.append((input_, output))
    
    oracle_matrix = np.zeros((maximum_integer**2, maximum_integer**2))
    for input_, output in oracle_table:
        oracle_matrix[int(output, 2), int(input_, 2)] = 1
    
    gate = UnitaryGate(oracle_matrix, label='$U_f$')
    return gate


def simon_init(n):
    qc = QuantumCircuit(2*n)
    
    for i in range(n, 2*n):
        qc.h(i)
        
    qc.barrier()
    
    return qc


def simon_final(n):
    qc = QuantumCircuit(2*n, n)
    
    for i in range(n, 2*n):
        qc.h(i)
        
    qc.measure(range(n, 2*n), range(n))

    return qc

def prepare_states(n, x: str):
    qcircuit = QuantumCircuit(n)
    x = reversed(x)
    for i, xi in enumerate(x):
        if xi == "1": qcircuit.x(i)
    
    qcircuit.barrier()
    
    return qcircuit

def oracle(n, s):
    qc = QuantumCircuit(2*n)
    for i in range(n):
        qc.cx(n + i, i)
    
    reverse_s = s[::-1]
    flag_bit = reverse_s.find("1")
    
    if flag_bit != -1:
        for i in range(n):
            if reverse_s[i] == '1':
                qc.cx(2 * n - (flag_bit + 1), i)

    qc.barrier()
        
    return qc

def measure_all(n):
    qc = QuantumCircuit(2*n, 2*n)
    qc.measure(range(2*n), range(2*n))
    
    return qc

#%% Oracle circuit
nbits = 5
s = "".join(random.choices(["0", "1"], k=nbits))
init_state = '001000'
oracle_circuit = prepare_states(2*nbits, init_state).compose(
    oracle(nbits, s)).compose(
        measure_all(nbits))
fig = plt.figure(oracle_circuit.draw(output='mpl'))

counts = backend.run(oracle_circuit, shots=10000).result().get_counts()
fig.suptitle(f"{counts = }")
plt.show()

#%% Circuit
simon_circuit = simon_init(nbits).compose(
    oracle(nbits, s).compose(
    simon_final(nbits)))
fig = simon_circuit.draw(output='mpl')
fig = plt.figure(fig)
plt.show()

#%% Simulation
counts = backend.run(simon_circuit, shots=100000).result().get_counts()
figure = plt.figure(plot_histogram(counts))
plt.show()