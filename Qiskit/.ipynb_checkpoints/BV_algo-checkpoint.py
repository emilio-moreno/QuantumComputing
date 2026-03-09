# %% Imports
import qiskit
import random
import matplotlib.pyplot as plt

# %% Functions

def bv_circuit_init(n):
    qcircuit = qiskit.QuantumCircuit(n + 1)
    
    for i in range(n):
        qcircuit.h(i)
    
    qcircuit.x(n)
    qcircuit.h(n)
    qcircuit.barrier()
        
    return qcircuit

def bv_oracle(s):
    n = len(s)
    s = s[::-1]
    
    qcircuit = qiskit.QuantumCircuit(n + 1)
    
    for i, bit in enumerate(s):
        if bit == "1":
            qcircuit.cx(i, n)
            
    qcircuit.barrier()
    
    return qcircuit

def bv_circuit_end(n):
    qcircuit = qiskit.QuantumCircuit(n + 1, n)
    
    for i in range(n):
        qcircuit.h(i)
    
    qcircuit.measure(range(n), range(n))
    
    return qcircuit

# %% Circuit
n = 4
bits = ["0", "1"]
choices = random.choices(bits, k=n)
s = "".join(choices)

bv_circuit = bv_circuit_init(n)
bv_circuit = bv_circuit.compose(bv_oracle(s))
bv_circuit = bv_circuit.compose(bv_circuit_end(n))

fig = bv_circuit.draw(output='mpl')

plt.figure(fig)
# %% Simulation
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator

backend = AerSimulator(method='statevector')
shots = 1000
counts = backend.run(bv_circuit, shots=shots).result().get_counts()

fig = plot_histogram(counts)
plt.figure(fig)
print("")
#%%
print(s)
