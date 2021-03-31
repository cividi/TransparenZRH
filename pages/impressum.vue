<template>
  <div class="content">
    <Header />
    <div class="text">
      <h1 class="title">Impressum</h1>
      <p>
        Daten spielen eine wichtige Rolle in der «Smart City Zürich». Dank ihnen
        kann beispielsweise die städtische Infrastruktur gezielt und effizient
        geplant und unterhalten werden. Mittels Sensoren, welche
        Fahrradfrequenzen, Luftqualität und anderes messen, werden Daten im
        öffentlichen Raum erhoben.
      </p>
      <p>
        Mit zunehmender Datensammlung steigt die Bedeutung von Transparenz und
        Rechenschaftspflicht gegenüber der Öffentlichkeit. Die Stadt Zürich ist
        diesbezüglich bereits heute aktiv, indem sie viele Daten als «Open Data»
        veröffentlicht. In diesem Pilotprojekt von Smart City Zürich soll
        getestet werden, wie zusätzliche Transparenz geschaffen werden kann.
      </p>
      <p>
        Eine einfache Bildsprache informiert hierbei transparent über die
        Sammlung von Daten im öffentlichen Raum und deren Verwendung. Sensoren
        werden mit Piktogrammen und QR-Codes beschriftet. Letztere leiten auf
        Websites weiter, welche die gesammelten Daten visualisieren und weitere
        Informationen bieten. Dazu werden ausschliesslich Daten von bereits
        vorhandenen Sensoren und offenen, frei zugänglichen Behördendaten («Open
        Data») verwendet. Bei Fragen steht Ihnen das Smart City Team der Stadt
        Zürich gerne zur Verfügung. Maximilian.stern@zuerich.ch
      </p>
    </div>
    <Footer />
  </div>
</template>

<script>
export default {}
</script>

<style>
.content {
  display: flex;
  flex-direction: column;
}
.text {
}

.title {
  @apply font-bold tracking-normal text-xl text-zueriblue p-4;
}

p {
  @apply p-4;
}
</style>
