<template>
  <div class="gauge">
    <div class="gaugecontent">
      <div>{{ value }}</div>
      <div>{{ unit }}</div>
      <div>{{ label }}</div>
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
  @apply bg-zueriblue text-white;
}
.gaugecontent {
  @apply container pt-10 pb-10;
}
</style>
