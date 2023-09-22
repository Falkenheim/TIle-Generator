import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import json
import os
import webbrowser
import string
import math

#(1)2
# 3 4
# Snaked Proofreading Tile für das Nordwestliche Tile
# tile = Aktuell betrachtetes Tile, auf welchem Proofreading angewendet wird
# has_glues = Dictionary, um Wachstumsrichtung des Tiles abfragen zu können
# temperature = Temperatur des Systems
# glue_strength = Dictionary, um zusätzliche Kleberstärken abfragen zu können, um innere Kleber zu bestimmen
# label_counts = Dictionary, um die Anzahl aller Bezeichner im gesamten Tileset abzubilden und so eindeutige innere Kleberbezeichner erstellen zu können
# label_suffix = Liste von Suffixen für die Kleberbezeichner
def snaked_proofreading_north_west(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists):
    # Fall khaki
    if tile["color"] == "khaki" or tile["color"] == "#ecda88":
        if not tile["glues"][3]["strength"] is None:
            glue_strength["east"] = max(glue_strength["east"], tile["glues"][3]["strength"])
        return generate_tile(
            tile["label"], # Label
            tile["glues"][0]["label"], # nördlicher Bezeichner
            tile["glues"][0]["strength"]-1 if tile["glues"][0]["label"] else tile["glues"][0]["strength"], # nördlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3], # östlicher Bezeichner
            temperature, # östlicher Kleber
            "", # südlicher Bezeichner
            0, # südlicher Kleber
            tile["glues"][3]["label"], # westlicher Bezeichner
            tile["glues"][3]["strength"]-1 if not has_glues["south"] and not has_glues["north"] and has_glues["east"] and tile["glues"][3]["label"] != "" else tile["glues"][3]["strength"], # westlicher Kleber
            tile["color"] # Tile Farbe
        )
    # Fall salmon
    elif tile["color"] == "salmon" or tile["color"] == "#e8bfad":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]] * 3 - 2], # östlicher Bezeichner
            temperature,  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]] * 3 - 1], # südlicher Bezeichner
            1,  # südlicher Kleber
            tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"]-1 if tile["glues"][3]["label"] else tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"] # Tile Farbe
        )
    # Fall red/crimson
    elif tile["color"] == "red" or tile["color"] == "crimson" or tile["color"] == "#e42034" or tile["color"] == "#b51621":
        if not tile["glues"][2]["strength"] is None:
            glue_strength["north"] = max(glue_strength["north"], tile["glues"][2]["strength"])
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2], # östlicher Bezeichner
            temperature,  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # südlicher Bezeichner
            temperature,  # südlicher Kleber
            tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"]-1 if tile["glues"][3]["label"] else tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"] # Tile Farbe
        )
    # Fall skyblue
    elif tile["color"] == "skyblue" or tile["color"] == "#c2d9e6":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"], # nördlicher Bezeichner
            tile["glues"][0]["strength"]-1 if tile["glues"][0]["label"] else tile["glues"][0]["strength"],  # nördlicher Kleber
            "", # östlicher Bezeichner
            0,  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1], # südlicher Bezeichner
            1,  # südlicher Kleber
            tile["glues"][3]["label"], # westlicher Bezeichner
            tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"] # Tile Farbe
        )
    # Fall deepskyblue/royalblue
    elif tile["color"] == "deepskyblue" or tile["color"] == "royalblue" or tile["color"] == "#3ca9d5" or tile["color"] == "#0083ad":
        if not tile["glues"][0]["strength"] is None:
            glue_strength["south"] = max(glue_strength["south"], tile["glues"][0]["strength"])
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            "",  # östlicher Bezeichner
            0,  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # südlicher Bezeichner
            temperature,  # südlicher Kleber
            tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall white/grey
    else:
        # Fall Süden hat Kleber und Norden existiert:
        # 3 2
        # 4 1
        if has_glues["south"] and exists["north"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # östlicher Bezeichner
                max(temperature - (tile["glues"][0]["strength"] if tile["glues"][0]["strength"] else 0), 1),  # östlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # südlicher Bezeichner
                max(temperature - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),  # südlicher Kleber
                tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden hat Kleber und Norden existiert nicht:
        # 3 2
        # 4 1
        elif has_glues["south"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # östlicher Bezeichner
                temperature,  # östlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # südlicher Bezeichner
                max(temperature - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),  # südlicher Kleber
                tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Norden hat Kleber und Süden nicht
        # 2 1
        # 3 4
        elif has_glues["north"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                "",  # östlicher Bezeichner
                0,  # östlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # südlicher Bezeichner
                max(temperature - (tile["glues"][0]["strength"] if tile["glues"][0]["strength"] else 0), 1),  # südlicher Kleber
                tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden UND Norden hat keine Kleber, aber Osten:
        # 2 1
        # 3 4
        else:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # östlicher Bezeichner
                temperature,  # östlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # südlicher Bezeichner
                temperature,  # südlicher Kleber
                tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"]-1 if tile["glues"][3]["label"] else tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )

# 1(2)
# 3 4
# Snaked Proofreading Tile für das Nordöstliche Tile
# tile = Aktuell betrachtetes Tile, auf welchem Proofreading angewendet wird
# has_glues = Dictionary, um Wachstumsrichtung des Tiles abfragen zu können
# temperature = Temperatur des Systems
# glue_strength = Dictionary, um zusätzliche Kleberstärken abfragen zu können, um innere Kleber zu bestimmen
# label_counts = Dictionary, um die Anzahl aller Bezeichner im gesamten Tileset abzubilden und so eindeutige innere Kleberbezeichner erstellen zu können
# label_suffix = Liste von Suffixen für die Kleberbezeichner
# exists = Dictionary mit Information über die Existenz von Grenzen des Moleküls
def snaked_proofreading_north_east(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists):
    # Fall khaki
    if tile["color"] == "khaki" or tile["color"] == "#ecda88":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # südlicher Bezeichner
            temperature,  # südlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # westlicher Bezeichner
            temperature,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall salmon
    elif tile["color"] == "salmon" or tile["color"] == "#e8bfad":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # südlicher Bezeichner
            temperature,  # südlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # westlicher Bezeichner
            temperature,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall red/crimson
    elif tile["color"] == "red" or tile["color"] == "crimson" or tile["color"] == "#e42034" or tile["color"] == "#b51621":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"]-1 if tile["glues"][1]["label"] else tile["glues"][1]["strength"],  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # südlicher Bezeichner
            max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0) + 1, 1),  # südlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # westlicher Bezeichner
            temperature,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall skyblue
    elif tile["color"] == "skyblue" or tile["color"] == "#c2d9e6":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
            tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # südlicher Bezeichner
            temperature,  # südlicher Kleber
            "",  # westlicher Bezeichner
            0,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall deepskyblue/blue
    elif tile["color"] == "deepskyblue" or tile["color"] == "royalblue" or tile["color"] == "#3ca9d5" or tile["color"] == "#0083ad":
        return generate_tile(
            tile["label"],  # Label
            tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
            max(temperature - glue_strength["east"], tile["glues"][0]["strength"]) if has_glues["south"] else tile["glues"][0]["strength"],  # nördlicher Kleber
            tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # südlicher Bezeichner
            max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0) + 1, 1),  # südlicher Kleber
            "",  # westlicher Bezeichner
            0,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall white
    else:
        # Fall Süden hat Kleber und Norden existiert:
        # 3 2
        # 4 1
        if has_glues["south"] and exists["north"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][2]["label"].replace("'","") + "<" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                max(temperature - (tile["glues"][0]["strength"] if tile["glues"][0]["strength"] else 0) - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0), 1),  # südlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # westlicher Bezeichner
                max(temperature - (tile["glues"][0]["strength"] if tile["glues"][0]["strength"] else 0), 1),  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden hat Kleber und Norden existiert nicht:
        # 3 2
        # 4 1
        if has_glues["south"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][2]["label"].replace("'","") + "<" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                max(temperature - (tile["glues"][0]["strength"] if tile["glues"][0]["strength"] else 0) - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0), 1),  # südlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # westlicher Bezeichner
                temperature,  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden hat keine Kleber, aber Norden:
        # 4 1
        # 3 2
        elif has_glues["north"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
                max(temperature - glue_strength["east"], tile["glues"][0]["strength"]),  # nördlicher Kleber
                tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][0]["label"].replace("'", "") + ">" if tile["glues"][0]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0) - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),  # südlicher Kleber
                "",  # westlicher Bezeichner
                0,  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden UND Norden hat keine Kleber, aber Osten:
        # 2 1
        # 3 4
        else:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"] + "'" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
                tile["glues"][0]["strength"],  # nördlicher Kleber
                tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"]-1 if tile["glues"][1]["label"] else tile["glues"][1]["strength"],  # östlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # südlicher Bezeichner
                1,  # südlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # westlicher Bezeichner
                temperature,  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
