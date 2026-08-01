import pyautogui


class VirtualMouse:

    def __init__(self):

        # Screen size
        self.screen_width, self.screen_height = pyautogui.size()

        # Previous cursor position
        self.previous_x = 0
        self.previous_y = 0

        # Smoothness
        # Value kam = cursor slow/smooth
        # Value zyada = cursor fast
        self.smoothening = 5


    def move_cursor(
        self,
        x,
        y,
        frame_width,
        frame_height
    ):

        # Convert camera coordinates
        target_x = int(

            x
            * self.screen_width
            / frame_width

        )


        target_y = int(

            y
            * self.screen_height
            / frame_height

        )


        # Smooth movement
        current_x = (

            self.previous_x

            + (

                target_x
                - self.previous_x

            )
            / self.smoothening

        )


        current_y = (

            self.previous_y

            + (

                target_y
                - self.previous_y

            )
            / self.smoothening

        )


        # Move cursor
        pyautogui.moveTo(

            int(current_x),

            int(current_y)

        )


        # Save current position
        self.previous_x = current_x

        self.previous_y = current_y