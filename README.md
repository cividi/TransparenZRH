# Digitale Transparenz im öffentlichen Raum

Daten spielen eine wichtige Rolle in der «Smart City Zürich». Dank ihnen kann beispielsweise die städtische Infrastruktur gezielt und effizient geplant und unterhalten werden. Mittels Sensoren, welche Fahrradfrequenzen, Luftqualität und anderes messen, werden Daten im öffentlichen Raum erhoben.

Mit zunehmender Datensammlung steigt die Bedeutung von Transparenz und Rechenschaftspflicht gegenüber der Öffentlichkeit. Die Stadt Zürich ist diesbezüglich bereits heute aktiv, indem sie viele Daten als «Open Data» veröffentlicht. In diesem Pilotprojekt von Smart City Zürich soll getestet werden, wie zusätzliche Transparenz geschaffen werden kann.

Eine einfache Bildsprache informiert hierbei transparent über die Sammlung von Daten im öffentlichen Raum und deren Verwendung. Sensoren werden mit Piktogrammen und QR-Codes beschriftet. Letztere leiten auf Websites weiter, welche die gesammelten Daten visualisieren und weitere Informationen bieten. Dazu werden ausschliesslich Daten von bereits vorhandenen Sensoren und offenen, frei zugänglichen Behördendaten («[Open Data](https://www.stadt-zuerich.ch/opendata.secure.html)») verwendet.

- [Projektseite](https://transparenzrh.vercel.app)
  - Beispielsensor [Luftqualität Schimmelstrasse](https://transparenzrh.vercel.app/view/air/Zch_Schimmelstrasse) (`/view/air/Zch_Schimmelstrasse`)
  - API-Proxy [Luftqualität Schimmelstrasse](https://transparenzrh.vercel.app/api/v1/air/Zch_Schimmelstrasse) (`/api/v1/air/Zch_Schimmelstrasse`)
- [Python Notebook](https://github.com/Brieden/mixed/blob/main/stick-it-open.ipynb)
- [D3 Notebook](https://observablehq.com/@n0rdlicht/transparenzrh)

## Developer

### Stack

- Frontends
  - Nuxt.js
  - TailwindCSS
- Backend (`/api`)
  - Flask

For testing and deployment add the following environment variables:

- `API_URL`

### Run and Deploy

```bash
# clone repository
$ git clone git@github.com:cividi/TransparenZRH.git

# install dependencies
$ npm install

# serve frontend and backend with hot reload at localhost:3000
$ export API_URL=http://localhost:3000/api/v1/
$ vercel dev # frontent only: npm run dev

# build for production and launch server
$ npm run build
$ npm run start

# generate static project
$ npm run generate
```

For detailed explanation on how things work, check out [Nuxt.js docs](https://nuxtjs.org).