# 1 2
#(3)4
# Snaked Proofreading Tile für das Südwestliche Tile
# tile = Aktuell betrachtetes Tile, auf welchem Proofreading angewendet wird
# has_glues = Dictionary, um Wachstumsrichtung des Tiles abfragen zu können
# temperature = Temperatur des Systems
# glue_strength = Dictionary, um zusätzliche Kleberstärken abfragen zu können, um innere Kleber zu bestimmen
# label_counts = Dictionary, um die Anzahl aller Bezeichner im gesamten Tileset abzubilden und so eindeutige innere Kleberbezeichner erstellen zu können
# label_suffix = Liste von Suffixen für die Kleberbezeichner
def snaked_proofreading_south_west(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists):
    # Fall khaki
    if tile["color"] == "khaki" or tile["color"] == "#ecda88":
        return generate_tile(
            tile["label"],  # Label
            "",  # nördlicher Bezeichner
            0,  # nördlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # östlicher Bezeichner
            temperature,  # östlicher Kleber
            tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"]-1 if tile["glues"][2]["label"] else tile["glues"][2]["strength"],  # südlicher Kleber
            tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall salmon
    elif tile["color"] == "salmon" or tile["color"] == "#e8bfad":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # nördlicher Bezeichner
            1,  # nördlicher Kleber
            "",  # östlicher Bezeichner
            0,  # östlicher Kleber
            tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"]-1 if tile["glues"][2]["label"] else tile["glues"][2]["strength"],  # südlicher Kleber
            tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall red/crimson
    elif tile["color"] == "red" or tile["color"] == "crimson" or tile["color"] == "#e42034" or tile["color"] == "#b51621":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # nördlicher Bezeichner
            temperature,  # nördlicher Kleber
            "",  # östlicher Bezeichner
            0,  # östlicher Kleber
            tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall skyblue
    elif tile["color"] == "skyblue" or tile["color"] == "#c2d9e6":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # nördlicher Bezeichner
            1,  # nördlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # östlicher Bezeichner
            temperature,  # östlicher Kleber
            tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"]-1 if tile["glues"][3]["label"] else tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall deepskyblue/blue
    elif tile["color"] == "deepskyblue" or tile["color"] == "royalblue" or tile["color"] == "#3ca9d5" or tile["color"] == "#0083ad":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # nördlicher Bezeichner
            temperature,  # nördlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # östlicher Bezeichner
            temperature,  # östlicher Kleber
            tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
            tile["glues"][3]["strength"] - 1 if tile["glues"][3]["label"] else tile["glues"][3]["strength"],  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall white
    else:
        # Fall Süden oder Osten hat Kleber:
        # 3 2
        # 4 1
        if has_glues["south"]:
            return generate_tile(
                tile["label"],  # Label
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # nördlicher Bezeichner
                max(temperature - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),  # nördlicher Kleber
                "",  # östlicher Bezeichner
                0,  # östlicher Kleber
                tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Norden hat Kleber und Süden hat keine Kleber, existiert aber.
        # 4 1
        # 3 2
        elif has_glues["north"] and exists["south"]:
            return generate_tile(
                tile["label"],  # Label
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # nördlicher Bezeichner
                max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0), 1),  # nördlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # östlicher Bezeichner
                max(temperature - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),   # östlicher Kleber
                tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Norden hat Kleber und Süden hat keine Kleber und existiert auch nicht.
        # 4 1
        # 3 2
        elif has_glues["north"]:
            return generate_tile(
                tile["label"],  # Label
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # nördlicher Bezeichner
                max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0), 1),  # nördlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # östlicher Bezeichner
                temperature,  # östlicher Kleber
                tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden UND Norden hat keine Kleber, aber Osten:
        # 2 1
        # 3 4
        else:
            return generate_tile(
                tile["label"],  # Label
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # nördlicher Bezeichner
                temperature,  # nördlicher Kleber
                "",  # östlicher Bezeichner
                0,  # östlicher Kleber
                tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                tile["glues"][3]["label"] + "'" if tile["glues"][3]["label"] else tile["glues"][3]["label"],  # westlicher Bezeichner
                tile["glues"][3]["strength"],  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )

# 1 2
# 3(4)
# Snaked Proofreading Tile für das Südöstliche Tile
# tile = Aktuell betrachtetes Tile, auf welchem Proofreading angewendet wird
# has_glues = Dictionary, um Wachstumsrichtung des Tiles abfragen zu können
# temperature = Temperatur des Systems
# glue_strength = Dictionary, um zusätzliche Kleberstärken abfragen zu können, um innere Kleber zu bestimmen
# label_counts = Dictionary, um die Anzahl aller Bezeichner im gesamten Tileset abzubilden und so eindeutige innere Kleberbezeichner erstellen zu können
# label_suffix = Liste von Suffixen für die Kleberbezeichner
# exists = Dictionary mit Information über die Existenz von Grenzen des Moleküls
def snaked_proofreading_south_east(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists):
    # Fall khaki
    if tile["color"] == "khaki" or tile["color"] == "#ecda88":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # nördlicher Bezeichner
            temperature,  # nördlicher Kleber
            tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-1],  # westlicher Bezeichner
            temperature,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall salmon
    elif tile["color"] == "salmon" or tile["color"] == "#e8bfad":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # nördlicher Bezeichner
            temperature,  # nördlicher Kleber
            tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            "",  # westlicher Bezeichner
            0,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall red/crimson
    elif tile["color"] == "red" or tile["color"] == "crimson" or tile["color"] == "#e42034" or tile["color"] == "#b51621":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # nördlicher Bezeichner
            max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0) + 1,1),  # nördlicher Kleber
            tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
            max(temperature - glue_strength["east"], tile["glues"][2]["strength"]) if not has_glues["south"] and has_glues["north"] else tile["glues"][2]["strength"],  # südlicher Kleber
            "",  # westlicher Bezeichner
            0,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall skyblue
    elif tile["color"] == "skyblue" or tile["color"] == "#c2d9e6":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # nördlicher Bezeichner
            temperature,  # nördlicher Kleber
            tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"],  # östlicher Kleber
            tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # westlicher Bezeichner
            temperature,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall deepskyblue/blue
    elif tile["color"] == "deepskyblue" or tile["color"] == "royalblue" or tile["color"] == "#3ca9d5" or tile["color"] == "#0083ad":
        return generate_tile(
            tile["label"],  # Label
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # nördlicher Bezeichner
            max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0) + 1, 1),  # nördlicher Kleber
            tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
            tile["glues"][1]["strength"]-1 if tile["glues"][1]["label"] else tile["glues"][1]["strength"],  # östlicher Kleber
            tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
            tile["glues"][2]["strength"],  # südlicher Kleber
            tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-2],  # westlicher Bezeichner
            temperature,  # westlicher Kleber
            tile["color"]  # Tile Farbe
        )
    # Fall white
    else:
        # Fall Süden hat Kleber:
        # 3 2
        # 4 1
        if has_glues["south"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][2]["label"].replace("'", "") + "<" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # nördlicher Bezeichner
                max(temperature - (tile["glues"][0]["strength"] if tile["glues"][0]["strength"] else 0) - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0), 1),  # nördlicher Kleber
                tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                max(temperature - glue_strength["east"], tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0),  # südlicher Kleber
                "",  # westlicher Bezeichner
                0,  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Norden hat Kleber und Süden hat keine Kleber, existiert aber:
        # 4 1
        # 3 2
        elif has_glues["north"] and exists["south"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"].replace("'", "") + ">" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
                max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0) - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),  # nördlicher Kleber
                tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # westlicher Bezeichner
                max(temperature - (tile["glues"][2]["strength"] if tile["glues"][2]["strength"] else 0), 1),  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Norden hat Kleber und Süden hat keine Kleber und existiert nicht:
        # 4 1
        # 3 2
        elif has_glues["north"]:
            return generate_tile(
                tile["label"],  # Label
                tile["glues"][0]["label"].replace("'", "") + ">" if tile["glues"][0]["label"] else tile["glues"][0]["label"],  # nördlicher Bezeichner
                max(temperature - (tile["glues"][1]["strength"] if tile["glues"][1]["strength"] else 0), 1),  # nördlicher Kleber
                tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # westlicher Bezeichner
                temperature,  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )
        # Fall Süden UND Norden hat keine Kleber, aber Osten:
        # 2 1
        # 3 4
        else:
            return generate_tile(
                tile["label"],  # Label
                tile["label"].lower() + label_suffix[label_counts[tile["label"]]*3-3],  # nördlicher Bezeichner
                1,  # nördlicher Kleber
                tile["glues"][1]["label"] + "'" if tile["glues"][1]["label"] else tile["glues"][1]["label"],  # östlicher Bezeichner
                tile["glues"][1]["strength"],  # östlicher Kleber
                tile["glues"][2]["label"] + "'" if tile["glues"][2]["label"] else tile["glues"][2]["label"],  # südlicher Bezeichner
                tile["glues"][2]["strength"],  # südlicher Kleber
                "",  # westlicher Bezeichner
                0,  # westlicher Kleber
                tile["color"]  # Tile Farbe
            )

