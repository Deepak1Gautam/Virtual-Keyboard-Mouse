import cv2
import math
import pyautogui
import time

from modules.hand_tracker import HandTracker
from modules.virtual_mouse import VirtualMouse
from modules.virtual_keyboard import VirtualKeyboard


# =====================================================
# CAMERA
# =====================================================

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


# =====================================================
# OBJECTS
# =====================================================

tracker = HandTracker()
mouse = VirtualMouse()
keyboard = VirtualKeyboard()


# =====================================================
# VARIABLES
# =====================================================

mode = "MOUSE"

typed_text = ""

key_cooldown = 0

left_click_cooldown = 0

right_click_cooldown = 0

dragging = False


# =====================================================
# KEYBOARD VARIABLES
# =====================================================

caps_lock = False

shift_active = False


# =====================================================
# MOUSE VARIABLES
# =====================================================

scroll_previous_y = None

pinch_start_time = None

PINCH_HOLD_TIME = 0.5


# =====================================================
# MODE SWITCHING
# =====================================================

gesture_start_time = None

last_gesture = None

GESTURE_HOLD_TIME = 1.0


# =====================================================
# FPS
# =====================================================

prev_time = 0

fps = 0


# =====================================================
# STATUS
# =====================================================

action_status = "READY"

gesture_status = "NONE"


# =====================================================
# WINDOW
# =====================================================

WINDOW_NAME = "Virtual Keyboard + Mouse"


# =====================================================
# TRANSPARENT PANEL
# =====================================================

def draw_transparent_panel(
    frame,
    x1,
    y1,
    x2,
    y2,
    color=(30, 30, 30),
    alpha=0.60
):

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x1, y1),
        (x2, y2),
        color,
        cv2.FILLED
    )

    cv2.addWeighted(
        overlay,
        alpha,
        frame,
        1 - alpha,
        0,
        frame
    )


# =====================================================
# DRAW BUTTON
# =====================================================

def draw_button(
    frame,
    text,
    x,
    y,
    width,
    height,
    active=False
):

    if active:

        color = (0, 140, 0)

    else:

        color = (40, 40, 40)


    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (x, y),
        (x + width, y + height),
        color,
        cv2.FILLED
    )

    cv2.addWeighted(
        overlay,
        0.70,
        frame,
        0.30,
        0,
        frame
    )


    cv2.rectangle(
        frame,
        (x, y),
        (x + width, y + height),
        (255, 255, 255),
        2
    )


    text_size = cv2.getTextSize(
        text,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        2
    )[0]


    text_x = x + (
        width - text_size[0]
    ) // 2


    text_y = y + (
        height + text_size[1]
    ) // 2


    cv2.putText(
        frame,
        text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )


# =====================================================
# MAIN LOOP
# =====================================================

