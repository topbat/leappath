<template>
  <span class="lp-tag" :class="cls">匹配 {{ value }}%</span>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ value: { type: Number, default: 0 } })
const cls = computed(() => {
  if (props.value >= 80) return 'bg-success/15 text-success'
  if (props.value >= 60) return 'bg-warning/15 text-warning'
  return 'bg-danger/12 text-danger'
})
</script>