# Fügt eine weitere Flag hinzu
def add_flag():
    # inkrementiere den Flag Counter
    global flag_counter
    flag_counter += 1
    # erstelle ein Label, ein Eingabefeld und einen Removebutton für die neue Flag
    label = tk.Label(root, text=f"Flag {flag_counter}:")
    label.grid(row=20 + flag_counter, column=0)
    entry = tk.Entry(root)
    entry.grid(row=20 + flag_counter, column=1)
    remove_button = tk.Button(root, text="-", command=lambda e=entry: remove_flag(e))
    remove_button.grid(row=20 + flag_counter, column=2)
    # füge Label, Flag und Remove Button in der Liste hinzu
    flag_labels.append(label)
    flag_entries.append(entry)
    flag_remove_buttons.append(remove_button)
    # lösche den alten "+"-Button und erstelle einen neuen unter der neusten Flag
    add_button.grid_forget()
    add_button.grid(row=21 + flag_counter, column=1)

# Enfernt eine bestimmte Flag
def remove_flag(entry):
    # dekrementiere den Flag Counter
    global flag_counter
    flag_counter -= 1
    # nimm den Index der jeweiligen Flag und lösche Label, Eingabefeld und removebutton
    idx = flag_entries.index(entry)
    flag_labels[idx].grid_forget()
    flag_entries[idx].grid_forget()
    flag_remove_buttons[idx].grid_forget()
    # lösche Label, Flag und Remove Button aus den jeweiligen Liste
    del flag_labels[idx]
    del flag_entries[idx]
    del flag_remove_buttons[idx]
    # Update der Labels
    for i, label in enumerate(flag_labels):
        label.config(text=f"Flag {i + 1}:")
    # Update des Grids nachdem die Listen angepasst wurden
    update_flag_labels_and_buttons()
    # lösche den alten "+"-Button und erstelle einen neuen auf der gelöschten Flag
    add_button.grid_forget()
    add_button.grid(row=21 + flag_counter, column=1)

# Update, wenn Flag hinzugefügt oder entfernt wird
def update_flag_labels_and_buttons():
    for i, entry in enumerate(flag_entries):
        # Update Labels
        flag_labels[i].grid(row=21 + i, column=0)
        # Update Eingabefelder
        entry.grid(row=21 + i, column=1)
        # Update Remove Buttons
        flag_remove_buttons[i].grid(row=21 + i, column=2)
    # Update "+"-Button
    add_button.grid(row=22 + flag_counter, column=1)

# Toggle für die Flag Label, Eingabefelder und Buttons, wenn die Flag Checkbox geklickt wird
def toggle_flags_checkbox():
    if flags_var.get():
        add_button.grid(row=21, column=1)
    else:
        for label in flag_labels:
            label.grid_forget()
        for entry in flag_entries:
            entry.grid_forget()
        for btn in flag_remove_buttons:
            btn.grid_forget()
        flag_labels.clear()
        flag_entries.clear()
        flag_remove_buttons.clear()
        global flag_counter
        flag_counter = 0
        add_button.grid_forget()
#    update_molecule_height()

# def ensure_one_checked():
#    global previous_molecule_height
    # Wenn der aktuelle Wert 0 ist (keine Checkbox aktiviert)
#    if molecule_height.get() == 0:
#        molecule_height.set(previous_molecule_height)
#    else:
#        # Update der previous_molecule_height Variable, wenn sich der Wert ändert
#        previous_molecule_height = molecule_height.get()

#def update_molecule_height():
#    if (flags_var.get() or priority_var.get()) and not coding_checkbox.get():
#        molecule_height_label.grid(row=17, column=0)
#        molecule_height_checkbox_1.grid(row=17, column=1, sticky="w")
#        molecule_height_checkbox_2.grid(row=17, column=1, sticky="s")
#        molecule_height_checkbox_3.grid(row=17, column=1, sticky="e")
#    else:
#        molecule_height_label.grid_forget()
#        molecule_height_checkbox_1.grid_forget()
#        molecule_height_checkbox_2.grid_forget()
#        molecule_height_checkbox_3.grid_forget()
#    molecule_height.trace_add("write", lambda *args: ensure_one_checked())

# Überprüft, ob die Farbe des Tiles korrekt ist
# color = gegebener String, der eine korrekte Farbe beinhalten sollte
# color_code = True, wenn Hex Color Code; False, wenn Named Color Code
def check_color(color, color_code):
    valid_colors_hex = ["white", "#e8bfad","#b51621","#e42034","#c2d9e6","#3ca9d5","#0083ad","#ecda88","#0000","#95bc0e", "#3bb2a0"]
    valid_colors_named = ["khaki", "red", "salmon", "crimson", "deepskyblue", "royalblue", "skyblue", "white", "lightgreen","turquoise"]
    if color_code and color not in valid_colors_hex:
        raise ValueError("Ungültiges Colorcoding. Ausgewähltes Color Coding: HEX. Gültige Optionen sind: '#0000', '#e8bfad', '#b51621', '#e42034', '#c2d9e6', '#3ca9d5', '#0083ad', '#ecda88','white'.")
    elif not color_code and color not in valid_colors_named:
        raise ValueError("Ungültiges Colorcoding. Ausgewähltes Color Coding: NAMEN. Gültige Optionen sind: 'khaki', 'crimson', 'red', 'salmon', 'deepskyblue', 'skyblue', 'royalblue', 'white'")

