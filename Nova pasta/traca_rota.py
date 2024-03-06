import keyboard
import time
import json
from pathlib import Path

class KeyDirection:
    def __init__(self, key_name=None, start_time=None):
        self.key_name = key_name
        self.start_time = start_time if start_time is not None else time.time()
        self.time_press = 0
        self.is_pressed = False

    def start_press(self):
        self.is_pressed = True
        self.start_time = time.time()

    def end_press(self):
        self.is_pressed = False
        self.calc_time_press(time.time())

    def calc_time_press(self, end_time):
        self.time_press = end_time - self.start_time

print("Ao executar o codigo, clique no jogo e trace a rota \n Nao use diagonais! \n Para salvar uma rota aperte 'barra de espaco' \n Para encerrar o programa, digite 'sair' quando solicitado o land number!")

while True:
    
    land_number = input("Insira o numero da land: ")
    lista = []
    if land_number == "sair":
        break

    def on_key_event(e, lista):
        key_name = e.name

        # Verifica se a tecla está sendo pressionada pela primeira vez
        if e.event_type == keyboard.KEY_DOWN and not any(item.key_name == key_name and item.is_pressed for item in lista):
            temp = KeyDirection(key_name, time.time())
            temp.start_press()
            if e.name != 'enter' and e.name != 'space':
                lista.append(temp)

        # Verifica se a tecla foi liberada
        elif e.event_type == keyboard.KEY_UP:
            for item in lista:
                if item.key_name == key_name and item.is_pressed:
                    item.end_press()

    # Configura o hook do evento de tecla
    keyboard.hook(lambda e: on_key_event(e, lista))
    keyboard.wait('space')
    
    json_data = []

    json_file_path = Path('rotas_galinheiro.json')
    if json_file_path.exists():
        with open(json_file_path, 'r') as existing_json_file:
            json_data = json.load(existing_json_file)

    # Adiciona os novos dados
    json_data.append({
        'land_number': land_number,
        'directions': []
    })

    for item in lista:
        json_data[-1]['directions'].append({
            'key_name': item.key_name,
            'time_press': round(item.time_press, 2)
        })

    # Salva as informações no arquivo JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=2) 
  