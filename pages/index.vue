<template>
  <div class="content">
    <Header :simple="true" />
    <div class="text">
      <h1 class="title">Digitale Transparenz im öffentlichen Raum</h1>
      <p>
        Daten spielen eine wichtige Rolle in der «Smart City Zürich». Dank ihnen
        kann beispielsweise die städtische Infrastruktur gezielt und effizient
        geplant und unterhalten werden. Mittels Sensoren, welche
        <NuxtLink to="/view/air/Zch_Stampfenbachstrasse"
          >Fahrradfrequenzen</NuxtLink
        >,
        <NuxtLink to="/view/velo/2997">Luftqualität</NuxtLink>
        und anderes messen, werden Daten im öffentlichen Raum erhoben.
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
        vorhandenen Sensoren und offenen, frei zugänglichen Behördendaten (<a
          href="https://www.stadt-zuerich.ch/opendata.secure.html"
          target="_blank"
          >«Open Data»</a
        >) verwendet.
      </p>
      <p>
        Fragen steht Ihnen das
        <a
          href="https://www.stadt-zuerich.ch/prd/de/index/stadtentwicklung/smart-city.html"
          target="_blank"
          >Smart City Team</a
        >
        der Stadt Zürich gerne zur Verfügung.
      </p>
      <p>maximilian [punkt] stern [at] zuerich [punkt] ch</p>
    </div>
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

.title {
  @apply font-bold tracking-normal text-xl text-zueriblue p-4;
}

p {
  @apply p-4;
}
</style>
