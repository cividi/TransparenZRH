<template>
  <div class="content">
    <Header :simple="true" />
    <div class="text">
      <h1 class="font-bold tracking-normal text-xl text-zueriblue px-4 pt-4">
        Digitale Transparenz im öffentlichen Raum
      </h1>
      <p>
        Daten spielen eine wichtige Rolle in der «Smart City Zürich». Dank ihnen
        kann beispielsweise die städtische Infrastruktur gezielt und effizient
        geplant und unterhalten werden. Mittels Sensoren, welche
        <NuxtLink to="/view/bike/VZS_LUXG">Fahrrad-</NuxtLink>,
        <NuxtLink to="/view/pedestrian/FZS_LETL">Personenfrequenzen</NuxtLink>,
        <NuxtLink to="/view/air/Zch_Schimmelstrasse">Luftqualität</NuxtLink>
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
export default {
  data() {
    return {
      title: 'Digitale Transparenz im öffentlichen Raum',
      description:
        'Mit zunehmender Datensammlung steigt die Bedeutung von Transparenz und Rechenschaftspflicht gegenüber der Öffentlichkeit. Die Stadt Zürich ist diesbezüglich bereits heute aktiv, indem sie viele Daten als «Open Data» veröffentlicht. In diesem Pilotprojekt von Smart City Zürich soll getestet werden, wie zusätzliche Transparenz geschaffen werden kann.',
      image: '/favicon/icon.png',
    }
  },
  head() {
    return {
      title: this.title,
      meta: [
        {
          hid: 'description',
          name: 'description',
          content: this.description,
        },
        {
          hid: 'twitter:title',
          name: 'twitter:title',
          content: this.title,
        },
        {
          hid: 'twitter:description',
          name: 'twitter:description',
          content: this.description,
        },
        {
          hid: 'twitter:image',
          name: 'twitter:image',
          content: this.image,
        },
        {
          hid: 'twitter:image:alt',
          name: 'twitter:image:alt',
          content: this.title,
        },
        {
          hid: 'og:title',
          property: 'og:title',
          content: this.title,
        },
        {
          hid: 'og:description',
          property: 'og:description',
          content: this.description,
        },
        {
          hid: 'og:image',
          property: 'og:image',
          content: this.image,
        },
        {
          hid: 'og:image:secure_url',
          property: 'og:image:secure_url',
          content: this.image,
        },
        {
          hid: 'og:image:alt',
          property: 'og:image:alt',
          content: this.title,
        },
      ],
    }
  },
}
</script>

<style lang="postcss">
.content {
  display: flex;
  flex-direction: column;
}

p {
  @apply px-4 py-2;
}
</style>
