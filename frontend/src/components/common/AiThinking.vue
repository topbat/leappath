<template>
  <div class="inline-flex items-center gap-2 text-primary">
    <span class="material-symbols-outlined ms-fill" style="font-size:18px">auto_awesome</span>
    <span class="text-sm font-medium">{{ text }}</span>
    <span class="flex gap-0.5">
      <i class="lp-dot w-1.5 h-1.5 rounded-full bg-primary"></i>
      <i class="lp-dot w-1.5 h-1.5 rounded-full bg-primary" style="animation-delay:.2s"></i>
      <i class="lp-dot w-1.5 h-1.5 rounded-full bg-primary" style="animation-delay:.4s"></i>
    </span>
  </div>
</template>

<script setup>
defineProps({ text: { type: String, default: 'AI 思考中' } })
</script>
