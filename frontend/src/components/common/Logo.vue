<template>
  <div class="flex items-center gap-2.5 select-none">
    <svg :width="size" :height="size" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" class="shrink-0">
      <defs>
        <linearGradient :id="gid" x1="16" y1="104" x2="104" y2="16" gradientUnits="userSpaceOnUse">
          <stop stop-color="rgb(var(--c-primary))" />
          <stop offset="1" stop-color="rgb(var(--c-accent))" />
        </linearGradient>
      </defs>
      <rect x="4" y="4" width="112" height="112" rx="28" :fill="`url(#${gid})`" />
      <path d="M28 84 L48 84 L48 64 L68 64 L68 44 L88 44" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.92" />
      <circle cx="92" cy="30" r="11" fill="#fff" />
      <circle cx="92" cy="30" r="5" :fill="`url(#${gid})`" />
    </svg>
    <div v-if="showText" class="leading-none">
      <div class="font-display font-extrabold text-ink" :style="{ fontSize: textSize + 'px' }">跃途<span class="text-primary ml-1">LeapPath</span></div>
      <div v-if="tagline" class="text-[11px] text-ink-soft mt-1">全生命周期 AI 求职助手</div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  size: { type: Number, default: 36 },
  showText: { type: Boolean, default: true },
  tagline: { type: Boolean, default: false },
  textSize: { type: Number, default: 18 },
})
const gid = computed(() => 'lp-logo-' + Math.random().toString(36).slice(2, 8))
</script>
