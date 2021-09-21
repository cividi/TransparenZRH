<template>
  <div class="content">
    <div>
      <div v-if="sensorData.updated" class="text-sm text-coolgray">
        <p class="px-4 py-2">Datenstand: {{ sensorData.updated }}</p>
      </div>
      <div class="gaugegrid">
        <div v-for="gauge in sensorData.gauges" :key="gauge.label">
          <LoadingGauge v-if="gauge.type == 'loading'" />
          <NumberGauge
            v-if="gauge.type == 'number'"
            :label="gauge.label"
            :value="gauge.value"
            :unit="gauge.unit"
          />
          <SvgGauge
            v-if="gauge.type == 'svg'"
            :label="gauge.label"
            :svg="gauge.src"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sensorData: {
        title: 'Lädt...',
        gauges: [
          { label: '', unit: '', value: '', type: 'loading' },
          { label: '', unit: '', value: '', type: 'loading' },
          { label: '', unit: '', value: '', type: 'loading' },
          { label: '', unit: '', value: '', type: 'loading' },
        ],
        description: ' ',
        updated: ' ',
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
    try {
      const fetchedData = await this.$axios.$get(this.fetchUrl)

      this.sensorData.updated = new Intl.DateTimeFormat('de', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        timeZone: 'Europe/Zurich',
        timeZoneName: 'short',
        hour12: false,
      }).format(Date.parse(fetchedData.created))
      this.sensorData.title = fetchedData.views[0].title

      const gauges = fetchedData.views
      this.sensorData.gauges = gauges.map(function (obj) {
        const resourceIndex = obj.resources.map(function (viewResourceName) {
          return [...Array(fetchedData.resources.length).keys()].filter(
            function (el) {
              return fetchedData.resources[el].name === viewResourceName
            }
          )
        })[0]

        let data = null

        if ('filter' in obj.spec) {
          const filter = obj.spec.filter
          data = fetchedData.resources[resourceIndex].data.filter(function (
            el
          ) {
            if ('equals' in filter) {
              return el[filter.field] === filter.equals
            } else {
              /* eslint-disable no-console */
              console.error(
                'Filters other than equals are not supported at the moment.'
              )
              /* eslint-enable no-console */
              return false
            }
          })[0]
        } else {
          data = fetchedData.resources[resourceIndex].data[0]
        }

        const encoding = obj.spec.encoding

        if (obj.specType === 'gauge') {
          const nObj = {}
          nObj.type = obj.spec.mark
          Object.keys(encoding).forEach(function (enc) {
            if (typeof encoding[enc] === 'string') {
              nObj[enc] = encoding[enc]
            } else if (typeof encoding[enc] === 'object') {
              if ('field' in encoding[enc]) {
                nObj[enc] = data[encoding[enc].field]
              }
              if (
                'type' in encoding[enc] &&
                encoding[enc].type === 'quantitative'
              ) {
                nObj[enc] = nObj[enc].toLocaleString('de-CH')
              }
            }
          })
          return nObj
        } else {
          return false
        }
      })
    } catch (error) {
      /* eslint-disable no-console */
      console.error(error)
      /* eslint-enable no-console */
    }
  },
}
</script>

<!-- prettier-ignore -->
<style lang="postcss">
.gaugegrid {
  @apply grid grid-cols-2;
  align-items: center;
  background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 2 2' preserveAspectRatio='none'%3E%3Crect width='2' height='2' fill='%230F05A0' /%3E%3Crect width='1' height='1' fill='%236496FF'/%3E%3Crect x='1' y='1' width='1' height='1' fill='%236496FF'/%3E%3C/svg%3E")
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
