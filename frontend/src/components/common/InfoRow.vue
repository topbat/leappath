<template>
  <div class="flex justify-between items-center py-2 border-b border-border/50">
    <span class="text-ink-soft text-sm">{{ label }}</span>
    <span :class="highlight ? 'font-display font-bold text-primary text-lg' : 'text-ink font-medium'">{{ value }}</span>
  </div>
</template>

<script setup>
defineProps({ label: String, value: [String, Number], highlight: Boolean })
</script>
