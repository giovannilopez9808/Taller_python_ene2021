from Class_list import *
inputs = {
    "repeat number": 9,
    "program name": "MD-n2",
    "path input": "../Input/",
}
program = MD(inputs["path input"],
             inputs["program name"],
             inputs["repeat number"])
program.run()
