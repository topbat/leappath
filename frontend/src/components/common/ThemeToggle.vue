<template>
  <button
    class="flex items-center gap-2 rounded-pill border border-border bg-surface px-3 py-1.5 text-sm font-medium text-ink-soft hover:border-primary hover:text-primary transition-all"
    @click="theme.toggle()"
    :title="`当前：${theme.label}，点击切换`"
  >
    <span class="material-symbols-outlined" style="font-size:18px">{{ theme.isFlux ? 'auto_awesome' : 'workspace_premium' }}</span>
    <span class="hidden sm:inline">{{ theme.label }}</span>
    <span class="flex gap-1">
      <i class="w-2.5 h-2.5 rounded-full" :class="theme.theme === 'leap' ? 'ring-2 ring-offset-1 ring-primary' : ''" style="background:#1A56DB"></i>
      <i class="w-2.5 h-2.5 rounded-full" :class="theme.theme === 'flux' ? 'ring-2 ring-offset-1 ring-primary' : ''" style="background:#7C3AED"></i>
    </span>
  </button>
</template>

<script setup>
import { useThemeStore } from '@/stores/theme'
const theme = useThemeStore()
</script>
