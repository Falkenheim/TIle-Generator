# Tile-Generator

Dieses Repository enthält ein Python-Skript, welches bestimmte Datenstrukturen (genannt "_tiles") transformiert und modifiziert, basierend auf verschiedenen Input-Parametern.

## Funktionen

- **Color Coding:** Abhängig von der Farbgebung (`color_code`) können Tiles in verschiedenen Farben (z.B. "khaki", "salmon" oder "skyblue") priorisiert und manipuliert werden.
- **Flagging:** Das Skript kann Flags (Kennzeichnungen) hinzufügen oder entfernen, basierend auf den eingegebenen Parametern.
- **Priorität:** Es können Prioritäten gesetzt werden, welche dann in der Reihenfolge ihrer Wichtigkeit verarbeitet werden.
- **Proofreading:** Es gibt eine Option, die ein "Proofreading" (Korrekturlesen) der "_tiles" ermöglicht, um mögliche Fehler zu korrigieren.
- **Farben ändern:** Es gibt eine Option, um die Farben der Tiles zu ändern oder zu behalten (`color_kept`).

## Verwendung

Das Hauptskript (`main`) verarbeitet Daten, Temperatur, Farbcodes und andere Parameter und gibt eine modifizierte Liste von "_tiles" zurück.

Es gibt auch eine `start_program` Funktion, die als primärer Einstiegspunkt für das Programm dient und den Benutzer durch verschiedene Eingabeaufforderungen führt.

## Beispielaufruf

Das Skript kann direkt aus dem Python-Interpreter aufgerufen werden:

```bash
python script_name.py
