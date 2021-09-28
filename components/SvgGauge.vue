<template>
  <div class="gauge">
    <div class="gaugecontent">
      <div class="gauge__readout gauge__label">{{ label }}</div>
      <div class="gauge__readout gauge__svg">
        <img class="gauge__svg__img" :src="svg" />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: { type: String, default: '' },
    svg: { type: String, default: '' },
  },
}
</script>

<style scoped lang="postcss">
.gauge {
  @apply text-white bg-zueriblue;
  height: 50vw;
  width: 98vw;
  display: grid;
  align-items: center;
  text-align: center;
}
.gauge__readout {
}
img.gauge__svg__img {
  margin: auto;
  width: 90%;
}
.gauge__label {
  @apply pb-2;
}
</style>
