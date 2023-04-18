from pathlib import Path
import json
import random


def getComment(position, piece = ""):
    path = Path(__file__,'..').resolve()
    
    with open(path.joinpath("commentary_data.json") , "r", encoding="utf-8") as f:
        data = json.load(f)

        r = random.randint(0,100)

        if r < 10: 
            return ""
        if r < 60: 
            default = data["default"]
            i = random.randint(0, len(default)-1)
            return default[i]
        else:
            if not (position in data):
                return "Brak słów"
        
            return data[position]
        


