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
Besonders wichtig war es uns, dass die Lenkung nicht zu viel Spiel hat. Auf diese Weise sollte garantiert werden, dass das Auto auch ohne große Korrekturen durch das Steuerungssystem geradeaus fahren kann. Dadurch müsste das Programm weniger Korrekturen ausführen. 
Der Antrieb des Fahrzeugs hat ein Differenzial, das die Fahreigenschaften verbessern soll. 
Es wird sichergestellt, dass das Fahrzeug weder untersteuert noch übersteuert. 
Um das Differenzial anzutreiben ist ein kleines Getriebe nötig.

Die Wahl der Motoren ist auf die Motoren des Spike Prime von Lego gefallen. 
Diese Motoren haben den Vorteil, dass sie gut mit dem Gerüst des Fahrzeugs verbunden werden können und keine weiteren Komponenten wie Getriebe benötigt werden. 

Als Kontrollplatine haben wir uns für einen Rasbery Pi 4B entschieden, da er genügend Rechenleistung und Kompatibilität mit anderen benötigten Komponenten liefert.
Die Motoren können jedoch nicht direkt an den Pi angeschlossen werden. Zum Betreiben der Motoren wird ein Buildhat verwendet. Dieser wird an die GPIO Pins angeschlossen. 
Das Spike Prime System liefert auch Ultraschallsensoren. Diese sind kompatibel mit dem Buildhat.
Wir haben die Ultraschallsensoren im Lauf der Entwicklung zum Fahrzeug hinzugefügt, um das Manövrieren zu vereinfachen, da die Kammera nicht immer zuverlassliche Daten liefert und diese sehr schwer zu verarbeiten sind. 

Wir verwenden eine Kammera um die Hindernisse auf der Bahn zu erkennen. Bei der Kamera handelt es sich um eine OpenMV Cam H7.
Zuerst wollten wir die Kammera auch verwenden um die Wände zu erkennen. Da dies nicht alzu gut funktioniert hat, haben wir uns dazu entschieden die Erkennung der Wände und das Manövrieren über andere Sensoren zu realisieren. 
Dafür haben wir die Ultraschallsensoren zum Fahrzeug hinzugefügt. 


Entsprechend den Entwicklungen des Fahrzeugs hat sich auch das Programm gewandelt. Bevor jedoch die Implementierung eines Algorithmus zum Steuern des Fahrzeugs begonnen werden kann müssen einige Grundlagen bereitgestellt werden.
Diese Grundlagen beinhalten das Programm zum Interpretieren der Kammeradaten, die Kommunikation zwischen allen Komponenten und das Kontrollieren dieser. 
Die Kommunikation zu Sensoren und Motoren wird durch den Buildhat und seine Software die Kommunikation zwischen den Komponenten und das Steuern des Fahrzeugs. 
Die Kommunikation zu Motoren und Sensoren (nicht Kamera) wird vom Buildhat und seiner Sofware gesteuert. 
Die Kamera ist mit einem USD-Kabel mit dem Rasbery Pi verbunden. Die Daten werden über einen Serialport in Form von JSON-Objekten versendet. Diese Packets beinhalten die interpretierten Daten der Kamera. Die Kamera kann durch interne Bibliotheken Farberkennung durchführen. Die Farberkennug gibt Blobs zurück, die eigenschaften wie ID (mit zu erkennenden Farben definiert), Position und Größe. Die Blobs werden auf dem Rasbery Pi in Objekte einer für sie angelegten Klasse verwandelt. Mit dieser Klasse kann im Algorithmus weitergearbeitet werden. Die Sensoren sind durch den Buildhat als vordefinierte Klassen verfügbar. Sie können einfach in das Programm integriert werden und ihre Daten stehen bereits in nutzbarer Form zur Verfügung. 
Die Motoren werden wie die Sensoren auch über den Buildhat gesteuert. Der Buildhat ermöglicht leichte und schnelle Interaktion mit den Sensoren und Motoren. 

Da es nicht gut möglich ist mit der Kammera zu arbeiten und diese nur sehr unzuverlässlich funktioniert orientiert sich der Algorithmus hauptsächlich mit Hilfe der Ultraschallsensoren. Dies führt zwar zu einer mehr oder weniger blinden Fahrt, die auch weniger effizient ist als es mit anderen Methoden möglich wäre, aber sie funktioniert größtenteils zuverlässig. 

Die Funktionsweise des algorithmuAlgorithmus orientiert sich stark an den technischen Begebenheiten des Fahrzeugs.
Das Programm ist in drei Teile eingeteilt. 
Der erste Teil ist das Abbiegen an den Ecken. Wenn das Fahrzeug auf eine bestimmte Distanz, die mit dem ersten Ultraschallsensor erkannt wird, an die Wand herangefahren ist, prüft es mit dem zur Seite gerichteten Ultraschallsensor in welche Richtung es drehen muss. Danach wird eine entsprechende Sequenz an Bewegungen ausgeführt, die das Fahrzeug um c.a. 90 Grad dreht. 
Der zweite Teil des Algorithmus muss sich auf die Kammera verlassen. Es sollen die Hindernisse auf der Strecke entdeckt werden. abhängig von der Farbe des Hindernisses wird die Bahn des Fahrzeuges korrigiert. Diese Korrektur geschieht an dieser Stelle jedoch nur mit dem Einstellen einer Variablen, die im dritten Teil zum Steuern des Fahrzeuges verwendet wird.
Der dritte Teil steuert die Lenkung des Fahrzeugs. Er vergleicht die gewollte Spur mit der, die das Fahrzeug tatsächlich fährt und korrigiert dem entsprechend die Bahn, indem es die Lenkung einstellt. 