while True:


    # =================================================
    # CAMERA FRAME
    # =================================================

    success, frame = cap.read()


    if not success:

        break


    frame = cv2.flip(
        frame,
        1
    )


    height, width, _ = frame.shape


    # =================================================
    # FPS
    # =================================================

    current_time = time.time()


    if prev_time != 0:

        fps = 1 / (
            current_time - prev_time
        )


    prev_time = current_time


    # =================================================
    # HAND DETECTION
    # =================================================

    frame, results = tracker.find_hands(
        frame
    )


    landmarks = tracker.find_position(
        frame
    )


    # =================================================
    # MODE SWITCHING
    # =================================================

    if landmarks:


        fingers = tracker.fingers_up(
            landmarks
        )


        # ONE FINGER = MOUSE

        if (

            fingers[1] == 1

            and fingers[2] == 0

            and fingers[3] == 0

            and fingers[4] == 0

        ):

            current_gesture = "MOUSE"

            gesture_status = "INDEX FINGER"


        # TWO FINGERS = KEYBOARD

        elif (

            fingers[1] == 1

            and fingers[2] == 1

            and fingers[3] == 0

            and fingers[4] == 0

        ):

            current_gesture = "KEYBOARD"

            gesture_status = "INDEX + MIDDLE"


        else:

            current_gesture = None

            gesture_status = "NONE"


        if current_gesture != last_gesture:

            last_gesture = current_gesture

            gesture_start_time = time.time()


        if current_gesture:


            gesture_time = (

                time.time()

                - gesture_start_time

            )


            if gesture_time >= GESTURE_HOLD_TIME:


                if current_gesture != mode:


                    mode = current_gesture

                    action_status = f"{mode} MODE"


                    if dragging:

                        pyautogui.mouseUp()

                        dragging = False


    else:

        last_gesture = None

        gesture_start_time = None

        gesture_status = "NO HAND"


    # =================================================
    # TOP NAVIGATION
    # =================================================

    draw_button(
        frame,
        "MOUSE MODE",
        20,
        20,
        180,
        50,
        mode == "MOUSE"
    )


    draw_button(
        frame,
        "KEYBOARD MODE",
        220,
        20,
        220,
        50,
        mode == "KEYBOARD"
    )


    draw_button(
        frame,
        "EXIT",
        width - 140,
        20,
        120,
        50
    )


    # =================================================
    # KEYBOARD MODE
    # =================================================

    if mode == "KEYBOARD":


        hover_key = None


        if landmarks:


            index_x = landmarks[8][1]

            index_y = landmarks[8][2]


            key_info = keyboard.get_key_info(
                index_x,
                index_y
            )


            if key_info:

                hover_key = key_info["key"]


        # DRAW KEYBOARD

        frame = keyboard.draw_keyboard(
            frame,
            hover_key
        )


        if landmarks:


            index_x = landmarks[8][1]

            index_y = landmarks[8][2]


            thumb_x = landmarks[4][1]

            thumb_y = landmarks[4][2]


            selected_key = keyboard.get_key(
                index_x,
                index_y
            )


            distance = math.hypot(
                index_x - thumb_x,
                index_y - thumb_y
            )


            # KEY PRESS

            if (

                selected_key

                and distance < 40

                and key_cooldown == 0

            ):


                if selected_key == "SPACE":

                    typed_text += " "

                    pyautogui.press(
                        "space"
                    )

                    action_status = "SPACE"


                elif selected_key == "BACKSPACE":

                    typed_text = typed_text[:-1]

                    pyautogui.press(
                        "backspace"
                    )

                    action_status = "BACKSPACE"


                elif selected_key == "ENTER":

                    typed_text += "\n"

                    pyautogui.press(
                        "enter"
                    )

                    action_status = "ENTER"


                elif selected_key == "CLEAR":

                    typed_text = ""

                    action_status = "CLEARED"


                elif selected_key == "CAPS":

                    caps_lock = not caps_lock

                    action_status = (

                        "CAPS ON"

                        if caps_lock

                        else

                        "CAPS OFF"

                    )


                elif selected_key == "SHIFT":

                    shift_active = True

                    action_status = "SHIFT ACTIVE"


                else:

                    character = selected_key


                    if caps_lock or shift_active:

                        character = character.upper()

                    else:

                        character = character.lower()


                    typed_text += character


                    pyautogui.write(
                        character
                    )


                    action_status = (
                        f"TYPE: {character}"
                    )


                    shift_active = False


                key_cooldown = 20


            if key_cooldown > 0:

                key_cooldown -= 1


            # POINTER

            cv2.circle(
                frame,
                (index_x, index_y),
                12,
                (0, 255, 0),
                cv2.FILLED
            )


            if selected_key:

                cv2.putText(
                    frame,
                    f"Selected: {selected_key}",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )


    # =================================================
    # MOUSE MODE
    # =================================================

    elif mode == "MOUSE":


        if landmarks:


            thumb_x = landmarks[4][1]

            thumb_y = landmarks[4][2]


            index_x = landmarks[8][1]

            index_y = landmarks[8][2]


            middle_x = landmarks[12][1]

            middle_y = landmarks[12][2]


            index_thumb_distance = math.hypot(

                index_x - thumb_x,

                index_y - thumb_y

            )


            middle_thumb_distance = math.hypot(

                middle_x - thumb_x,

                middle_y - thumb_y

            )


            index_middle_distance = math.hypot(

                index_x - middle_x,

                index_y - middle_y

            )


            # SCROLL

            if index_middle_distance > 60:


                action_status = "SCROLLING"


                current_y = middle_y


                if scroll_previous_y is not None:


                    movement = (

                        scroll_previous_y

                        - current_y

                    )


                    if movement > 8:

                        pyautogui.scroll(2)


                    elif movement < -8:

                        pyautogui.scroll(-2)


                scroll_previous_y = current_y


            else:


                scroll_previous_y = None


                # CURSOR

                mouse.move_cursor(

                    index_x,

                    index_y,

                    width,

                    height

                )


                # RIGHT CLICK

                if (

                    middle_thumb_distance < 40

                    and right_click_cooldown == 0

                ):


                    pyautogui.rightClick()


                    action_status = "RIGHT CLICK"


                    right_click_cooldown = 20


                # PINCH

                if index_thumb_distance < 35:


                    if pinch_start_time is None:

                        pinch_start_time = time.time()


                    pinch_duration = (

                        time.time()

                        - pinch_start_time

                    )


                    if pinch_duration >= PINCH_HOLD_TIME:


                        if not dragging:


                            pyautogui.mouseDown()

                            dragging = True


                        action_status = "DRAGGING"


                else:


                    if dragging:


                        pyautogui.mouseUp()

                        dragging = False

                        action_status = "DRAG RELEASED"


                    if (

                        pinch_start_time is not None

                        and (

                            time.time()

                            - pinch_start_time

                        ) < PINCH_HOLD_TIME

                        and left_click_cooldown == 0

                    ):


                        pyautogui.click()


                        action_status = "LEFT CLICK"


                        left_click_cooldown = 20


                    pinch_start_time = None


                if left_click_cooldown > 0:

                    left_click_cooldown -= 1


                if right_click_cooldown > 0:

                    right_click_cooldown -= 1


                # POINTERS

                cv2.circle(
                    frame,
                    (index_x, index_y),
                    12,
                    (255, 0, 255),
                    cv2.FILLED
                )


                cv2.circle(
                    frame,
                    (thumb_x, thumb_y),
                    12,
                    (0, 255, 255),
                    cv2.FILLED
                )


    # =================================================
    # TYPED TEXT PANEL
    # =================================================

    if mode == "KEYBOARD":


        draw_transparent_panel(
            frame,
            20,
            85,
            width - 20,
            145,
            (30, 30, 30),
            0.55
        )


        cv2.putText(
            frame,
            typed_text[-50:],
            (35, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )


    # =================================================
    # STATUS PANEL
    # =================================================

    panel_x = width - 310

    panel_y = 100

    panel_width = 290

    panel_height = 190


    draw_transparent_panel(
        frame,
        panel_x,
        panel_y,
        panel_x + panel_width,
        panel_y + panel_height,
        (30, 30, 30),
        0.55
    )


    cv2.rectangle(
        frame,
        (panel_x, panel_y),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        "SYSTEM STATUS",
        (panel_x + 20, panel_y + 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"MODE: {mode}",
        (panel_x + 20, panel_y + 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"GESTURE: {gesture_status}",
        (panel_x + 20, panel_y + 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"ACTION: {action_status}",
        (panel_x + 20, panel_y + 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (panel_x + 20, panel_y + 155),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        f"CAPS: {'ON' if caps_lock else 'OFF'}",
        (panel_x + 20, panel_y + 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 255, 255),
        2
    )


    # =================================================
    # FULL INSTRUCTION PANEL
    # =================================================

    instruction_x = 20

    instruction_y = height - 180


    draw_transparent_panel(
        frame,
        10,
        instruction_y - 35,
        width - 20,
        height - 10,
        (30, 30, 30),
        0.55
    )


    cv2.rectangle(
        frame,
        (10, instruction_y - 35),
        (width - 20, height - 10),
        (255, 255, 255),
        2
    )


    cv2.putText(
        frame,
        "GESTURE CONTROLS",
        (instruction_x, instruction_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 255),
        2
    )


    if mode == "MOUSE":


        cv2.putText(
            frame,
            "INDEX FINGER -> MOVE CURSOR",
            (instruction_x, instruction_y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "INDEX + THUMB PINCH -> LEFT CLICK",
            (instruction_x, instruction_y + 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "HOLD PINCH -> DRAG",
            (instruction_x, instruction_y + 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "THUMB + MIDDLE PINCH -> RIGHT CLICK",
            (instruction_x + 400, instruction_y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "INDEX + MIDDLE APART -> SCROLL",
            (instruction_x + 400, instruction_y + 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "TWO FINGERS HOLD -> KEYBOARD MODE",
            (instruction_x + 400, instruction_y + 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


    else:


        cv2.putText(
            frame,
            "INDEX + MIDDLE HOLD -> KEYBOARD MODE",
            (instruction_x, instruction_y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "INDEX FINGER HOVER -> SELECT KEY",
            (instruction_x, instruction_y + 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "THUMB + INDEX PINCH -> TYPE",
            (instruction_x, instruction_y + 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )


        cv2.putText(
            frame,
            "CAPS | SHIFT | SPACE | BACKSPACE | ENTER | CLEAR",
            (instruction_x + 430, instruction_y + 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (255, 255, 255),
            1
        )


    cv2.putText(
        frame,
        "Q: QUIT",
        (width - 120, height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        2
    )


    # =================================================
    # SHOW
    # =================================================

    cv2.imshow(
        WINDOW_NAME,
        frame
    )


    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"):

        break


# =====================================================
# SAFETY
# =====================================================

if dragging:

    pyautogui.mouseUp()


cap.release()

cv2.destroyAllWindows()