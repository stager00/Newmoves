from picrawler import Picrawler
from time import sleep
from robot_hat import Music, TTS
from vilib import Vilib
import readchar
import random
import threading
import cv2
import numpy as np

crawler = Picrawler()
music = Music()
tts = TTS()
camera_on = False

manual = '''
Press keys on keyboard to control Picrawler!
    w: Forward
    a: Turn left
    s: Backward
    d: Turn right
    i: Sit
    o: Stand
    u: Look up
    j: Look down
    k: Dance
    l: Wave hand
    m: Beckon
    n: Shake hand
    f: Fighting
    e: Excited
    p: Play dead
    c: Climb
    v: Swivel
    x: Forward Jump Up
    z: Superman Crawl
    t: Spin 360
    b: Wave Both Hands
    q: Side Step Left
    r: Backflip
    g: Toggle Camera Feed
    space: Say the target again
    Ctrl^C: Quit
'''

color = "red"
color_list = ["red", "orange", "yellow", "green", "blue", "purple"]
key_dict = {
    'w': 'forward',
    's': 'backward',
    'a': 'turn_left',
    'd': 'turn_right',
}

def renew_color_detect():
    global color
    color = random.choice(color_list)
    Vilib.color_detect(color)
    tts.say("Look for " + color)

key = None
lock = threading.Lock()

def key_scan_thread():
    global key
    while True:
        key_temp = readchar.readkey()
        print('\r', end='')
        with lock:
            key = key_temp.lower()
            if key == readchar.key.SPACE:
                key = 'space'
            elif key == readchar.key.CTRL_C:
                key = 'quit'
                break
        sleep(0.01)

def toggle_camera():
    global camera_on
    camera_on = not camera_on
    if camera_on:
        cap = cv2.VideoCapture(0)
        while camera_on:
            ret, frame = cap.read()
            if not ret:
                break

            cv2.imshow('Camera Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('g'):
                camera_on = False

        cap.release()
        cv2.destroyAllWindows()

def sit(spider):
    spider.do_action('sit', speed=60)

def stand(spider):
    spider.do_action('stand', speed=60)

def look_up(spider):
    coords = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -76], [45, 0, -76], [45, 0, -38], [45, 45, -30]],
    ]
    for coord in coords:
        spider.do_step(coord, 60)

def look_down(spider):
    coords = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -28], [45, 0, -40], [45, 0, -68], [45, 45, -76]],
    ]
    for coord in coords:
        spider.do_step(coord, 60)

def dance(spider):
    spider.do_action('dance', speed=95)

