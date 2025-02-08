# sudo apt update
# sudo apt install libmpv-dev libmpv2
# sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1

import json
import logging

import httpx
import flet as ft


async def get_data(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == httpx.codes.OK:
            return r.json()
        else:
            return {"пусто": None}


class ControlBox(ft.Container):
    def __init__(self, content):
        super().__init__()

        self.content = content
        self.border_radius = 10
        self.width = 300
        self.padding = 10
        self.margin = 10
        self.bgcolor = ft.colors.GREY_100


class GazeCard(ft.Column):
    def __init__(self, easing):
        super().__init__()
        
        self.chk = ft.Checkbox(
            label="Включить", 
            value=True,
            on_change=self.chk_changed
        )
        self.speed = ft.TextField(
            label="Скорость движения глаз",
            hint_text="Используйте значения в диапазоне от 10 до 100",
            input_filter=ft.NumbersOnlyInputFilter(), 
            value="100"
        )

        self.easing = ft.Dropdown(
            label="Тип движения",
            options=[ft.dropdown.Option(ease) for ease in easing], 
        )

        self.dir = ft.Row(
            controls=[
                ft.TextField(
                    expand=True,
                    input_filter=ft.InputFilter(
                        allow=True, 
                        regex_string=r"[.0-9]", 
                        replacement_string=""
                    ),
                    label="Смещение по X",
                    value="0.5"
                ),
                ft.TextField(
                    expand=True,
                    input_filter=ft.InputFilter(
                        allow=True, 
                        regex_string=r"[.0-9]", 
                        replacement_string=""
                    ),
                    label="Смещение по Y",
                    value="0.5"
                )
            ]
        )

        self.controls = [
            self.chk,
            self.speed,
            self.easing,
            self.dir
        ]

    def chk_changed(self, e):
        for ctrl in self.controls:
            if not isinstance(ctrl, ft.Checkbox):
                ctrl.disabled = not self.chk.value
                ctrl.update()


class Test(ft.Column):
    def __init__(self):
        super().__init__()
        
        self.chk = ft.Checkbox(
            label="Включить", 
            value=True,
            on_change=self.chk_changed
        )
        self.btn_1 = ft.ElevatedButton("Button 1")
        self.btn_2 = ft.ElevatedButton("Button 2")
        self.btn_3 = ft.ElevatedButton("Button 3")
        self.btn_4 = ft.ElevatedButton("Button 4")

        self.controls = [
            self.chk,
            self.btn_1,
            self.btn_2,
            self.btn_3,
            self.btn_4,
        ]

    def chk_changed(self, e):
        for ctrl in self.controls:
            if isinstance(ctrl, ft.ElevatedButton):
                ctrl.disabled = not self.chk.value
                ctrl.update()


async def main(page: ft.Page):

    async def set_face_clicked(e):
        response = {
            "expression": "",
            "gaze": {
                "easing": "",
                "speed": 50,
                "direction": [0.5, 0.5]
            }
        }

        response["expression"] = expressions[expression_dropdown.value].replace("_", "-")
        logging.error(card.controls[1].controls[0].content.speed.value)
        
        async with httpx.AsyncClient() as client:
            await client.post(
                "http://patrik-face/set_face/", 
                data=json.dumps(response)
            )
        page.update()


    output_text = ft.Text()

    set_face_btn = ft.ElevatedButton(
        text="Задать эмоцию",
        on_click=set_face_clicked
    )

    expressions = await get_data("http://patrik-face/get_expressions/")
    expression_dropdown = ft.Dropdown(
        width=300,
        label="Эмоция",
        options=[ft.dropdown.Option(exp) for exp in expressions], 
    )

    animations = await get_data("http://patrik-face/get_animations/")
    animations_dropdown = ft.Dropdown(
        width=300,
        label="Анимация",
        options=[ft.dropdown.Option(anim) for anim in animations], 
    )


    anim_1 = ft.Column(
        controls= [
            expression_dropdown,
            animations_dropdown,
            set_face_btn,
            output_text
        ],
        width=300
    )

    easing = await get_data("http://patrik-face/get_easing/")

    card = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    anim_1,
                    ControlBox(Test())
                ]
            ),
            ft.Row(
                controls=[
                    ControlBox(GazeCard(easing))
                ]
            )
        ]
    )

    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                text="Эмоции",
                content=card,
                icon=ft.icons.FACE_RETOUCHING_NATURAL),
            ft.Tab(
                tab_content=ft.Icon(ft.icons.SEARCH),
            ),
            ft.Tab(
                text="Tab 3",
                icon=ft.icons.SETTINGS,
                content=ft.Text("This is Tab 3"),
            ),
        ],
    )

    page.add(t)

ft.app(target=main)

