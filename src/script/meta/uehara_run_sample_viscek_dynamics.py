#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import glob
import string
import argparse
import platform
import itertools
import subprocess
import numpy as np

sys.path.append(".")

from pyutils.parallel import multi_process, for_each

parser = argparse.ArgumentParser()
parser.add_argument("--begin_id", type=int, default=0)
parser.add_argument("--end_id", type=int, default=None)
parser.add_argument("--split_num", type=int, default=1)
parser.add_argument("--node_num", type=int, default=None)
parser.add_argument("--debug", action="store_true")
parser.add_argument("--show_std", action="store_true")
# experimental options
parser.add_argument("--eta_range", type=float, nargs=2, default=(-2, 2))
parser.add_argument("--eta_split", type=int, default=5)
parser.add_argument("--seed", type=int, required=True)
parser.add_argument("--T", type=int, default=1000000)
parser.add_argument("--sample_num", type=int, default=10)
parser.add_argument("--num_particles", type=int, default=1000)
parser.add_argument("--sharing", action="store_true")
parser.add_argument("--initial_condition", type=str, choices=["share", "perturbation"], default="perturbation")
parser.add_argument("--noise_range", type=float, nargs=2, default=(-2, 2))
parser.add_argument("--num_perturbations", type=int, default=5)

args, unknown = parser.parse_known_args()
print(args.debug)
if __name__ == '__main__':
    def _run(_id, _eta, worker_id=None):
        cmd = "python src/script/base/uehara_sample_vicsek_dynamics.py "
        cmd += "--seed {} ".format(args.seed)
        cmd += "--T {} ".format(args.T)
        cmd += "--sample_num {} ".format(args.sample_num)
        cmd += "--num_particles {} ".format(args.num_particles)
        cmd += "--eta {} ".format(10**_eta)
        cmd += "--num_perturbations {} ".format(args.num_perturbations)

        save_name = f"seed={args.seed},T={args.T},N={args.sample_num},D={args.num_particles},"
        save_name += "eta={:.2f}".format(_eta)

        if args.sharing:
            save_name += ",shared "
            cmd += "--share_w_in "
            cmd += "--share_us "

        cmd += "--save_name {} ".format(save_name)
        cmd += " ".join(unknown) + " "
        print("[{}] : {}".format(_id, cmd))
        if not args.debug:
            std = None if args.show_std else subprocess.DEVNULL
            subprocess.call(
                cmd.split(), stdout=std, stderr=std)

    eta_list = np.linspace(*args.eta_range, args.eta_split)
    arg_list = list(itertools.product(eta_list, ))
    arg_list = [(_id,) + _ for _id, _ in enumerate(arg_list)]
    arg_list = arg_list[args.begin_id:args.end_id:args.split_num]

    if args.node_num is None:
        for_each(_run, arg_list, expand=True, verbose=False)
    else:
        multi_process(_run, arg_list, verbose=False, append_id=True,
                      expand=True, nodes=args.node_num)
