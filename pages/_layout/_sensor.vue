<template>
  <div class="container">
    <Header />
    <div>
      <h1 class="title">{{ currentLayout.title }} {{ currentSensor.title }}</h1>
      <div class="gaugegrid">
        <Gauge
          v-for="gauge in gauges_sample"
          :key="gauge.label"
          :label="gauge.label"
          :value="gauge.value"
          :unit="gauge.unit"
        />
      </div>
      <div class="description">
        <p>{{ currentLayout.description }}</p>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import * as d3 from 'd3'

export default {
  data() {
    return {
      ckanURL: 'https://data.stadt-zuerich.ch/api/3/action/datastore_search',
      gauges_sample: [
        {
          label: 'Seit Mitternacht',
          value: "20'342",
          unit: 'Personen',
        },
        {
          label: 'NOx',
          value: 12.1,
          unit: 'm/s',
        },
        {
          label: 'NO',
          value: 23.2,
          unit: 'm/s',
        },
        {
          label: 'Heute',
          value: 'n.v.',
          unit: '',
        },
      ],
      sensors: [
        {
          id: '2997',
          title: 'Lux-Guyer-Weg',
        },
        {
          id: '3013',
          title: 'Lettenviadukt',
        },
        {
          id: 'Zch_Stampfenbachstrasse',
          title: 'Stampfenbachstrasse',
        },
      ],
      layouts: [
        {
          name: 'air',
          title: 'Luftverschmutzungssensor',
          description: 'Beschreibungstext Luftsensor.',
          load_params: {
            resource_id: '4466ec4a-b215-4134-8973-2f360e53c33d',
            sort: 'Datum desc',
            limit: 32000,
            filters: {
              Standort: this.$route.params.sensor,
            },
          },
          gauges: [
            {
              label: 'Ozon',
              defaultValue: 0,
              unit: 'µg/m3',
              type: 'lookup',
            },
          ],
        },
        {
          name: 'velo',
          title: 'Velozählstelle',
          description: 'Beschreibungstext Velo.',
          load_params: {
            resource_id: 'ebe5e78c-a99f-4607-bedc-051f33d75318',
            sort: 'DATUM desc',
            limit: 32000,
            filters: {
              FK_STANDORT: this.$route.params.sensor,
            },
          },
        },
        {
          name: 'fuss',
          title: 'Fussgängerzählstelle',
          description: 'Beschreibungstext Fussgänger.',
          load_params: {
            resource_id: 'ebe5e78c-a99f-4607-bedc-051f33d75318',
            sort: 'DATUM desc',
            limit: 32000,
            filters: {
              FK_STANDORT: this.$route.params.sensor,
            },
          },
        },
      ],
    }
  },
  computed: {
    currentLayout() {
      const requestedLayout = this.$route.params.layout
      if (this.layouts.map((i) => i.name).includes(requestedLayout)) {
        return this.layouts[
          this.layouts.map((i) => i.name).indexOf(requestedLayout)
        ]
      }
      return this.layouts[0]
    },
    currentSensor() {
      const requestedSensor = this.$route.params.sensor
      if (this.sensors.map((i) => i.id).includes(requestedSensor)) {
        return this.sensors[
          this.sensors.map((i) => i.id).indexOf(requestedSensor)
        ]
      }
      return this.sensors[0]
    },
  },
  async mounted() {
    const url = [
      this.ckanURL,
      this.dictToURI(this.currentLayout.load_params),
    ].join('?')

    console.log(url)

    let data = []

    if (this.currentLayout.name === 'air') {
      data = await d3.json(url).then(function (r) {
        r.result.records.forEach((d) => {
          d.date = d.Datum
          d.value = +d.Wert
          d.unit = d.Einheit
        })
        return r.result.records
      })
    } else if (this.currentLayout.name === 'velo') {
      data = await d3.json(url).then(function (r) {
        r.result.records.forEach((d) => {
          d.date = d.DATUM
          d.value = +d.VELO_IN + +d.VELO_OUT
          d.unit = 'Velo'
        })
        return r.result.records
      })
    } else if (this.currentLayout.name === 'fuss') {
      data = await d3.json(url).then(function (r) {
        r.result.records.forEach((d) => {
          d.date = d.DATUM
          d.value = +d.FUSS_IN + +d.FUSS_OUT
          d.unit = 'Personen'
        })
        return r.result.records
      })
    }

    console.log(data)
    return data
  },
  methods: {
    dictToURI(dict) {
      const str = []
      for (const p in dict) {
        if (dict[p] instanceof Object) {
          dict[p] = JSON.stringify(dict[p])
        }
        str.push(encodeURIComponent(p) + '=' + encodeURIComponent(dict[p]))
      }
      return str.join('&')
    },
  },
}
</script>

<style>
.container {
  @apply justify-center items-center text-center mx-auto w-screen mt-12;
}

.title {
  @apply block font-normal tracking-normal text-xl font-bold p-5;
}

.gaugegrid {
  @apply grid grid-cols-2;
  align-items: center;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 2 2' preserveAspectRatio='none'%3E%3Crect width='2' height='2' fill='%23090036' /%3E%3Crect width='1' height='1' fill='%230F05A0'/%3E%3Crect x='1' y='1' width='1' height='1' fill='%230F05A0'/%3E%3C/svg%3E")
    0 0/100% 100vw;
}

.description {
  @apply p-5 text-sm text-coolgray;
}
</style>
