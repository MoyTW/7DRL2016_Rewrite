import os

_this_file = os.path.realpath(__file__)
_res_dir = os.path.split(_this_file)[0]

config = os.path.join(_res_dir, 'config.json')
