<template>
  <div class="mb-3">
    <h3 class="text-xs font-bold uppercase tracking-wide mb-1.5 pb-1 border-b" style="color:rgb(var(--c-primary)); border-color:#eee">{{ title }}</h3>
    <slot />
  </div>
</template>

<script setup>
defineProps({ title: { type: String, required: true } })
</script>
