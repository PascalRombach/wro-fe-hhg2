"""Issue: Blobs not recognise; boundries set properly"""

import sensor, image
import json

THRESHOLDS = [
    (35,43,53,65,33,40), # Red pillars (code: 1)
    (37,46,-31,-39,12,16)# Green pillars (code: 2)
    # Black walls (code: 4)
]
"""Holds the threshold values for colour tracking"""
CODE_DESCRIPTORS = {
    1: "red_pillar",
    2: "green_pillar",
    4: "wall"
}
""""Translate the colour codes to strs for easy interpretation"""

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False) # Need to turn this off for colour tracking
sensor.set_auto_whitebal(False) # Also turn this off for colour tracking
# Flip the image as the camera is upside down
sensor.set_vflip(True)
sensor.set_hmirror(True)


# Main process loop
while True:
    im = sensor.snapshot()
    #print(image.rgb_to_lab(im.get_pixel(160,120)))
    #im.draw_cross(160,120)

    print("BEGIN") # Tell the RPi that a new line of blobs is coming up
    for blob in im.find_blobs(THRESHOLDS, pixels_threshold=10, area_threshold=10, merge=True):
        code_str = CODE_DESCRIPTORS[blob.code()]

        data_obj = {"type":code_str,"left_top":(blob.x(),blob.y()),"size":(blob.w(),blob.h())}
        print(json.dumps(data_obj))
        #im.draw_rectangle(*blob.rect())
        pass

    print("END") # Tell the RPi that this frame's data is now over
    pass