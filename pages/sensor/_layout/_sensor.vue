<template>
  <div class="container">
    <Header />
    <div>
      <h1 class="title">{{ data.titel }}</h1>
      <div class="gaugegrid">
        <Gauge
          v-for="gauge in data.gauges"
          :key="gauge.label"
          :label="gauge.label"
          :value="gauge.value"
          :unit="gauge.unit"
        />
      </div>
      <div class="description">
        <p>{{ data.description }}</p>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import axios from 'axios'

export default {
  async asyncData({ route }) {
    const url = [
      'http://transparenzrh.vercel.app/api/v1',
      route.params.layout,
      route.params.sensor,
    ].join('/')
    console.log(url)
    try {
      const { data } = await axios.get(url)
      console.log(data)
      return { data }
    } catch (err) {
      console.error(err)
      return { data: { titel: '', gauges: [], description: '' } }
    }
  },
  methods: {},
}
</script>

<!-- prettier-ignore -->
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
