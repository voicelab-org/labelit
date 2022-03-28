import random
import colorsys

def random_dark_color():
    h, s, l = random.random(), 0.4, 0.5
    r, g, b = [int(256 * i) for i in colorsys.hls_to_rgb(h, l, s)]
    return "rgb({},{},{})".format(r, g, b)