# Setze Dictionary Einträge, um die Wachstumsrichtung des Moleküls bestimmen zu können
# tile = gegebenes Tile
# has_glues = zu veränderndes Dictionary (wenn ein Tile der entsprechenden Farbe keinen Kleber hat, kann es nicht als Wachstumsfronst verwendet werden
# exists = zu veränderndes Dictionary (existieren Tiles, deren Kleber gecheckt werden können)zu veränderndes Dictionary
def check_growth(tile, has_glues, exists):
    # has_glues Check
    if (tile["color"] == "khaki" or tile["color"] == "#ecda88") and not tile["glues"][3]["strength"]:
        has_glues["east"] = False
    elif (tile["color"] == "deepskyblue" or tile["color"] == "#3ca9d5") and not tile["glues"][0]["strength"]:
        has_glues["south"] = False
    elif (tile["color"] == "red" or tile["color"] == "#b51621") and not tile["glues"][2]["strength"]:
        has_glues["north"] = False
    # exists check
    if tile["color"] == "khaki" or tile["color"] == "#ecda88":
        exists["east"] = True
    elif tile["color"] == "deepskyblue" or tile["color"] == "#3ca9d5":
        exists["south"] = True
    elif tile["color"] == "red" or tile["color"] == "#e42034":
        exists["north"] = True

# Hilfsfunktion, um das has_glues Dictionary zu aktualisieren, wenn bestimmte Tiles nicht existieren
# has_glues: zu veränderndes Dictionary
# exists: Dictionary zum gegenchecken
def check_existance(has_glues, exists):
    if not exists["north"]:
        has_glues["north"] = False
    if not exists["east"]:
        has_glues["east"] = False
    if not exists["south"]:
        has_glues["south"] = False

# Funktion die sicherstellt, dass nur eine der Color Schema Checkboxen ausgewählt ist
def only_one(var, value):
    if value:
        if var is color_hex:
            color_named.set(False)
        else:
            color_hex.set(False)
    else:  # Wenn versucht wird, die Checkbox zu deaktivieren
        if var is color_hex and not color_named.get():
            color_hex.set(True)
        elif var is color_named and not color_hex.get():
            color_named.set(True)

# Toggle für die nötigen Eingabefelder beim checken der Coding Checkbox
def toggle_coding_checkbox():
    if coding_checkbox.get():
        file_entry.config(state=tk.DISABLED)
        file_button.config(state=tk.DISABLED)
        color_hex_cb.config(state=tk.DISABLED)
        color_named_cb.config(state=tk.DISABLED)
        color_hex.set(False)
        color_named.set(False)
        checksum_label.grid(row=3, column=1)
        checksum_checkbox.grid(row=3, column=1, sticky="e")
        message_count_entry.grid(row=4, column=1)
        message_count_label.grid(row=4, column=0)
        tileset_weight_entry.grid(row=5, column=1)
        tileset_weight_label.grid(row=5, column=0)
        assembly_weight_entry.grid(row=6, column=1)
        assembly_weight_label.grid(row=6, column=0)
    else:
        file_entry.config(state=tk.NORMAL)
        file_button.config(state=tk.NORMAL)
        color_hex_cb.config(state=tk.NORMAL)
        color_named_cb.config(state=tk.NORMAL)
        color_hex.set(True)
        color_named.set(False)
        checksum_label.grid_remove()
        checksum_checkbox.grid_remove()
        message_count_entry.grid_remove()
        message_count_label.grid_remove()
        tileset_weight_entry.grid_remove()
        tileset_weight_label.grid_remove()
        assembly_weight_entry.grid_remove()
        assembly_weight_label.grid_remove()
#    update_molecule_height()

# Toggle für das Priorität Eingabefeld beim checken der Priorität Checkbox
def toggle_priority_checkbox():
    if priority_var.get():
        priority_level_label.grid(row=19, column=0, padx=5, pady=5)
        priority_level_entry.grid(row=19, column=1, padx=5, pady=5)
    else:
        priority_level_label.grid_remove()
        priority_level_entry.grid_remove()
#    update_molecule_height()

# Generiert ein Tile im NetTAS
# tile_label = Bezeichner des Tiles
# label1 = nördliches Kleberlabel
# strength1 = nördliche Kleberstärke
# label2 = östliches Kleberlabel
# strength2 = östliche Kleberstärke
# label3 = südliches Kleberlabel
# strength3 = südliche Kleberstärke
# label4 = westliches Kleberlabel
# strength4 = westliche Kleberstärke
# color = Farbe des Tiles
def generate_tile(tile_label, label1, strength1, label2, strength2, label3, strength3, label4, strength4, color):
    return {
        "label": tile_label,
        "glues": [
            {"label": label1, "strength": strength1},
            {"label": label2, "strength": strength2},
            {"label": label3, "strength": strength3},
            {"label": label4, "strength": strength4},
        ],
        "color": color
    }

