#!/usr/bin/env python3
# coding: utf-8

import os

from sympy import init_printing
from sympy import *
init_printing()


def get_input(local=False):
    if local:
    
        x,y,z = symbols('x y z')
    
        return filename

    dids = os.getenv('DIDS', None)

    if not dids:
        print("No DIDs found in environment. Aborting.")
        return

    dids = json.loads(dids)
    
    for did in dids:
        print('ls', f'/data/inputs/{did}/0')
        print('ls2', os.listdir(f'/data/inputs/'))
        filename = Path(f'/data/inputs/{did}/0')  # 0 for metadata service
        print(f"Reading asset file {filename}.")
        return filename



def run_model(local=False):
    
    e = x**2 + 2.0*y + sin(z); e
    



if __name__ == "__main__":
    run_model(get_input())