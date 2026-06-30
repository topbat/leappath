<template>
  <div class="relative inline-flex items-center justify-center">
    <svg :width="size" :height="size" viewBox="0 0 120 120" class="-rotate-90">
      <circle cx="60" cy="60" :r="r" fill="none" stroke="rgb(var(--c-surface-2))" :stroke-width="stroke" />
      <circle
        cx="60" cy="60" :r="r" fill="none" stroke="rgb(var(--c-primary))" :stroke-width="stroke"
        stroke-linecap="round" :stroke-dasharray="circ" :stroke-dashoffset="offset"
        style="transition: stroke-dashoffset .8s ease"
      />
    </svg>
    <div class="absolute inset-0 flex flex-col items-center justify-center">
      <span class="font-display font-extrabold text-ink leading-none" :style="{ fontSize: size / 3.6 + 'px' }">{{ display }}</span>
      <span v-if="label" class="text-xs text-ink-soft mt-1">{{ label }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  value: { type: Number, default: 0 },
  max: { type: Number, default: 100 },
  size: { type: Number, default: 140 },
  stroke: { type: Number, default: 10 },
  label: { type: String, default: '' },
  suffix: { type: String, default: '' },
})
const r = 60 - props.stroke / 2 - 2
const circ = computed(() => 2 * Math.PI * r)
const offset = computed(() => circ.value * (1 - Math.min(1, props.value / props.max)))
const display = computed(() => `${props.value}${props.suffix}`)
</script>