# Generiert Flag- oder Prioritätstiles je nachdem welche Höhe das betrachtete Molekül hat
# idx = aktueller Index in der Schleife, um eindeutige Bezeichner zu garantieren
# name = Label der Flag oder der Priorität
# width = Breite der Tiles im Molekül (z.B. 3, wenn 2 Flagtiles und Priotiles vorhanden)
# temp = Temperatur des Systems
# strengths = Dictionary für Bezeichner und Stärke der westlichen Kleber des Starts des Moleküls
# labels = Bezeichnerliste
# hex = True -> Color Coding durch Hex dargestellt, False -> Color Coding durch Namen dargestellt
# flag = True -> Flag; flag = False -> Prio Tile
def generate_flag_or_prio_tile(idx, name, width, temp, strengths, labels, hex, flag):
    fp_tiles = []
    name = str(name)
    # Höhe 3
    if not strengths["khaki"][0] == -1 and not strengths["salmon"][0] == -1 and not strengths["skyblue"][0] == -1:
        if width == 1: # nur ein Tile
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name, # Label
                    "", 0, # nördlicher Kleber
                    "σt", strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    strengths["salmon"][1], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],   # östlicher Kleber
                    "2" + name[0].upper(), temp,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negativ Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],   # östlicher Kleber
                        "2" + name[0].upper(), temp,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "2" + name[0].upper(), temp,  # nördlicher Kleber
                    "σb", strengths["skyblue"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["skyblue"][1], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue" # Farbe
                )
            )
        elif idx == 0: # erstes Tile neben Seed Tile
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    "σt", strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    labels[3*idx], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],   # östlicher Kleber
                    "2" + name[0].upper(), temp,  # südlicher Kleber
                    labels[3*idx+1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negativ Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],   # östlicher Kleber
                        "2" + name[0].upper(), temp,  # südlicher Kleber
                        labels[3*idx+1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "2" + name[0].upper(), temp,  # nördlicher Kleber
                    "σb", strengths["skyblue"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[3*idx+2], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue" # Farbe
                )
            )
        elif idx == width-1: # Letztes Tile neben restlichem Molekül
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    labels[3*(idx-1)], strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    strengths["salmon"][1], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[3*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                    "2" + name[0].upper(), temp,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negatives Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        labels[3*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                        "2" + name[0].upper(), temp,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "2" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[3*(idx-1)+2], strengths["skyblue"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["skyblue"][1], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue" # Farbe
                )
            )
        else: # ab 3 Flags/Prio Tiles innere Tiles
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    labels[3*(idx-1)], strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    labels[3*idx], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[3*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                    "2" + name[0].upper(), temp,  # südlicher Kleber
                    labels[3*idx+1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negatives Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        labels[3*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                        "2" + name[0].upper(), temp,  # südlicher Kleber
                        labels[3*idx+1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "2" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[3*(idx-1)+2], strengths["skyblue"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[3*idx+2], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue" # Farbe
                )
            )
    # Höhe 2 - nördlicher Rand
    elif not strengths["salmon"][0] == -1 and not strengths["khaki"][0] == -1:
        if width == 1:  # nur ein Tile
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    "σt", strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    strengths["salmon"][1], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],   # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # südliches negatives Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],   # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
        elif idx == 0:  # erstes Tile neben Seed Tile
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    "σt", strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    labels[2*idx], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],   # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[2*idx+1], strengths["khaki"][0],  # westlicher Kleber
                    "#95bc0e" if flag else "#3bb2a0" # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # südliches negatives Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],   # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        labels[2*idx+1], strengths["khaki"][0],  # westlicher Kleber
                        "#95bc0e" if flag else "#3bb2a0" # Farbe
                    )
                )
        elif idx == width-1:  # Letztes Tile neben restlichem Molekül
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    labels[2*(idx-1)], strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    strengths["salmon"][1], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[2*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # südliches negatives Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        labels[2*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
        else:  # ab 3 Flags/Prio Tiles innere Tiles
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0, # nördlicher Kleber
                    labels[2*(idx-1)], strengths["salmon"][0], # östlicher Kleber
                    "1" + name[0].upper(), temp, # südlicher Kleber
                    labels[2*idx], strengths["salmon"][0], # westlicher Kleber
                    "#e42034" if hex else "red" # Farbe
                )
            )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[2*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[2*idx+1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # südliches negatives Flagtile
                        "!" + name,  # Label
                        "1" + name[0].upper(), temp,  # nördlicher Kleber
                        labels[2*(idx-1)+1], strengths["khaki"][0],   # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        labels[2*idx+1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
    # Höhe 2 - südlicher Rand
    elif not strengths["skyblue"][0] == -1 and not strengths["khaki"][0] == -1:
        if width == 1:  # nur ein Tile
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],   # östlicher Kleber
                    "1" + name[0].upper(), temp,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # nördliches negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],   # östlicher Kleber
                        "1" + name[0].upper(), temp,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    "σb", strengths["skyblue"][0],   # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["skyblue"][1], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue" # Farbe
                )
            )
        elif idx == 0:  # erstes Tile neben Seed Tile
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],   # östlicher Kleber
                    "1" + name[0].upper(), temp,  # südlicher Kleber
                    labels[2*idx], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # nördliches negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],   # östlicher Kleber
                        "1" + name[0].upper(), temp,  # südlicher Kleber
                        labels[2*idx], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    "σb", strengths["skyblue"][0],   # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[2*idx+1], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue" # Farbe
                )
            )
        elif idx == width-1:  # Letztes Tile neben restlichem Molekül
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    labels[2*(idx-1)], strengths["khaki"][0],   # östlicher Kleber
                    "1" + name[0].upper(), temp,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # nördliches negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        labels[2*(idx-1)], strengths["khaki"][0],   # östlicher Kleber
                        "1" + name[0].upper(), temp,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise") # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[2*(idx-1)+1], strengths["skyblue"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["skyblue"][1], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue"  # Farbe
                )
            )
        else:  # ab 3 Flags/Prio Tiles innere Tiles
            fp_tiles.append(
                generate_tile( # nördliches Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    labels[2*(idx-1)], strengths["khaki"][0],  # östlicher Kleber
                    "1" + name[0].upper(), temp,  # südlicher Kleber
                    labels[2*idx], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # nördliches negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        labels[2*(idx-1)], strengths["khaki"][0],  # östlicher Kleber
                        "1" + name[0].upper(), temp,  # südlicher Kleber
                        labels[2*idx], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                    )
                )
            fp_tiles.append(
                generate_tile( # südliches Tile
                    name,  # Label
                    "1" + name[0].upper(), temp,  # nördlicher Kleber
                    labels[2*(idx-1)+1], strengths["skyblue"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[2*idx+1], strengths["skyblue"][0],  # westlicher Kleber
                    "#3ca9d5" if hex else "deepskyblue"  # Farbe
                )
            )
    # Höhe 1
    elif not strengths["khaki"][0] == -1:
        if width == 1:  # nur ein Tile
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negatives Tile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],  # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                    )
                )
        elif idx == 0:  # erstes Tile neben Seed Tile
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    "σc", strengths["khaki"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[idx], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        "σc", strengths["khaki"][0],  # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        labels[idx], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                    )
                )
        elif idx == width-1:  # Letztes Tile neben restlichem Molekül
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    labels[idx-1], strengths["khaki"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        labels[idx-1], strengths["khaki"][0],  # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        strengths["khaki"][1], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                    )
                )
        else:  # ab 3 Flags/Prio Tiles innere Tiles
            fp_tiles.append(
                generate_tile( # zentrales Tile
                    name,  # Label
                    "", 0,  # nördlicher Kleber
                    labels[idx-1], strengths["khaki"][0],  # östlicher Kleber
                    "", 0,  # südlicher Kleber
                    labels[idx], strengths["khaki"][0],  # westlicher Kleber
                    ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                )
            )
            if flag:
                fp_tiles.append(
                    generate_tile( # zentrales negatives Flagtile
                        "!" + name,  # Label
                        "", 0,  # nördlicher Kleber
                        labels[idx-1], strengths["khaki"][0],  # östlicher Kleber
                        "", 0,  # südlicher Kleber
                        labels[idx], strengths["khaki"][0],  # westlicher Kleber
                        ("#95bc0e" if flag else "#3bb2a0") if hex else ("lightgreen" if flag else "turquoise")  # Farbe
                    )
                )
    return fp_tiles

# Hilfsfunktion, um die Farbe der Tiles je nach color_code abzuändern
# tile = ein einzelnes übergebenes Tile
def change_colors(tile, color_code):
    frame_tile_colors = ["#ecda88", "khaki", "#e8bfad", "salmon", "#b51621", "crimson", "#c2d9e6", "skyblue", "#0083ad", "royalblue"]
    flag_prio_tile_colors = ["#3bb2a0", "turquoise", "#95bc0e", "lightgreen"]
    if tile["color"] in frame_tile_colors:
        tile["color"] = "#67939c" if color_code else "cadetblue"
    elif tile["color"] in flag_prio_tile_colors:
        tile["color"] = tile["color"]
    else:
        tile["color"] = "white"
    return tile

# Hilfsfunktion, um die Anzahl der Ziffern für eine Zahl num zur Basis base zu erhalten
# num = angegebener integer aus der Basis 10 (Dezimalzahl)
# base = Basis
def get_digits(num, base):
    if base == 1:
        return num
    if num == 0:
        return 1
    return math.ceil(math.log(num, base))


# ermittelt die effizienteste Basis zu einer angegeben Zahl anhand von Gewichtungen
# num = angegebener integer aus der Basis 10 (Dezimalzahl)
# weight1 = Gewichtung für die Anzahl der Tiles im Tileset
# weight2 = Gewichtung für die Anzahl der Tiles in der Assembly
# chksm = True, wenn Checksumme erstellt wird
def find_best_base(num, weight1, weight2, chksm):
    best_base = 2
    best_score = float('inf')

    # suche das beste Basissystem (maximal 36, da dann 0-Z verwendet wird) minimal binär
    for base in range(2, min(num + 1, 36)):
        # Anzahl der Ziffern nach Zahl und Basis
        y = get_digits(num, base)
        # Anzahl der Tiles im Tileset
        xy1 = sum(base**d for d in range(1, y + 1)) + base**y + 1 if chksm else base * y + 1
        # xy1 = base * y + 1
        # Anzahl der Tiles in der Assembly
        y1 = y + 1
        score = weight1 * xy1 + weight2 * y1
        if score < best_score:

            best_score = score
            best_base = base        
    return best_base