def wave_hand(spider):
    stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    wave_hand = [
        [[45, 45, -70], [50, 40, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [-20, 60, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [50, 40, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [-20, 60, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [50, 40, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [-20, 60, 120], [45, 0, -60], [45, 45, -30]],
    ]
    return_stand = [
        [[45, 45, -50], [45, 0, -30], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -40], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in stand:
        spider.do_step(coord, 80)
    for coord in wave_hand:
        spider.do_step(coord, 90)
    for coord in return_stand:
        spider.do_step(coord, 80)

def beckon(spider):
    stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    beckon = [
        [[45, 45, -70], [10, 60, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [10, 60, 50], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [10, 60, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [10, 60, 50], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [10, 60, 120], [45, 0, -60], [45, 45, -30]],
        [[45, 45, -70], [10, 60, 50], [45, 0, -60], [45, 45, -30]],
    ]
    return_stand = [
        [[45, 45, -50], [45, 0, -30], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -40], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in stand:
        spider.do_step(coord, 80)
    for coord in beckon:
        spider.do_step(coord, 90)
    for coord in return_stand:
        spider.do_step(coord, 80)

def shake_hand(spider):
    ready = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -65], [5, 280, 80], [45, 0, -60], [45, 45, -40]],
    ]
    shake_hand = [
        [[45, 45, -65], [5, 280, 100], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 280, -10], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 280, 100], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 280, -10], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 280, 100], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 280, -10], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 100, 10], [45, 0, -60], [45, 45, -40]],
        [[45, 45, -65], [5, 100, 10], [45, 0, -60], [45, 45, -40]],
    ]
    return_stand = [
        [[45, 45, -50], [45, 0, -30], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -40], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in ready:
        spider.do_step(coord, 80)
    sleep(.2)
    for coord in shake_hand:
        spider.do_step(coord, 82)
    for coord in return_stand:
        spider.do_step(coord, 80)

def fighting(spider):
    ready = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -40], [45, 0, -40], [50, 20, -20], [45, 45, -50]],
        [[45, 45, -40], [45, 0, -40], [40, 20, -45], [45, 45, -50]],
        [[45, 45, -40], [45, 0, -40], [60, 40, -60], [45, 45, -40]],
        [[45, 45, -40], [45, 30, -30], [60, 40, -60], [45, 45, -40]],
        [[45, 45, -30], [45, 30, -30], [60, 40, -60], [60, 40, -60]],
    ]
    twist_butt = [
        [[55, 7, -30], [19, 48, -30], [77, 12, -60], [36, 63, -60]],
        [[19, 48, -30], [55, 7, -30], [36, 63, -60], [77, 12, -60]],
        [[55, 7, -30], [19, 48, -30], [77, 12, -60], [36, 63, -60]],
        [[19, 48, -30], [55, 7, -30], [36, 63, -60], [77, 12, -60]],
        [[40, 30, -30], [40, 30, -30], [60, 40, -60], [60, 40, -60]],
        [[40, 60, -30], [40, 60, -30], [60, 10, -60], [60, 10, -60]],
    ]
    pounce_bite = [
        [[40, 40, -60], [20, 60, 110], [60, 60, -60], [60, 60, -60]],
        [[40, 40, -40], [20, 30, -40], [60, 60, -60], [60, 60, -60]],
        [[20, 60, 110], [20, 30, -60], [60, 60, -60], [60, 60, -60]],
        [[20, 30, -40], [20, 30, -40], [60, 60, -60], [60, 60, -60]],
    ]
    return_stand = [
        [[45, 45, -50], [45, 0, -30], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -40], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in ready:
        spider.do_step(coord, 80)
    for coord in twist_butt:
        spider.do_step(coord, 82)
    sleep(0.2)
    for coord in pounce_bite:
        spider.do_step(coord, 100)
    sleep(1)
    for coord in return_stand:
        spider.do_step(coord, 82)

def excited(spider):
    stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    up_down = [
        [[45, 45, -30], [45, 0, -30], [45, 0, -30], [45, 45, -30]],
        [[45, 45, -65], [45, 0, -65], [45, 0, -65], [45, 45, -65]],
        [[45, 45, -70], [45, 0, -70], [45, 0, -70], [45, 45, -70]],
        [[45, 45, -30], [45, 0, -30], [45, 0, -30], [45, 45, -30]],
        [[45, 45, -65], [45, 0, -65], [45, 0, -65], [45, 45, -65]],
        [[45, 45, -75], [45, 0, -75], [45, 0, -75], [45, 45, -75]],
        [[45, 45, -30], [45, 0, -30], [45, 0, -30], [45, 45, -30]],
        [[45, 45, -65], [45, 0, -65], [45, 0, -65], [45, 45, -65]],
        [[45, 45, -80], [45, 0, -80], [45, 0, -80], [45, 45, -80]],
    ]
    return_stand = [
        [[45, 45, -30], [45, 0, -30], [45, 0, -30], [45, 45, -30]],
        [[45, 45, -65], [45, 0, -65], [45, 0, -65], [45, 45, -65]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in stand:
        spider.do_step(coord, 80)
    for coord in up_down:
        spider.do_step(coord, 95)
    for coord in return_stand:
        spider.do_step(coord, 80)

def play_dead(spider):
    sit = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -10], [45, 0, -10], [45, 0, -10], [45, 45, -10]],
    ]
    play_dead = [
        [[45, 45, 100], [45, 45, 100], [45, 45, 100], [45, 45, 100]],
        [[45, 35, 60], [35, 45, 80], [35, 45, 80], [45, 35, 60]],
        [[35, 45, 80], [45, 35, 60], [45, 35, 60], [35, 45, 80]],
        [[45, 35, 60], [35, 45, 80], [35, 45, 80], [45, 35, 60]],
        [[35, 45, 80], [45, 35, 60], [45, 35, 60], [35, 45, 80]],
    ]
    for coord in sit:
        spider.do_step(coord, 80)
    for coord in play_dead:
        spider.do_step(coord, 90)

