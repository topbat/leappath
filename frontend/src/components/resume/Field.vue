<template>
  <label class="block">
    <span class="text-sm font-medium text-ink-soft mb-1.5 block">{{ label }}</span>
    <slot />
  </label>
</template>

<script setup>
defineProps({ label: { type: String, default: '' } })
</script>
