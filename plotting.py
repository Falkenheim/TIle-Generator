import json
import sys
import os

def load_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_to_txt(tileset_points, assembly_points, filename):
    with open(filename, 'w') as f:
        f.write("Tileset Plot:\n")
        for point in tileset_points:
            f.write(f"({point[0]},{point[1]})\n")

        f.write("\nAssembly Plot:\n")
        for point in assembly_points:
            f.write(f"({point[0]},{point[1]})\n")

def extract_points(data, size_key):
    points = []
    last_point = None
    for entry in data:
        x = entry["assembly weight"] / entry["tileset weight"]
        y = entry[size_key]
        
        if last_point and last_point[1] == y:
            last_point = (x, y)  # Update the x-coordinate fploor the same y value
        else:
            if last_point:
                points.append(last_point)
            last_point = (x, y)
    if last_point:
        points.append(last_point)
    
    return points


def main():
    # Überprüfe, ob der Dateiname als Argument gegeben wurde
    if len(sys.argv) != 2:
        print("Usage: plotting.py <input_filename>")
        sys.exit(1)

    input_filename = sys.argv[1]
    base_name = os.path.splitext(os.path.basename(input_filename))[0]
    output_filename = f"{base_name}-plot.txt"
    
    # Einlesen der Daten
    data = load_data(input_filename)
    
    # Punkte extrahieren
    tileset_points = extract_points(data, "tileset size")
    assembly_points = extract_points(data, "assembly size")

    # Ergebnisse in eine .txt-Datei schreiben
    save_to_txt(tileset_points, assembly_points, output_filename)

if __name__ == "__main__":
    main()