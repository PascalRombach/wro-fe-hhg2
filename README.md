Future Engineers - Beispielrepository 
====

Dieses GitHub-Repository dient als Vorlage für Teams in Future Engineers.

## Content

* Der Ordner `Programmcode` enthält den kompletten Programmcode, der für das Roboterauto verwendet wird.
* Im Ordner `Roboterauto` sollen sechs Fotos abgelegt werden, die das Roboterauto aus allen Richtungen zeigen.
* Im Ordner `Technische Zeichnungen` werden Zeichnungen von Komponenten des Roboterautos oder dem gesamten Roboterauto abgelegt.
* Der Ordner `Video` beinhaltet die Datei "video.md", die mit einem Link zu einem Youtube-Video befüllt werden muss. Das Video zeigt das Roboterauto beim Absolvieren des Spielfeldes.

## Einleitung

Zuerst haben wir begonnen Prototypen des Fahrzeugkörpers zu bauen. Diese sollten zunächst nur rollen und lenken können. 
Besonders wichtig war es uns, dass die Lenkung nicht zu viel Spiel hat. Auf diese weise sollte garantiert werden, dass das Auto auch ohne große Korrekturen durch das Steuerungssystem geradeaus fahren kann. Auf diese Weise müsste das Programm weniger Korrekturen ausführen. 
Der Antrieb des Fahrzeugs hat ein Differenzial, das die Fahreigenschaften verbessern soll. 
Es wird sichergestellt, dass das Fahrzeug weder untersteuert noch übersteuert. 
Um das Differenzial anzutreiben ist ein kleines Getriebe nötig.

Die Wahl der Motoren ist auf die Motoren des Spike Prime von Lego gefallen. 
Diese Motoren haben den Vorteil, dass sie gut mit dem Gerüst des Fahrzeugs verbunden werden können und keine weiteren Komponenten wie Getriebe benötigt werden. 

Als Kontrollplatine haben wir uns für einen Rasbery Py4 entschieden, da er genügent Rechenleistung und Kompatibilität mit anderen benötigten Komponenten liefert.
Die motoren können jedoch nicht direkt an den Py angeschlossen werden. Zum betreiben der Motoren wird ein Buldhat verwendet. Dieser wird an die GpIo Pins angeschlossen. 
Das Spike Prime System liefert auch ultraschall Sensoren. Diese sind kompatibel mit dem Buildhat.
Wir haben die Ultraschallsensoren im lauf der Entwicklung zum Fahrzeug hinzugefügt, um das manövrieren zu vereinfachen, da die Kammera nicht immer zuverlassliche Daten liefert und diese sehr schwer zu verarbeiten sind. 

Wir verwenden eine Kammera um die Jindernisse auf der Bahn zu erkennen. Bei der kammera handelt es sich um eine ... .
Zuerst wollten wir die Kammera auch verwenden um die Wände zu erkennen. Da dies nicht alzu gut funktioniert hat, haben wir uns dazu entschieden die Erkennung der Wände und das Manövrieren  über andere Sensoren zu realisieren. 
Dafür haben wie die Ultraschallsensoren zum Fahrzeug hinzugefügt. 


