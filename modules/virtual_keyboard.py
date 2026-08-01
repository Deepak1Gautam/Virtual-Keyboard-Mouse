import cv2


class VirtualKeyboard:

    def __init__(self):

        # =========================
        # KEYBOARD LAYOUT
        # =========================

        self.keys = [

            # Number Row
            [
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "0"
            ],

            # QWERTY Row
            [
                "Q", "W", "E", "R", "T",
                "Y", "U", "I", "O", "P"
            ],

            # Home Row
            [
                "A", "S", "D", "F", "G",
                "H", "J", "K", "L"
            ],

            # Bottom Row
            [
                "Z", "X", "C", "V",
                "B", "N", "M"
            ],

            # Special Keys
            [
                "CAPS",
                "SHIFT",
                "SPACE",
                "BACKSPACE",
                "ENTER",
                "CLEAR"
            ]

        ]

        # =========================
        # KEY SETTINGS
        # =========================

        self.key_width = 75

        self.key_height = 50

        self.gap = 8

        self.start_y = 190


    # =========================
    # GET KEY WIDTH
    # =========================

    def get_key_width(self, key):

        if key == "SPACE":

            return 250

        elif key in [

            "BACKSPACE",
            "ENTER",
            "SHIFT",
            "CAPS",
            "CLEAR"

        ]:

            return 120

        else:

            return self.key_width


    # =========================
    # GET ROW WIDTH
    # =========================

    def get_row_width(self, row):

        total_width = 0

        for key in row:

            total_width += (

                self.get_key_width(key)

                + self.gap

            )

        return total_width - self.gap


    # =========================
    # DRAW KEYBOARD
    # =========================

    def draw_keyboard(

        self,

        frame,

        hover_key=None

    ):

        current_y = self.start_y


        for row in self.keys:


            # Calculate row width
            row_width = self.get_row_width(row)


            # Center row
            current_x = (

                frame.shape[1]

                - row_width

            ) // 2


            for key in row:


                # Key width
                width = self.get_key_width(key)


                # =========================
                # HOVER COLOR
                # =========================

                if key == hover_key:

                    background_color = (

                        0,

                        180,

                        0

                    )

                else:

                    background_color = (

                        45,

                        45,

                        45

                    )


                # =========================
                # DRAW KEY
                # =========================

                cv2.rectangle(

                    frame,

                    (

                        current_x,

                        current_y

                    ),

                    (

                        current_x + width,

                        current_y

                        + self.key_height

                    ),

                    background_color,

                    cv2.FILLED

                )


                # =========================
                # BORDER
                # =========================

                cv2.rectangle(

                    frame,

                    (

                        current_x,

                        current_y

                    ),

                    (

                        current_x + width,

                        current_y

                        + self.key_height

                    ),

                    (

                        255,

                        255,

                        255

                    ),

                    2

                )


                # =========================
                # TEXT SIZE
                # =========================

                text_size = cv2.getTextSize(

                    key,

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.55,

                    2

                )[0]


                # =========================
                # TEXT POSITION
                # =========================

                text_x = (

                    current_x

                    + (

                        width

                        - text_size[0]

                    ) // 2

                )


                text_y = (

                    current_y

                    + (

                        self.key_height

                        + text_size[1]

                    ) // 2

                )


                # =========================
                # DRAW TEXT
                # =========================

                cv2.putText(

                    frame,

                    key,

                    (

                        text_x,

                        text_y

                    ),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    0.55,

                    (

                        255,

                        255,

                        255

                    ),

                    2

                )


                # Next key
                current_x += (

                    width

                    + self.gap

                )


            # Next row
            current_y += (

                self.key_height

                + self.gap

            )


        return frame


    # =========================
    # GET KEY INFO
    # =========================

    def get_key_info(

        self,

        x,

        y,

        frame_width=1280

    ):


        current_y = self.start_y


        for row in self.keys:


            # Row width
            row_width = self.get_row_width(

                row

            )


            # Center row
            current_x = (

                frame_width

                - row_width

            ) // 2


            for key in row:


                # Key width
                width = self.get_key_width(

                    key

                )


                # Check finger position
                if (

                    current_x

                    <= x

                    <= current_x + width

                    and

                    current_y

                    <= y

                    <= current_y + self.key_height

                ):


                    return {

                        "key": key,

                        "x": current_x,

                        "y": current_y,

                        "width": width,

                        "height": self.key_height

                    }


                # Next key
                current_x += (

                    width

                    + self.gap

                )


            # Next row
            current_y += (

                self.key_height

                + self.gap

            )


        return None


    # =========================
    # GET KEY
    # =========================

    def get_key(

        self,

        x,

        y

    ):


        key_info = self.get_key_info(

            x,

            y

        )


        if key_info:

            return key_info["key"]


        return None