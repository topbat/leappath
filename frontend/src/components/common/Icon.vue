<template>
  <span class="material-symbols-outlined" :class="[fill ? 'ms-fill' : '', sizeClass]" :style="style">
    <slot>{{ name }}</slot>
  </span>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  name: { type: String, default: '' },
  fill: { type: Boolean, default: false },
  size: { type: [Number, String], default: 24 },
})
const sizeClass = ''
const style = computed(() => ({ fontSize: `${props.size}px`, lineHeight: 1 }))
</script>
