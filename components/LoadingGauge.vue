<template>
  <div class="gauge">
    <div class="gaugecontent">
      <div class="gauge__readout gauge__label"></div>
      <div class="gauge__readout gauge__value">
        <div class="loading__container">
          <div class="loading__dot"></div>
          <div class="loading__dot"></div>
          <div class="loading__dot"></div>
        </div>
      </div>
      <div class="gauge__readout gauge__unit"></div>
    </div>
  </div>
</template>

<script></script>

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
  @apply pb-2;
}
.loading__container {
  @apply w-20 h-4 m-auto flex space-x-2 items-center justify-center animate-pulse;
}
.loading__dot {
  @apply w-2 h-2 bg-white rounded-full;
}
</style>
