<template>
  <div class="content">
    <Header />
    <div>
      <h1 class="title">{{ sensorData.title }}</h1>
      <div class="date" v-if="sensorData.updated">
        <p>Datenstand: {{ sensorData.updated }}</p>
      </div>
      <div class="gaugegrid">
        <Gauge
          v-for="gauge in sensorData.gauges"
          :key="gauge.label"
          :label="gauge.label"
          :value="gauge.value"
          :unit="gauge.unit"
        />
      </div>
      <div class="description">
        <p>{{ sensorData.description }}</p>
        <ul v-if="sensorData.links">
          <li v-for="(link, index) in sensorData.links" :key="index">
            <a :href="link.url" target="_blank">{{ link.text }}</a>
          </li>
        </ul>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
export default {
  data() {
    return {
      sensorData: {
        title: 'Lädt...',
        gauges: [
          { label: '', unit: '', value: '' },
          { label: '', unit: '', value: '' },
          { label: '', unit: '', value: '' },
          { label: '', unit: '', value: '' },
        ],
        description: '',
        updated: null,
      },
      fetchUrl: [this.$route.params.layout, this.$route.params.sensor].join(
        '/'
      ),
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
          hid: 'og:image:alt',
          property: 'og:image:alt',
          content: this.title,
        },
      ],
    }
  },
  computed: {
    title: () => {
      return `Sensor – Digitale Transparenz im öffentlichen Raum`
    },
    description: () => {
      return 'Aktuell ausgelesene Sensorwerte und weitere Details.'
    },
  },
  async mounted() {
    console.log(this.fetchUrl)
    const fetchedData = await this.$axios.$get(this.fetchUrl)
    fetchedData.updated = new Intl.DateTimeFormat('de', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      timeZone: 'Europe/Zurich',
      timeZoneName: 'short',
      hour12: false,
    }).format(Date.parse(fetchedData.updated))
    this.sensorData = fetchedData
  },
}
</script>

<!-- prettier-ignore -->
<style>
.container {
  @apply justify-center items-center text-center mx-auto w-screen mt-12;
}

.date {
  @apply text-sm text-coolgray;
}

.gaugegrid {
  @apply grid grid-cols-2;
  align-items: center;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 2 2' preserveAspectRatio='none'%3E%3Crect width='2' height='2' fill='%230F05A0' /%3E%3Crect width='1' height='1' fill='%23537BFE'/%3E%3Crect x='1' y='1' width='1' height='1' fill='%23537BFE'/%3E%3C/svg%3E")
    0 0/100% 100vw;
}

.description {
  @apply text-sm text-coolgray;
}

.description ul {
  @apply p-4;
}

.description ul li {
  @apply pb-2;
}

.description ul li a {
  @apply border-zueriblue border block py-1 px-2 rounded;
}
</style>