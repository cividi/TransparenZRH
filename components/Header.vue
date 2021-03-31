<template>
  <header>
    <div class="grid grid-cols-4">
      <img src="~/assets/Logo_der_Stadt_Zürich.svg" class="logo" />
      <div class="header__text col-start-2 col-end-5" v-if="!simple">
        Digitale Transparenz<br />im öffentlichen Raum
      </div>
    </div>
  </header>
</template>

<style scoped>
header {
  /* @apply fixed top-0 w-screen h-12 bg-zueriblue text-white; */
}

img.logo {
  @apply pt-4 pl-4;
}

.header__text {
  @apply p-4 text-sm text-coolgray-100;
}
</style>

<script>
export default {
  props: ['simple'],
}
</script>
