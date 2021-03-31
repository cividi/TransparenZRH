<template>
  <div class="gauge">
    <div class="gaugecontent">
      <div>
        <div class="gauge__readout gauge__value">{{ value }}</div>
        <div class="gauge__readout gauge__unit">{{ unit }}</div>
      </div>
      <div class="gauge__readout gauge__label">{{ label }}</div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['label', 'value', 'unit'],
}
</script>

<style scoped>
.gauge {
  @apply text-white;
  min-height: 50vw;
  display: grid;
  align-items: center;
}
.gauge__readout {
  display: inline-block;
}
.gauge__value {
  @apply text-4xl font-bold;
}
.gauge__unit {
  @apply font-light text-xs;
}
.gauge__label {
  @apply pt-2;
}
</style>
