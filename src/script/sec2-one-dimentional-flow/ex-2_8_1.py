import os
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

parser = argparse.ArgumentParser(add_help=True)
parser.add_argument("-x", "--x_0_list", type=list, default=[0.3, 0.01, 2, 2], help="[2, 0.3] means x_0 = 2, 0.3.")
parser.add_argument("-tf", "--t_f", type=int, default=10)
parser.add_argument("-t", "--t_0_list", type=list, default=[0, 1, 3, 6], help="[0, 2] means t_0 = 0, 2.")
parser.add_argument("-v", "--visualize", action="store_true")
parser.add_argument("-f", "--figurepath",type=str, required=True)

args = parser.parse_args()

assert len(args.x_0_list) == len(args.t_0_list)

filepath_woExt = os.path.splitext(args.figurepath)[0]

t_mesh, x_mesh = np.meshgrid(np.arange(0, 10, 0.5), np.arange(0, 2.2, 0.2))
u_mesh = np.ones_like(t_mesh)
v_mesh = x_mesh * (1 - x_mesh)

solutions = []
logistic_eq = lambda t, y: y * (1 - y)
for x_0, t_0 in zip(args.x_0_list, args.t_0_list):
    print(f"x_0 = {x_0},\nt_0 = {t_0},\nt_f = {args.t_f}\n")
    sol = solve_ivp(fun = logistic_eq,
                    t_span = [t_0, args.t_f],
                    y0 = [x_0],
                    method = "RK45",
                    rtol=0.001,
                    atol=1e-06,
                    max_step = 0.05)
    solutions.append(sol)

fig = plt.figure(figsize=[60,15])
fig.subplots_adjust(left = 0.05,
                    right = 0.95,
                    bottom = 0.05,
                    top = 0.95,
                    wspace = 0.08)

fs = 40

ax_onlyField = fig.add_subplot(121)
ax_onlyField.quiver(t_mesh, 
                    x_mesh, 
                    u_mesh, 
                    v_mesh,
                    width = 0.003)

plt.setp(ax_onlyField.get_xticklabels(), fontsize=fs)
plt.setp(ax_onlyField.get_yticklabels(), fontsize=fs)

ax_trajectory = fig.add_subplot(122)
ax_trajectory.quiver(t_mesh, 
                     x_mesh,
                     u_mesh,
                     v_mesh,
                     width = 0.003)

plt.setp(ax_trajectory.get_xticklabels(), fontsize=fs)
plt.setp(ax_trajectory.get_yticklabels(), fontsize=fs)
for sol in solutions:
    print(sol.y)
    ax_trajectory.plot(sol.t, sol.y[0], linewidth=7)
if args.visualize:
    fig.show()
fig.savefig(args.figurepath)