# Generiert Tileset für Assembly der Höhe 1 entsprechend des message_count und den Gewichtungen
# message_count: Anzahl der Nachrichten, welche durch das Tileset abbildbar sein sollen
# temperature: die Temperatur des Systems
# tileset_weight: Gewichtung für die Anzahl der Tiles im Tileset
# assembly_weight: Gewichtung für die Anzahl der Tiles in der Assembly
def generate_data(message_count, temperature, tileset_weight, assembly_weight):
    tiles = []
    # finde optimale Basis und daraus resultierende Anzahl der Ziffern
    base = find_best_base(message_count, tileset_weight, assembly_weight, False)
    digits = get_digits(message_count, base)
    # Liste für die Labels [0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F,G,H,I,J,...]
    labels = list(string.digits + string.ascii_uppercase)
    glue_labels = string.ascii_lowercase
    # Seed Tile
    tiles.append(generate_tile("σ", "", 0, "", 0, "", 0, glue_labels[0], temperature, "#ecda88"))
    # restliche Tiles
    for digit in range(1, digits+1):
        for i in range(0, base):
            tiles.append(generate_tile(labels[i], "", 0, glue_labels[digit-1], temperature, "", 0, glue_labels[digit], temperature, "white"))
    # Letztes Tile mit Liganden
    tiles.append(
        generate_tile("ω", "adr", 1, glue_labels[digit], temperature, "adr", 1, "", 0, "white"))
    return {"_tiles": tiles}

# Rekursive Funktion, um alle notwenigen Tiles für Checksummen zu erstellen
# base = Die Zahlenbasis
# digit = die aktuell betrachtete Ziffernstelle
# temperature = die Temperatur des Systems
# labels = Liste für darstellung von höheren Basissystemen
# glue_label = Kleberbezeichner
def generate_data_recursive(base, digit, temperature, labels, glue_label):
    temp_tiles = []
    if digit == 1:
        for i in range(base):
            temp_tiles.append(generate_tile(
                labels[i],
                "", 0,
                glue_label, temperature,
                "", 0,
                labels[i] + glue_label, temperature,
                "white"
                )
            )
    else:
        for i in range(base):
            temp_tiles.extend(generate_data_recursive(base,digit-1,temperature,labels,labels[i]+glue_label))
    return temp_tiles

# erstellt für Basis und Ziffernzahl die Liste von allen Zahlen
# base = Zahlenbasis
# digits = Anzahl der Ziffern
def generate_formatted_numbers(base, digits):
    numbers = []
    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    max_num = base ** digits
    for num in range(max_num):
        result = ""
        temp_num = num
        while temp_num:
            result = chars[temp_num % base] + result
            temp_num //= base

        # Führende Nullen hinzufügen, um die gewünschte Länge zu erreichen
        while len(result) < digits:
            result = '0' + result

        numbers.append(result or '0')
    return numbers

# Generiert Tileset analog zu "generate_data_based_on_message_count", aber mit Checksumme am Ende des Moleküls
# message_count: Anzahl der Nachrichten, welche durch das Tileset abbildbar sein sollen
# temperature: die Temperatur des Systems
# tileset_weight: Gewichtung für die Anzahl der Tiles im Tileset
# assembly_weight: Gewichtung für die Anzahl der Tiles in der Assembly
def generate_data_with_checksum(message_count, temperature, tileset_weight, assembly_weight):
    tiles = []
    # finde optimale Basis und daraus resultierende Anzahl der Ziffern
    base = find_best_base(message_count, tileset_weight, assembly_weight, True)
    digits = get_digits(message_count, base)
    labels = list(string.digits + string.ascii_uppercase)
    all_nums = generate_formatted_numbers(base, digits)
    # Seed Tile
    tiles.append(generate_tile("σ", "", 0, "", 0, "", 0, "σ", temperature, "#ecda88"))
    # erste Stelle
    for i in range(base):
        tiles.append(generate_tile(
            labels[i],
            "", 0,
            "σ", temperature,
            "", 0,
            labels[i], temperature,
            "white"
            )
        )
    # Rekursion für mehr stellen
    for digit in range(2, digits + 1):
        tiles.extend(generate_data_recursive(base, digit, temperature, labels, ""))
    # Checksummentiles erstellen
    for num in all_nums:
        tiles.append(generate_tile(
            num,
            "adr", 1,
            num, temperature,
            "adr", 1,
            "", 0,
            "white"
            )
        )
    return {'_tiles': tiles}


# Definition der Funktion zur Auswahl der Datei
def select_file():
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_name)

##############################################################################################################################

#
#
#  MAIN
#
#
# Definition der Hauptfunktion
# data = Datensatz
# temperature = Systemtemperatue
# color_code = True, wenn HTML; False, wenn CSS
# color_kept = True, wenn Colorcode erhalten bleiben soll
# flags = Liste von Flags
# priority = Prioritätslevel
# proofreading = True, wenn proofreading durchgeführt werden soll
# eval = nur für Evaluation benötigt
def main(data, temperature, color_code, color_kept, flags, priority, proofreading, eval):
    # Neue "_tiles"-Liste für die Ausgabe erstellen
    new_tiles = []
    # true, wenn alle Tiles in den jeweiligen Richtungen mindestens eine Kleberstärke > 0 haben
    has_glues = {
        "east": True,
        "south": True,
        "north": True
    }
    # true, wenn mindestens ein Tile in den jeweiligen Richtungen existiert
    exists = {
        "north": False,
        "south": False,
        "east": False
    }
    # Stärke von:
    # Seed (East) links
    # Südliche Grenze oben
    # Nördliche Grenze unten
    glue_strength = {
        "east": 0,
        "south": 0,
        "north": 0
    }

    # Stärke und Bezeichner der "Start-Tiles"
    strengths = {
        "khaki": (-1, ""),
        "salmon": (-1, ""),
        "skyblue": (-1, "")
    }

    # Setup 1
    # Sammle Informationen über den Molekülstart und -höhe, für Flags und Priorität-Tiles
    # und überschreibe Labels, wenn Flag- oder Prioritätstiles hinzugefügt werden sollen
    for tile in data['_tiles']:
        if tile["color"] == "khaki" or tile["color"] == "#ecda88":
            strengths["khaki"] = (tile['glues'][3]['strength'], tile['glues'][3]['label'])
            if flags or priority:
                tile['glues'][3]['label'] = "σc"
        elif tile["color"] == "salmon" or tile["color"] == "#e8bfad":
            strengths["salmon"] = (tile['glues'][3]['strength'], tile['glues'][3]['label'])
            if flags or priority:
                tile['glues'][3]['label'] = "σt"
        elif tile["color"] == "skyblue" or tile["color"] == "#c2d9e6":
            strengths["skyblue"] = (tile['glues'][3]['strength'], tile['glues'][3]['label'])
            if flags or priority:
                tile['glues'][3]['label'] = "σb"

    if flags or priority:
        # Upper Case Bezeichner für Flags und Prios, um Fehler vorzubeugen.
        uppercase_glue_labels = list(string.ascii_uppercase)
        # Sicher stellen, dass genügend Bezeichner vorhanden sind
        # resultierende Liste: (A,B,C,...,X,Y,Z,AA,AB,AC,...,ZX,ZY,ZZ)
        for first_char in string.ascii_uppercase:
            for second_char in string.ascii_uppercase:
                uppercase_glue_labels.append(first_char + second_char)
        # seperater Index, da er in zwei Schleifen gebraucht, aber nur in einer inkrementiert wird
        label_idx = 0
        # Menge von gleichzeitigen Tiles im finalen Molekül
        width = len(flags) + (1 if priority else 0)

    if flags:
        for flag in flags:
            # Höhe 3
            data['_tiles'].extend(generate_flag_or_prio_tile(label_idx, str(flag) + "f", width, temperature, strengths, uppercase_glue_labels, color_code, True))
            label_idx += 1

    if priority:
        for prio in range(1, int(priority)+1):
            # width = label_idx + 1, damit dieses Tile entweder immer in den width = 1 oder idx = width - 1 Cases geht
            data['_tiles'].extend(generate_flag_or_prio_tile(label_idx, str(prio) + "p", label_idx+1, temperature, strengths, uppercase_glue_labels, color_code, False))

    # Nach Farben sortieren, um einige zusätzliche Infos verwenden zu können
    color_order_hex = ["#ecda88", "#e8bfad", "#c2d9e6", "#e42034", "#3ca9d5", "#0000", "white", "#b51621",
                       "#0083ad", "#95bc0e", "#3bb2a0"]
    color_order_named = ["khaki", "salmon", "skyblue", "red", "deepskyblue", "white", "crimson", "royalblue",
                         "lightgreen", "turquoise"]

    if color_code:
        data['_tiles'].sort(key=lambda x: color_order_hex.index(x['color']))
    else:
        data['_tiles'].sort(key=lambda x: color_order_named.index(x['color']))

    # Wenn Proofreading aktiviert wurde, wende 2x2 snaked proofreading an ...
    if proofreading:
        # Jedes Tile-Label Vorkommen zählen
        label_counts = {}
        # Suffixe für innere Verbindungen
        label_suffix = list(string.digits + string.ascii_lowercase)
        # Sicher stellen, dass genügend Bezeichner vorhanden sind (auch für Checksummen Dinge)
        # resultierende Liste: (0,1,2,...,7,8,9,a,b,c,...,x,y,z,aa,ab,ac,...,zx,zy,zz,aaa,...,zzz)
        for first_char in string.ascii_lowercase:
            for second_char in string.ascii_lowercase:
                label_suffix.append(first_char + second_char)
                for third_char in string.ascii_lowercase:
                    label_suffix.append(first_char + second_char + third_char)
        # Setup 2:
        # 1. Color Coding überprüfen
        # 2. Check, ob die weißen Tiles von Norden oder von Süden starten müssen
        # 3. Jedes Tile-Label Vorkommen zählen
        for tile in data['_tiles']:
            # 1.
            check_color(tile["color"], color_code)
            # 2.
            check_growth(tile, has_glues, exists)
            # 3.
            label = tile['label']
            label_counts[label] = label_counts.get(label, 0) + 1

        check_existance(has_glues, exists)
        if all(value == False for value in has_glues.values()):
            raise ValueError(
                "Für Konstruktion werden Kleber für folgende farbige Tiles benötigt: 'red','khaki' oder 'deepskyblue'")
        for tile in data['_tiles']:
            # Snaked Proofreading auf das Tile anwenden
            # 1 2
            # 3 4
            # Tile 1 (hier die Glue Strength updaten)
            new_tiles.append(snaked_proofreading_north_west(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists))
            # Tile 2
            new_tiles.append(snaked_proofreading_north_east(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists))
            # Tile 3
            new_tiles.append(snaked_proofreading_south_west(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists))
            # Tile 4
            new_tiles.append(snaked_proofreading_south_east(tile, has_glues, temperature, glue_strength, label_counts, label_suffix, exists))
            # Count verringern
            label_counts[tile["label"]] -= 1
    # ... Wenn nicht, dann übernimm die originalen Tiles in der Ausgabemenge
    else:
        for tile in data['_tiles']:
            # ohne Proofreading werden die originalen Tiles übernommen
            new_tiles.append(tile)

    # entferne den Color Code, wenn die Checkbox nicht ausgewählt wurde, um den Color Code zu behalten
    if not color_kept:
        new_tiles = [change_colors(tile, color_code) for tile in new_tiles]

    if eval:
        return len(new_tiles)
    else:
        # Ausgabe zurückgeben
        return {"_tiles": new_tiles}

