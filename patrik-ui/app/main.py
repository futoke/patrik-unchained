# sudo apt update
# sudo apt install libmpv-dev libmpv2
# sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1


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

    page.add(
        expression_dropdown,
        animations_dropdown,
        set_face_btn,
        output_text
    )

ft.app(target=main)

