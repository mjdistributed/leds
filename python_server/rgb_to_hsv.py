# `rgbToHsv`
# Converts an RGB color value to HSV
# *Assumes:* r, g, and b are contained in the set [0, 255] or [0, 1]
# *Returns:* { h, s, v } in [0,1]
def rgbToHsv(r, g, b):

    max_rgb = max(r, g, b)
    min_rgb = min(r, g, b)
    print("max: " + str(max_rgb) + ", min: " + str(min_rgb))
    h = s = v = max_rgb

    delta = max_rgb - min_rgb
    print("delta: " + str(delta))
    if (max_rgb == 0):
        s = 0
    else:
        s = delta * 1.0 / max_rgb

    print("s: "+ str(s))

    if (max_rgb == min_rgb):
        h = 0; # achromatic
    else:
        if(max_rgb == r):
            if(g < b):
                tmp = 6
            else:
                tmp = 0
            h = (g - b) * 1.0 / delta + tmp
        elif(max_rgb == g):
            print("max is green")
            h = (b - r) * 1.0 / delta + 2
        elif(max_rgb == b):
            h = (r - g) * 1.0 / delta + 4
        h /= 6
    return (h, s, v)


# takes h from [0,1] to [0,359]
def scaleHue(h):
    return h * 359