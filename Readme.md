# Tile-Generator

Dieses Repository enthält ein zwei Python-Skripts. Das Skript **tile_generator.pyw** ist dabei das Hauptskript, welches bestimmte Datenstrukturen (Tiles) transformiert und modifiziert, basierend auf verschiedenen Input-Parametern.
Das Skript **plotting.py** ist ein kleines Skript, welches Tilesetgröße und Assemblygröße für die Evaluation des Verhältnis dieser beiden Parameter in eine .txt-Datei schreibt.

## Funktionen des Hauptskripts

- **Generation:** Das Skript kann Tilesets generieren. Wichtige Eingabeparameter dafür sind Anzahl der Nachrichten und die Gewichtung von Tileset und Assembly
- **Checksummen:** Das Skript kann auch generierte Tilesets als Tilesets mit Checksumme erstellen.
- **Flags:** Das Skript kann Flags in Tilesets hinzufügen, basierend auf den eingegebenen Parametern.
- **Priorität:** Das Skript kann Prioritätslevel in Tilesets hinzufügen.
- **Proofreading:** Das Skript kann Proofreading auf dem Tileset anwenden.

## Verwendung

Das Hauptskript (`main`) verarbeitet Tilesets und bestimmte Eingaben in der GUI und gibt eine modifizierte Liste von "_tiles" in einer JSON-Datei zurück, welche in der Simulationsumgebung netTAS als Tilesets geladen werden können.

Das Tool **netTAS** findet sich unter folgendem Link: https://nettas.itm.uni-luebeck.de/tileSet


