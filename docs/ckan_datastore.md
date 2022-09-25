# Digitale Transparenz im öffentlichen Raum - technischer Bericht Daten

|               |                                 |
| ------------- | ------------------------------- |
| Verfasser:in  | Thorben Westerhuys, cividi GmbH |
| Revision      | 1                               |
| Ort und Datum | Zürich, 24.09.2022              |

## Management Summary

Mit der bestehenden Datastore API des [OGD Portals der Stadt Zürich](https://data.stadt-zuerich.ch) besteht ein grosses Potential für Microsites, spezifische Anwendungen, Dashboards etc. mittels einheitlicher und normalisierender Schnittstelle auf eine grosse Bandbreite an öffentlich verfügbaren Daten zuzugreifen und diese zu verarbeiten. Zusätzlich bedeutet der Zugriff via Datastore, dass je nach Anwendung nicht vollständige Datensätze, sondern Subsets heruntergeladen werden können und durch die automatische Normalisierung Datensatzübergreifende Anwendungen erheblich vereinfacht. Dadurch konnte der Prototyp für digitale Transparenz im öffentlichen Raum auf die dargestellten Werte und das notwnedige Layout fokussieren, anstelle aufwändiger Datenintegration der verschiedenen Sensortypen.

## Ausgangslage

Mit der zunehmenden Anzahl an Messungen mittels Sensoren, Kameras und anderer Möglichkeiten, besteht gleichzeitig der Bedarf an einer einheitlichen Sichtbarmachung, sowie Zugänglichkeit der erhobenen Daten. Der vorliegende Prototyp kombiniert dabei offen publizierte Sesnordaten mit einem einfach verständlichen Webinterface, das mittels Vor-Ort QR-Code direkt aufgerufen werden kann.

Dazu muss die Anwendung zweierlei gewährleisten:

1. Abruf der Daten in geeigneter Form
1. Verständliche Darstellung der Daten für mobile Endgeräte

## 1. Datenabruf

Das [Open Data Portal](https://data.stadt-zuerich.ch) der Stadt Zürich basiert auf dem Open Source Projekt [CKAN](https://ckan.org) in Version [`2.7.6`](https://github.com/ckan/ckan/blob/2.7/CHANGELOG.rst#v276-2019-07-03). Für eine Vorschau der tabellarischen Daten wird zudem die [Datastore Erweiterung](https://docs.ckan.org/en/2.7/maintaining/datastore.html) genutzt und ist als Data Explorer interaktiv im Portal einsehbar.

Für den Abruf der Daten galt es auf möglichst bestehender Infrastruktur aufzusetzen und keine neuen Abhängigkeiten zu schaffen. Da die Datastore Erweiterung bereits eine [umfassende API](https://docs.ckan.org/en/2.7/maintaining/datastore.html?highlight=datastore#the-datastore-api) zur Abfrage der Datensätze bereitstellt, fiel die Wahl auf eine direkte Integration der API anstelle eines "Daten-Proxies".

![Datensatz mit aktivem Datastore](images/ckan_meta_datastore_active.png 'Datensatz mit aktivem Datastore')

Spezifisch bietet die Datastore API folgende Endpunkte, die eine schnelle und effiziente Abfrage für die Sensor Datensätze ermöglichte. Die Erweiterung im Zusammenspiel mit dem [CKAN DataPusher](https://github.com/ckan/datapusher) führt dabei zu folgenden Eigenschaften für Datensätze, die im Datastore vorhanden sind (siehe obiger Screenshot):

1. Die einfache Abfrage mittels REST-API des vollständigen oder gefilterten Datensatzes anhand Such-, Filter- und Sortieroptionen über eine standartisierte Schnittstelle
1. Automatische Normalisierung semi-strukturierte Datensätze, sodass diese einer einheitlichen Philosophie folgen - siehe dazu "Normalisierung der Daten"
1. Einfache Aggregate

### 1.1 Einfache Abfrage via [`ckanext.datastore.logic.action.datastore_search`](https://docs.ckan.org/en/2.7/maintaining/datastore.html?highlight=datastore#ckanext.datastore.logic.action.datastore_search)

Haupt Schnittstelle zur Abfrage einzelner Zeilen und Spalten innerhalb eines Datensatzes via REST-API.

- `resource_id`: Die benötigte Resource
- `filters` / `q`: Filtert alle Zeilen nach exakten oder vorhanden sein bestimmter Strings, ermöglicht das direkte filtern nach Sensor IDs
- `sort`: Sortieren, ermöglicht z.B. das korrekte sortieren nach Datum
- `fields`: Limitiert die ausgegebenen Felder, ermöglicht einen effizienteren Datentrasnfer bei Tabellen mit vielen Spalten
- `limit`: Limiert die Anzahl zurückgegebener Zeilen, ermöglicht eine schnellere Verarbeitung und zusammen mit `sort` einfache Selektierung der relevanten Zeilen
- `records_format`: Transformiert die Antwort ggf. in andere Formate (z.B. JSON Objects, JSON lists, CSV oder TSV), sodass dies nicht clientseitig geschehen muss

Durch diese Schnittstelle konnten wir mittels der [bestehenden CKAN Integration](https://v4.framework.frictionlessdata.io/docs/tutorials/formats/ckan-tutorial) im Python basierten [`frictionless Framework`](https://v4.framework.frictionlessdata.io) direkt die relevanten Rohdaten innerhalb der Sensor Datensätze abfragen.

Beispielabfrage für die Luftqualitäts-Sensoren:

```python
from frictionless import Resource
from frictionless.plugins.ckan import CkanDialect

# Lädt die neuesten 5 Ozon Einträge in 2022 für den Standort Stampfenbachstrasse
resource = Resource(
  'https://data.stadt-zuerich.ch',
  format='ckan',
  dialect=CkanDialect(
    resource = 'ugz_ogd_air_h1_2022.csv',
    dataset = 'ugz_luftschadstoffmessung_stundenwerte',
    limit = 5,
    sort = 'Datum desc',
    filter = {
      'Standort': 'Zch_Stampfenbachstrasse',
      'Parameter': 'O3'
    }
  )
)
```

Als Teil der Luftqualitäts Pipeline: [air.pipeline.yaml](https://github.com/cividi/TransparenZRH/blob/33ef4edc08a9eba12e910356ae00ef35bd353205/api/descriptors/air.pipeline.yaml#L32)

Da die Datastore API derzeit nur zur Erzeugung der oben erwähnten Vorschau Tabellen gedacht ist, ergaben sich für den Protyp folgende Probleme:

- grosszügiges Caching der Abfragen notwendig (derzeit 15 min)
- manche Datensätze liefern unzuverlässige Antworten in der zweiten Jahreshälfte

Aus diesen Gründen verwendet die aktuelle Version des Prototypen einen eigenen Datenproxy zur Aufbereitung und Zwischenspeicherung der Rohdaten.

### 1.2 Normalisierung der Daten

Für eine einfache Integration verschiedener Sensortypen ist eine einheitliche Struktur der Daten unabdingbar. Das bedeutet jedoch nicht, dass jeder Datensatz der exakt gleichen Struktur folgen muss. Bereits eine Übersetzung bzw. Bereitstellung als "[Tidy Data](https://github.com/openZH/mdd-ogd-handbook/blob/main/publikationsleitlinien/warum_tidy_data.md)", wie durch die OGD Stelle des Kanton Zürich empfohlen, kann dazu führen, dass der Aufwand für neue Sensoren minimal ist. Der CKAN Datapusher erzeugt automatisch "Tidy Data" mittels der [`messydata`](https://messytables.readthedocs.io/en/latest/) Bibliothek. Dadurch sind viele Datensätze auf dem OGD Portal bereits in einer normalisierten Form vorhanden und zudem via API einfach und gezielt abrufbar. Jedoch nur, wenn die Daten zuverlässig in den Datastore geladen werden.

Ein gutes Beispiel sind die [Luftdaten](https://data.stadt-zuerich.ch/dataset/ugz_luftschadstoffmessung_stundenwerte).

Die stündlichen Rohdaten, publiziert auf [ogd.zueriluft.ch](http://ogd.zueriluft.ch/api/v1/h1.csv), haben

- einen mehrzeiligen Kopf
- enthalten nur eine Zeile je Stunde mit allen Messwerten und Standorten als Spalten

![Luftrohdaten auf zueriluft.ch](images/zueriluft_raw_data.png 'Luftrohdaten auf zueriluft.ch')

Der [analoge Datensatz](https://data.stadt-zuerich.ch/dataset/ugz_luftschadstoffmessung_stundenwerte/resource/65be6eee-b788-4a36-aa41-16da5d9cc02d) im Datastore des OGD Portals jedoch folgen der Tidy Data Philosophie. Dadurch

- ist der Kopf einzelig und kompatibel mit gängigen CSV Importern und über lange Zeit unveränderlich, z.B. ein neuer Sensor oder Messung ergibt keine Änderung des Datenformats
- entspricht jede Einzelmessung (z.B. Stickstiff an der Stampfenbachstrasse um 11.00 Uhr) einer Zeile und kann somit indiviuell abgefragt und aggregiert werden

![Normalisierte Luftdaten im OGD Portal](images/ckan_datastore_preview_normalized.png 'Normalisierte Luftdaten im OGD Portal')

Derzeit bekommt jedes Jahr eine eigene Resource, anstelle eines fortlaufenden oder rollenden Fortschreibung eines Datensatzes - z.B. die letzten 365 Tage. Das würde auch rollende Aggregate (z.B. letzte 7 Tage, letzte 7 Montage etc.) stark vereinfachen.

### 1.3 Einfache Aggregate

Derzeit gibt es keine einfache Möglichkeit Aggregate (z.B. Summen, Durchschnitte, Median der letzten 7 Tage, Montage etc.) direkt abzufragen. Daher werden diese als Teil der dTöR Applikation mittels eines Datenproxies generiert ([Beispiel Pipeline Jahresdurchschnitt Velodaten](https://github.com/cividi/TransparenZRH/blob/33ef4edc08a9eba12e910356ae00ef35bd353205/api/descriptors/bike.pipeline.yaml#L15)).

Der Datastore ermöglicht einfache SQL Abfragen. In unseren Tests konnten wir jedoch keine der PostgreSQL Aggregierungs-Funktionen erfolgreich benutzen.