def climb(spider):
    high_stand = [
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
    ]
    full_steps = [
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
    ]
    normal_stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in high_stand:
        spider.do_step(coord, 80)
    for coord in full_steps:
        spider.do_step(coord, 90)
    for coord in normal_stand:
        spider.do_step(coord, 80)

def swivel(spider):
    stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    swivel_motion = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    return_stand = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in stand:
        spider.do_step(coord, 80)
    for coord in swivel_motion:
        spider.do_step(coord, 90)
    for coord in return_stand:
        spider.do_step(coord, 80)

def forward_jump_up(spider):
    crouch = [
        [[45, 45, -30], [45, 0, -30], [45, 0, -30], [45, 45, -30]],
    ]
    kick_off = [
        [[45, 45, -30], [45, 0, -30], [45, 0, -100], [45, 45, -100]],
    ]
    extend_front_legs = [
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
    ]
    for coord in crouch:
        spider.do_step(coord, 80)
    for coord in kick_off:
        spider.do_step(coord, 100)
    for coord in extend_front_legs:
        spider.do_step(coord, 90)
    climb(spider)

def superman_crawl(spider):
    sit_belly = [
        [[45, 45, -10], [45, 0, -10], [45, 0, -10], [45, 45, -10]],
    ]
    extend_front_legs = [
        [[45, 45, 100], [45, 0, 100], [45, 0, -10], [45, 45, -10]],
    ]
    pull_up_back_legs = [
        [[45, 45, 100], [45, 0, 100], [45, 0, 30], [45, 45, 30]],
    ]
    lower_and_push = [
        [[45, 45, 0], [45, 0, 0], [45, 0, 30], [45, 45, 30]],
        [[45, 45, 0], [45, 0, 0], [45, 0, 50], [45, 45, 50]],
    ]
    for coord in sit_belly:
        spider.do_step(coord, 80)
    for coord in extend_front_legs:
        spider.do_step(coord, 90)
    for coord in pull_up_back_legs:
        spider.do_step(coord, 80)
    for coord in lower_and_push:
        spider.do_step(coord, 60)

def spin_360(spider):
    spin_steps = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in spin_steps:
        spider.do_step(coord, 100)

def wave_both_hands(spider):
    wave_steps = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, 100], [45, 0, 100], [45, 0, -50], [45, 45, -50]],
        [[45, 45, 50], [45, 0, 50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, 100], [45, 0, 100], [45, 0, -50], [45, 45, -50]],
        [[45, 45, 50], [45, 0, 50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in wave_steps:
        spider.do_step(coord, 80)

def side_step(spider, direction='left'):
    if direction == 'left':
        side_steps = [
            [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
            [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        ]
    else:
        side_steps = [
            [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
            [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        ]
    for coord in side_steps:
        spider.do_step(coord, 80)

def backflip(spider):
    flip_steps = [
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
        [[45, 45, -100], [45, 0, -100], [45, 0, -100], [45, 45, -100]],
        [[45, 45, 100], [45, 0, 100], [45, 0, 100], [45, 45, 100]],
        [[45, 45, -50], [45, 0, -50], [45, 0, -50], [45, 45, -50]],
    ]
    for coord in flip_steps:
        spider.do_step(coord, 100)

def main():
    global key
    action = None
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)
    sleep(0.8)
    speed = 80
    print(manual)

    sleep(1)
    _key_t = threading.Thread(target=key_scan_thread)
    _key_t.setDaemon(True)
    _key_t.start()

    tts.say("game start")
    sleep(0.05)
    renew_color_detect()
    while True:
        if Vilib.detect_obj_parameter['color_n'] != 0 and Vilib.detect_obj_parameter['color_w'] > 100:
            tts.say("well done")
            sleep(0.05)
            renew_color_detect()

        with lock:
            if key is not None and key in ('wsad'):
                action = key_dict[str(key)]
                key = None
            elif key == 'space':
                tts.say("Look for " + color)
                key = None
            elif key == 'quit':
                _key_t.join()
                Vilib.camera_close()
                print("\n\rQuit")
                break
            elif key == 'g':
                toggle_camera()

        if action is not None:
            crawler.do_action(action, 1, speed)
            action = None

        sleep(0.05)

if __name__ == "__main__":
    main()
