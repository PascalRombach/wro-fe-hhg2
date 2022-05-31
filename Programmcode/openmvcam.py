import sensor, image, pyb
import json, time

THRESHOLDS = [
    (35,43,53,65,33,40), # Red pillars (code: 1)
    (14,18,-4,-3,0,1),# Green pillars (code: 2)
    (10,-10,0, 20,0,7) # Black walls (code: 4)
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


vcp = pyb.USB_VCP()
vcp.init()

# Main process loop
def main():
    while vcp.isconnected():
        im = sensor.snapshot()
        #print(image.rgb_to_lab(im.get_pixel(160,120)))
        #im.draw_cross(160,120)

        vcp.send(b"BEGIN\n") # Tell the RPi that a new line of blobs is coming up
        vcp.send(f"{im.width},{im.height}\n".encode("utf-8"))
        for blob in im.find_blobs(THRESHOLDS, pixels_threshold=10, area_threshold=10, merge=True):
            if not blob.code() in CODE_DESCRIPTORS.keys(): continue
            code_str = CODE_DESCRIPTORS[blob.code()]

            data_obj = {"type":code_str,"left_top":(blob.x(),blob.y()),"size":(blob.w(),blob.h())}
            vcp.send((json.dumps(data_obj)+"\n").encode("utf-8"))
            im.draw_rectangle(*blob.rect())
            pass

        vcp.send(b"END\n") # Tell the RPi that this frame's data is now over
        pass

while True:
    while not vcp.isconnected(): time.sleep_ms(100)
    main()
    pass
