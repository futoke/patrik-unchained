# sudo apt update
# sudo apt install libmpv-dev libmpv2
# sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1

import httpx
import flet as ft


async def get_expressions():
    async with httpx.AsyncClient() as client:
        r = await client.get("http://localhost:8888/get_expressions/")
        return r.json()


async def main(page: ft.Page):
    async def button_clicked(e):
        sended_value = expressions[expression_dropdown.value].replace("_", "-")
        output_text.value = f"Dropdown value is:  {sended_value}"

        async with httpx.AsyncClient() as client:
            await client.post(
                "http://localhost:8888/set_face/",
                json={"expression": sended_value}
            )

        page.update()

    expressions = await get_expressions()

    output_text = ft.Text()
    submit_btn = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    expression_dropdown = ft.Dropdown(
        width=300,
        label="Эмоция",
        options=[ft.dropdown.Option(exp) for exp in expressions], 
    )
    page.add(expression_dropdown, submit_btn, output_text)

ft.app(target=main)