#
#
#   Programm Start
#
#
# Start Funktion des Programms
def start_program():
    try:
        output_file = output_entry.get()
        if not output_file:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Namen für die Ausgabedatei ein.")
            return
        temperature = temp_entry.get()
        if not temperature.isdigit():
            messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl für die Temperatur ein.")
            return

        # Wenn die Coding Checkbox ausgewählt ist, dann generiere aus dem Message Count ein Tileset
        if coding_checkbox.get():
            message_count_str = message_count_entry.get()
            tileset_weight_str = tileset_weight_entry.get()
            assembly_weight_str = assembly_weight_entry.get()
            if not message_count_str.isdigit():
                messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl für die Anzahl der Nachrichten an.")
                return
            if not tileset_weight_str.isdigit():
                messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl für die Tileset Gewichtung an.")
                return
            if not assembly_weight_str.isdigit():
                messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl für die Assembly Gewichtung an.")
                return
            message_count = int(message_count_str)
            tileset_weight = int(tileset_weight_str)
            assembly_weight = int(assembly_weight_str)
            if checksum.get():
                data = generate_data_with_checksum(message_count, int(temperature), tileset_weight, assembly_weight)
            else:
                data = generate_data(message_count, int(temperature), tileset_weight, assembly_weight)
        # Wenn die Coding Checkbox nicht ausgewählt ist, dann braucht es eine Input Datei
        else:
            input_file = file_entry.get()
            if not input_file:
                messagebox.showerror("Fehler", "Bitte wählen Sie eine Eingabedatei aus oder generieren Sie ein Tileset.")
                return
            # JSON-Datei öffnen und Daten einlesen
            with open(input_file, 'r', encoding='utf-8') as file:
                data = json.load(file)

        # True = Hex, False = Named
        color_code = color_hex.get()
        color_kept = color_keeper.get()

        # True -> Proofreading, False -> Skip Proofreading
        proofreading = proofreading_check.get()

        # Wenn die Priority Checkbox ausgewählt ist
        if priority_var.get():
            priority = priority_level_entry.get()
            if not priority.isdigit():
                messagebox.showerror("Fehler", "Bitte geben Sie eine gültige Zahl für die Prioritätslevel an.")
                return
        else:
            priority = 0

        # Wenn die Flag Checkbox ausgewählt ist
        if flags_var.get():
            flags = [entry.get() for entry in flag_entries]
            if not flag_entries:
                messagebox.showerror("Fehler", "Wenn Flags ausgewählt werden, dann muss mindestens eine Flag angegeben werden.")
                return
        else:
            flags = []

        #if flags_var.get() or priority_var.get() and not coding_checkbox.get():
        #    height = molecule_height.get()
        #else:
        #    height = 0

        # Hilfscode, der nur für Evaluation und schnellere Analyse erstellt wurde
        if coding_checkbox.get():
            results = []
            # Hier einen Eintrag auf 1 setzen, um Iterator festzulegen und auf 0 setzen, um Iterator zu deaktivieren
            iteratives = {
                "mc": 0,
                "tw": 0,
                "aw": 0
            }
            iterator = iteratives["mc"] and message_count or iteratives["tw"] and tileset_weight or iteratives["aw"] and assembly_weight
            for it in range(1, iterator + 1):
                # your loop logic here

                result = {
                    "name": "",
                    "base": 0,
                    "digits": 0,
                    "tileset size": 0,
                    "assembly size": 0,
                    "message count": 0,
                    "tileset weight": 0,
                    "assembly weight": 0
                }
                if checksum.get():
                    eval_data = generate_data_with_checksum(
                        it if iteratives["mc"] else message_count, 
                        int(temperature), 
                        it if iteratives["tw"] else tileset_weight, 
                        it if iteratives["aw"] else assembly_weight)
                    result["base"] = find_best_base(
                        it if iteratives["mc"] else message_count, 
                        it if iteratives["tw"] else tileset_weight, 
                        it if iteratives["aw"] else assembly_weight,
                        True)
                else:
                    eval_data = generate_data(
                        it if iteratives["mc"] else message_count, 
                        int(temperature), 
                        it if iteratives["tw"] else tileset_weight, 
                        it if iteratives["aw"] else assembly_weight)
                    result["base"] = find_best_base(
                        it if iteratives["mc"] else message_count, 
                        it if iteratives["tw"] else tileset_weight, 
                        it if iteratives["aw"] else assembly_weight,
                        False)
                result["digits"] = get_digits(it if iteratives["mc"] else message_count, result["base"])
                result["tileset size"] = main(eval_data, int(temperature), color_code, color_kept, flags, priority, proofreading,True)
                if proofreading: # digits + seed- und endtile je 4 Proofreadingtile
                    result["assembly size"] = (result["digits"] + 2) * 4
                else: # digits + seed- und endtile
                    result["assembly size"] = result["digits"] + 2
                result["message count"] = it if iteratives["mc"] else message_count
                result["tileset weight"] = it if iteratives["tw"] else tileset_weight
                result["assembly weight"] = it if iteratives["aw"] else assembly_weight
                result["name"] = next(("Gen-" + key + "-" + str(it) for key, value in iteratives.items() if value), None)
                results.append(result)

            name = "Gen" + "-" + str(message_count) + "-" + str(tileset_weight) + "-" + str(assembly_weight) + "-" + ("chksm-" if checksum.get() else "") + "results.json"
            if iteratives["mc"] or iteratives["aw"] or iteratives["tw"]:
                with open(name, "w") as file:
                    json.dump(results, file, indent=2)

        # Output Datei ist immer eine json Datei, auch wenn nicht im Namen angegeben
        if not output_file.endswith('.json'):
            output_file += '.json'
        output_data = main(data, int(temperature), color_code, color_kept, flags, priority, proofreading, False)

        # Bestätigungsnachricht
        messagebox.showinfo("Erfolg", "Das Skript wurde erfolgreich ausgeführt.")

        # Die Ausgabe in die vom Benutzer angegebene Ausgabedatei schreiben
        with open(output_file, 'w') as file:
            json.dump(output_data, file, indent=2)
        # Dateibrowser öffnen, wenn Ausgabedatei gespeichert wurde
        output_dir = os.path.dirname(os.path.abspath(output_file))
        webbrowser.open(output_dir)
    except Exception as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {str(e)}")

