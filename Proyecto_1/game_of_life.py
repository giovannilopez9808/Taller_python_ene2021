# Funciones propias
from packages import *
parameters = {
    "dimension": 100,
    "caminatas": 20,
    "supervivencia": 0.9,
}
campo = game(parameters["dimension"], parameters["supervivencia"])
campo.create()
for walk in range(parameters["caminatas"]):
    campo_new = campo.copiar()
    for i in range(parameters["dimension"]):
        for j in range(parameters["dimension"]):
            islive = campo.rules(i, j)
            campo_new.change_values(i, j, islive)
    image_plot(campo_new.values, walk+1, parameters["caminatas"])
    campo = campo_new.copiar()
create_gif()
clip_maker()
