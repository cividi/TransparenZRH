<template>
  <div class="gauge">
    <div class="gaugecontent">
      <div class="gauge__readout gauge__label">{{ label }}</div>
      <div class="gauge__readout gauge__value">{{ value }}</div>
      <div class="gauge__readout gauge__unit">{{ unit }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: { type: String, default: '' },
    value: { type: String, default: '...' },
    unit: { type: String, default: '' },
  },
}
</script>

<style scoped lang="postcss">
.gauge {
  @apply text-white;
  min-height: 50vw;
  display: grid;
  align-items: center;
  text-align: center;
}
.gauge__readout {
}
.gauge__value {
  @apply text-4xl font-bold;
}
.gauge__unit {
  @apply font-light text-xs;
}
.gauge__label {
  @apply pb-1 pl-4 pr-4;
}
</style>