#
#
#   GUI
#
#
# Erstellung des GUI
root = tk.Tk()

# Setzen Sie den Namen des Fensters
root.title("Tile Generator")

# Setzen Sie die Mindestgröße des Fensters
root.minsize(300, 200)

# Label und Eingabefeld für die Eingabedatei
# Row 0
tk.Label(root, text="Eingabedatei: ").grid(row=0, column=0)
file_entry = tk.Entry(root)
file_entry.grid(row=0, column=1)

# Button zum Öffnen des Dateidialogs
# Row 1
file_button = tk.Button(root, text="Datei auswählen", command=select_file)
file_button.grid(row=1, column=1)

# Trennlinie
# Row 2
canvas1 = tk.Canvas(root, height=2, bg="black")
canvas1.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10,10))

# Kodierung/Tileset Generierung
# Row 3-6
tk.Label(root, text="Generiere Tileset:").grid(row=3, column=0)
coding_checkbox = tk.BooleanVar()
checksum = tk.BooleanVar()
checksum_checkbox = tk.Checkbutton(root, variable=checksum)
tileset_weight_entry = tk.Entry(root)
assembly_weight_entry = tk.Entry(root)
message_count_entry = tk.Entry(root)
tk.Checkbutton(root, variable=coding_checkbox, command=toggle_coding_checkbox).grid(row=3, column=0, sticky="e")
checksum_label = tk.Label(root, text="Checksumme erstellen:")
tileset_weight_label = tk.Label(root, text="Tileset Gewichtung:")
assembly_weight_label = tk.Label(root, text="Assembly Gewichtung:")
message_count_label = tk.Label(root, text="Anzahl Nachrichten:")

# Trennlinie
# Row 7
canvas1 = tk.Canvas(root, height=2, bg="black")
canvas1.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10,10))

# Label und Eingabefeld für die Ausgabedatei
# Row 8
tk.Label(root, text="Ausgabedatei Name: ").grid(row=8, column=0)
output_entry = tk.Entry(root)
output_entry.grid(row=8, column=1)

# Trennlinie
# Row 9
canvas1 = tk.Canvas(root, height=2, bg="black")
canvas1.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(10,10))

# Label und Eingabefeld für die Temperatur
# Row 10
tk.Label(root, text="Temperatur: ").grid(row=10, column=0)
temp_entry = tk.Entry(root)
temp_entry.grid(row=10, column=1)

# Trennlinie
# Row 11
canvas1 = tk.Canvas(root, height=2, bg="black")
canvas1.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(10,10))

# Checkbox, um Proofreading zu aktivieren
# Row 12
tk.Label(root, text="Proofreading: ").grid(row=12, column=0)
proofreading_check = tk.BooleanVar()
tk.Checkbutton(root, variable=proofreading_check).grid(row=12, column=0, sticky="e")

# Trennlinie
# Row 13
canvas1 = tk.Canvas(root, height=2, bg="black")
canvas1.grid(row=13, column=0, columnspan=2, sticky="ew", pady=(10,10))

# Checkboxen für das Color Coding
# Row 14+15
color_hex = tk.BooleanVar()
color_named = tk.BooleanVar()

# Standardmäßig Hex Color Coding ausgewählt
color_hex.set(True)

color_hex.trace_add("write", lambda *args: only_one(color_hex, color_hex.get()))
color_named.trace_add("write", lambda *args: only_one(color_named, color_named.get()))

tk.Label(root, text="HTML Farben:").grid(row=14, column=0)
color_hex_cb = tk.Checkbutton(root, variable=color_hex)
color_hex_cb.grid(row=14, column=0, sticky="e")

tk.Label(root, text="CSS Farben:").grid(row=15, column=0)
color_named_cb = tk.Checkbutton(root, variable=color_named)
color_named_cb.grid(row=15, column=0, sticky="e")

color_keeper = tk.BooleanVar()
tk.Label(root, text="Farbcode erhalten:").grid(row=16, column=0)
tk.Checkbutton(root, variable=color_keeper).grid(row=16, column=0, sticky="e")

# Trennlinie
# Row 17
canvas1 = tk.Canvas(root, height=2, bg="black")
canvas1.grid(row=17, column=0, columnspan=2, sticky="ew", pady=(10,10))

# Molekülhöhe
# Row 17
# molecule_height = tk.IntVar()
# Standardauswahl
# molecule_height.set(1)

# Checkboxen für die Molekülhöhe
# molecule_height_checkbox_1 = tk.Checkbutton(root, text="1", variable=molecule_height, onvalue=1)
# molecule_height_checkbox_2 = tk.Checkbutton(root, text="2", variable=molecule_height, onvalue=2)
# molecule_height_checkbox_3 = tk.Checkbutton(root, text="3", variable=molecule_height, onvalue=3)

# Standartwert und Checkbox
# previous_molecule_height = 1

# Label für die Molekülhöhe
# molecule_height_label = tk.Label(root, text="Höhe des Moleküls:")

# Checkbox für die Prioritätslevel
# Row 18+19
tk.Label(root, text="Priorität:").grid(row=18, column=0)
priority_var = tk.BooleanVar()
priority_checkbox = tk.Checkbutton(root, variable=priority_var, command=toggle_priority_checkbox)
priority_checkbox.grid(row=18, column=0, sticky="e")
priority_level_label = tk.Label(root, text="Anzahl Prioritätslevel:")
priority_level_entry = tk.Entry(root)

# Flag Listen
# Row 20 +++
flag_counter = 0
flag_labels = []
flag_entries = []
flag_remove_buttons = []

# Checkbox für Flags
tk.Label(root, text="Flags:").grid(row=20, column=0)
flags_var = tk.BooleanVar()
flags_checkbox = tk.Checkbutton(root, variable=flags_var, command=toggle_flags_checkbox)
flags_checkbox.grid(row=20, column=0, sticky="e")

# Button zum Hinzufügen von Flags
add_button = tk.Button(root, text="+", command=add_flag)

# Start-Button
# Row 99 um genug Platz für Flags zu garantieren
start_button = tk.Button(root, text="Start", command=start_program)
start_button.grid(row=99, column=0, sticky="e")

root.mainloop()