<template>
  <header>
    <div class="grid grid-cols-4">
      <img src="~/assets/Logo_der_Stadt_Zürich.svg" class="logo" />
      <div v-if="!simple" class="header__text col-start-2 col-end-5">
        Digitale Transparenz<br />im öffentlichen Raum
      </div>
    </div>
  </header>
</template>

<script>
export default {
  props: {
    simple: Boolean,
  },
  computed: {
    isSimple: () => {
      if (this.simple) {
        return true
      } else {
        return false
      }
    },
  },
}
</script>

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
