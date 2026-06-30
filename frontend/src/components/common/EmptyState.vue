<template>
  <div class="flex flex-col items-center justify-center py-16 text-center lp-fade">
    <div class="w-16 h-16 rounded-full bg-surface-2 flex items-center justify-center text-ink-soft/60 mb-4">
      <span class="material-symbols-outlined" style="font-size:32px">{{ icon }}</span>
    </div>
    <p class="text-ink-soft font-medium">{{ title }}</p>
    <p v-if="desc" class="text-sm text-ink-soft/70 mt-1 max-w-xs">{{ desc }}</p>
    <slot />
  </div>
</template>

<script setup>
defineProps({
  icon: { type: String, default: 'inbox' },
  title: { type: String, default: '暂无数据' },
  desc: { type: String, default: '' },
})
</script>
