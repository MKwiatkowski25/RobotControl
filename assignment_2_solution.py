from assignment_2_lib import take_a_photo, drive
import cv2
import numpy as np

def mask_red(photo):
    image = photo[0:400, :, [2, 1, 0]]
    # I assume that photo is taken from function take_a_photo(), so I change the order of colors
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower1 = np.array([0, 100, 50])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv_image, lower1, upper1)

    lower2 = np.array([170, 100, 50])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv_image, lower2, upper2)

    return mask1 + mask2

def mask_blue(photo):
    image = photo[0:400, :, [2, 1, 0]]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([110, 100, 50])
    upper = np.array([130, 255, 255])
    return cv2.inRange(hsv_image, lower, upper)

def mask_green(photo):
    image = photo[0:400, :, [2, 1, 0]]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([50, 100, 50])
    upper = np.array([70, 255, 255])
    return cv2.inRange(hsv_image, lower, upper)

def go_to_columns(car, mask_function):
    run = True
    pom = np.arange(-320, 320)
    while run:
        photo = take_a_photo(car)
        mask = mask_function(photo)[1]/255
        direction = np.dot(mask,pom)
        if direction<0:
            drive(car, True, 1)
        if direction>0:
            drive(car, True, -1)
        if all(mask==np.zeros(640)):
            run = False
        else:
            diff = np.max(np.where(mask == 1)) - np.min(np.where(mask == 1))
            if diff>400:
                run=False
        drive(car, True, 0)



def forward_distance(photo):
    mask = mask_red(photo)
    y = np.argmax(np.sum(mask, axis=1))
    size = np.sum(mask[y, :]) / 255

    #I made a list of sizes of the ball and for each I calculated distance and then converted it to steps.

    if size<50:
        if size<45:
            if size<42:
                if size<38:
                    if size < 36:
                        if size < 33:
                            if size < 31:
                                if size < 27:
                                    return 9700
                                else:
                                    return 9000
                            else:
                                return 8329
                        else:
                            return 7279
                    else:
                        return 6500
                else:
                    return 6150
            else:
                return 5650
        else:
            return 4800
    else:
        return 3850



def find_a_ball(car):
    run = True
    while run:
        photo = take_a_photo(car)

        mask = mask_red(photo)

        x = np.argmax(np.sum(mask, axis=0))
        y = np.argmax(np.sum(mask, axis=1))
        size = np.sum(mask[y, :]) / 255

        if size == 0:
            drive(car, True, -1)
            drive(car, False, 1)
        else:
            if x>320:
                drive(car, True, -1)
            else:
                if x < 280:
                    drive(car, True, 1)
                else:
                    drive(car, True, 0)
        if size > 180:
            run = False
    pass


def move_a_ball(car):
    find_a_ball(car) #At the beggining, robot goes to the ball
    #Robot finds blue columns and chooses direction (left/right)
    #When it's close to blue columns, it looks at the green ones and goes to them
    go_to_columns(car, mask_blue)
    go_to_columns(car, mask_green)
    pass
