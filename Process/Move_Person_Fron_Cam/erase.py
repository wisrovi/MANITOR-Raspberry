OBJ = dict()
OBJ["H_min"] = 0
OBJ["S_min"] = 48
OBJ["V_min"] = 40

OBJ["H_max"] = 60
OBJ["S_max"] = 255
OBJ["V_max"] = 255

import json
FILE = "config_color_piel.json"
# with open(FILE, 'w') as outfile:
#     json.dump(OBJ, outfile)

import os
if os.path.isfile(FILE):
    with open(FILE) as json_file:
        data = json.load(json_file)
        print(data)
else:
    print("No existe el archivo de configuracion para detectar el movimiento, por favor validelo o creelo con 'create_file_config_color.py'")