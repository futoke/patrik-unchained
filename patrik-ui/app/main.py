# sudo apt update
# sudo apt install libmpv-dev libmpv2
# sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1


import logging

import httpx
import flet as ft


class ControlBox(ft.Container):
    def __init__(self, content):
        super().__init__()

        self.content = content
        self.border_radius = 10
        self.width = 300
        self.padding = 10
        self.margin = 10
        self.bgcolor = ft.colors.GREY_100


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


async def get_data(url):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == httpx.codes.OK:
            return r.json()
        else:
            return {"пусто": None}


async def main(page: ft.Page):

    async def set_face_clicked(e):
        sended_value = expressions[expression_dropdown.value].replace("_", "-")
        output_text.value = f"Dropdown value is:  {sended_value}"

        async with httpx.AsyncClient() as client:
            await client.post(
                "http://patrik-face/set_face/",
                json={"expression": sended_value}
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
                    ft.Text("HELLO"),
                    ft.Text("HELLO")
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

