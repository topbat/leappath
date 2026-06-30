<template>
  <div>
    <div v-if="label || showValue" class="flex items-center justify-between mb-1.5">
      <span class="text-sm font-medium text-ink-soft">{{ label }}</span>
      <span v-if="showValue" class="text-sm font-bold text-ink">{{ value }}{{ suffix }}</span>
    </div>
    <div class="h-2.5 rounded-pill bg-surface-2 overflow-hidden">
      <div
        class="h-full rounded-pill"
        :class="colorClass"
        :style="{ width: Math.min(100, (value / max) * 100) + '%', transition: 'width .7s ease' }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  value: { type: Number, default: 0 },
  max: { type: Number, default: 100 },
  label: { type: String, default: '' },
  showValue: { type: Boolean, default: true },
  suffix: { type: String, default: '%' },
  color: { type: String, default: 'primary' },
})
const colorClass = computed(() => ({
  primary: 'bg-primary',
  success: 'bg-success',
  warning: 'bg-warning',
  accent: 'bg-accent',
}[props.color] || 'bg-primary'))
</script>
