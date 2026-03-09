# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 21:15:30 2026

@author: Emilio Moreno
"""

#%% [markdown] Imports
import pennylane as qml
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

colors = cm.gray

#%% [markdown] Rotations
device = qml.device('default.qubit', wires=1)

@qml.qnode(device)
def RZ(theta):
    qml.RZ(theta, wires=0)
    
    return qml.expval(qml.Z(wires=0))

@qml.qnode(device)
def RY(theta):
    qml.RY(theta, wires=0)
    
    return qml.expval(qml.Z(wires=0))

#%% [markdown] Expected values
theta = np.linspace(0, 2*np.pi, 10**4)
fig, ax = plt.subplots()
ax.set(xlabel="$\\theta$", ylabel="")
ax.plot(theta, RZ(theta), label=r"$\langle \psi | Z | \psi \rangle$",
        color=colors(0.25), ls='--')
ax.plot(theta, RY(theta), label=r"$\langle \phi | Z | \phi \rangle$",
        color=colors(0.75))
plt.legend()
plt.show()