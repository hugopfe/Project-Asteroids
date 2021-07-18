import os
import sys


def get_path(directory: str, filename: str):
    if directory:
        return os.path.join(ROOT_DIR, directory, filename)
    return os.path.join(ROOT_DIR, filename)


def img_path(filename: str): return get_path('images', filename)


ROOT_DIR = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

print(img_path('asteroid_big.png'))

bg = img_path('background.jpg')
ship = img_path('nave.png')
asteroid = img_path('asteroid_big.png')
ast_frag1 = img_path('asteroid_part_1.png')
ast_frag2 = img_path('asteroid_part_2.png')
ast_frag3 = img_path('asteroid_part_3.png')
logo = img_path('logo.png')
shield = img_path('shield_prototype.png')
