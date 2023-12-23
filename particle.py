import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

def psi(x, p=0, mu=0, sigma=1):
    P = np.exp(-(x-mu)**2 / sigma**2, dtype=complex)
    M = np.exp(1j*p*x)
    return normalize(M*P, x[1]-x[0])

def normalize(psi, dx):
    psi_norm = np.sum(np.square(np.abs(psi)))*dx
    return psi / np.sqrt(psi_norm)

def Laplacian(psi, gridspace=1, bound=1):
    d2psidx2 = -2 * psi[:]
    d2psidx2[:-bound] += psi[bound:] 
    d2psidx2[bound:] += psi[:-bound]
    return d2psidx2 / gridspace

def dpsidt(psi, hbar=1, m=1, V=0, **kwargs):
    return 1j*hbar/2*m * Laplacian(psi, **kwargs) - 1j*V*psi

def RK4_step(dydt, y, dt, **kwargs):
    k1 = dydt(y, **kwargs)
    k2 = dydt(y+dt/2*k1, **kwargs)
    k3 = dydt(y+dt/2*k2, **kwargs)
    k4 = dydt(y+dt*k3, **kwargs)
    return y + dt/6*(k1+2*k2+2*k3+k4)


x0 = -10
xf = 10
dx = 0.01
x = np.arange(x0, xf, dx)
mu = 0
p = 0
sigma = .1

wave_function0 = psi(x, p, mu, sigma)
wave_function_states = [wave_function0]
steps = 10000
dt = 0.01

hbar=1
m=100
barrier1 = np.where((x>1)&(x<1.2),1,0)
barrier2 = np.where((x>-1.2)&(x<-1),1,0)
V = barrier1 + barrier2

for i in range(steps):
    wave_function0 = RK4_step(dpsidt, wave_function0, dt, hbar=hbar, m=m, V=V)
    wave_function0 = normalize(wave_function0, dx)
    
    if i%5 == 0:
        wave_function_states.append(wave_function0)

fig, ax = plt.subplots()
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.fill_between(x, -2, 2, where=(x>1)&(x<1.2),color="red",alpha=0.2)
ax.fill_between(x, -2, 2, where=(x>-1.2)&(x<-1),color="red",alpha=0.2)

psi_square, = ax.plot([],[],label="P(Ψ)")
real, = ax.plot([],[],label="Ψ Re")
imag, = ax.plot([],[],label="Ψ Im")
ax.legend()

def animate(frame):
    psi_square.set_data(x, np.abs(wave_function_states[frame]))
    real.set_data(x, np.real(wave_function_states[frame]))
    imag.set_data(x, np.imag(wave_function_states[frame]))
    return psi_square,real,imag,

ANIMATOR = FuncAnimation(fig, animate, len(wave_function_states), interval=1, blit=True)
plt.show()
