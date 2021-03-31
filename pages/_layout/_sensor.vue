<template>
  <div class="container">
    <Header />
    <div>
      <h1 class="title">
        {{ currentLayout.title }}
      </h1>
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
  @apply block font-normal tracking-normal text-xl;
}
</style>
