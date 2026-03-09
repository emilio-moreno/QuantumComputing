# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 21:15:30 2026

@author: Emilio Moreno
"""

# %% Imports
import pennylane as qml
import matplotlib.patches as patches
import numpy as np

# %%
N = 3
device = qml.device('default.qubit', N)

@qml.qnode(device)
def circuit(theta, phi):
    qml.X(N - 1)
    for i in range(N): qml.H(i)
    qml.Barrier()
    
    qml.SWAP(wires=[0, 2])
    qml.CRY(theta, wires=[0, 1])
    qml.RZ(phi, wires=2)
    qml.Barrier()
    
    for i in range(N - 1): qml.H(i)
    
    expvals = []
    for i in range(N - 1):
        expvals.append(qml.expval(qml.PauliZ(i)))
    return expvals

theta, phi = np.pi/2, np.pi
# %% draw
print(qml.draw(circuit)(theta, phi))

# %% draw_mpl
styles = ('black_white', 'black_white_dark', 'sketch', 'pennylane',
          'pennylane_sketch', 'sketch_dark', 'solarized_light',
          'solarized_dark', 'default')
for style in styles:
    fig, ax = qml.draw_mpl(circuit, style=style)(theta, phi)
    fig.suptitle(f"draw_mpl with {style=}")
    
    fig.canvas.draw()

# %% draw_mpl with rectangular boxes
fig, ax = qml.draw_mpl(circuit, style='black_white',
                       decimals=2)(theta, phi)
fig.suptitle("draw_mpl with style='black_white' and rectangular boxes")

for p in ax.patches:
    if isinstance(p, patches.FancyBboxPatch):
        p.set_boxstyle("square,pad=0.2")
        p.set_linewidth(1.5)

fig.canvas.draw()
