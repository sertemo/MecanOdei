"""Script principal"""

import flet as ft

NOT_SHOWN_KEYS = ['Backspace', 'Caps Lock', 'Enter']
TEXT_REF = "La monja come jamón"



def main(page:ft.Page) -> None:
    class Counter:
        def __init__(self) -> None:
            self.count:int = 0

        def add(self) -> None:
            self.count += 1
        
        def sustract(self) -> None:
            if self.count:
                self.count -= 1

        def __repr__(self) -> str:
            return f'{int(self.count)}'
    
    counter = Counter()

    def on_keyboard(e: ft.KeyboardEvent):
        if e.shift and e.key not in NOT_SHOWN_KEYS:
            texto_escrito.value += e.key
            counter.add()   
        elif e.key == 'Backspace':
            texto_escrito.value = texto_escrito.value[:-1]
            counter.sustract()
        else:
            texto_escrito.value += e.key.lower()
            counter.add()
        
        

        for idx in range(counter.count):
            texto_ref.controls[idx].bgcolor = 'blue'

        page.update()
    
    page.on_keyboard_event = on_keyboard

    texto_ref = ft.Row([
        ft.Container(ft.Text(letra)) for letra in TEXT_REF
    ],
    spacing=0)
    texto_escrito = ft.Text( "", color='red')
    

    page.add(
        texto_ref,
        ft.Container(texto_escrito),
        ft.Text(counter.count))


if __name__ == '__main__':
    ft.app(target=main)