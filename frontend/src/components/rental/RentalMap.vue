<template>
  <div class="relative rounded-card overflow-hidden border border-border" :style="{ height: size + 'px', background: 'rgb(var(--c-surface-2))' }">
    <svg :width="'100%'" :height="size" :viewBox="`0 0 ${size} ${size}`">
      <!-- 网格背景 -->
      <defs>
        <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
          <path d="M32 0 L0 0 0 32" fill="none" stroke="rgb(var(--c-border))" stroke-width="1" opacity="0.5" />
        </pattern>
      </defs>
      <rect :width="size" :height="size" fill="url(#grid)" />

      <!-- 通勤圈 -->
      <g v-for="(c, i) in rings" :key="'ring' + i">
        <circle :cx="cx" :cy="cy" :r="c.r" :fill="c.fill" :stroke="c.stroke" stroke-width="1.5" stroke-dasharray="4 4" />
        <text v-if="c.r > 24" :x="cx" :y="cy - c.r + 14" text-anchor="middle" class="fill-ink-soft" style="font-size:10px">{{ c.minutes }}min</text>
      </g>

      <!-- 房源点 -->
      <g v-for="l in points" :key="l.id" class="cursor-pointer" @click="$emit('select', l)">
        <circle :cx="l.x" :cy="l.y" r="7" :fill="l.color" stroke="#fff" stroke-width="2" />
        <title>{{ l.title }} · ¥{{ l.price_monthly }}</title>
      </g>

      <!-- 公司中心 -->
      <g>
        <circle :cx="cx" :cy="cy" r="13" fill="rgb(var(--c-danger))" stroke="#fff" stroke-width="3" />
        <text :x="cx" :y="cy + 4" text-anchor="middle" fill="#fff" style="font-size:13px" class="material-symbols-outlined">business</text>
      </g>
    </svg>

    <!-- 图例 -->
    <div class="absolute bottom-2 left-2 glass rounded-btn px-2.5 py-1.5 text-xs space-y-0.5 border border-border">
      <div class="flex items-center gap-1.5"><i class="w-2.5 h-2.5 rounded-full" style="background:rgb(var(--c-danger))"></i>公司位置</div>
      <div class="flex items-center gap-1.5"><i class="w-2.5 h-2.5 rounded-full bg-success"></i>≤通勤近</div>
      <div class="flex items-center gap-1.5"><i class="w-2.5 h-2.5 rounded-full bg-warning"></i>通勤中</div>
    </div>
    <div class="absolute top-2 right-2 glass rounded-btn px-2.5 py-1 text-xs border border-border">{{ points.length }} 套房源</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  center: { type: Object, required: true }, // {lng, lat}
  listings: { type: Array, default: () => [] },
  circles: { type: Array, default: () => [] }, // [{minutes, radius_m, count}]
  size: { type: Number, default: 460 },
})
defineEmits(['select'])

const cx = computed(() => props.size / 2)
const cy = computed(() => props.size / 2)

// 米/度 与缩放：把最远房源(或1500m)缩放进半径 ~200px
const scale = computed(() => {
  let maxD = 1500
  for (const l of props.listings) maxD = Math.max(maxD, dist(l))
  return 195 / maxD
})
function meters(l) {
  const dx = (l.lng - props.center.lng) * 111000 * Math.cos((props.center.lat * Math.PI) / 180)
  const dy = (l.lat - props.center.lat) * 111000
  return { dx, dy }
}
function dist(l) { const { dx, dy } = meters(l); return Math.sqrt(dx * dx + dy * dy) }

const points = computed(() =>
  props.listings.map((l) => {
    const { dx, dy } = meters(l)
    const m = l.commute_minutes ?? 30
    return {
      ...l,
      x: cx.value + dx * scale.value,
      y: cy.value - dy * scale.value,
      color: m <= 20 ? 'rgb(var(--c-success))' : m <= 35 ? 'rgb(var(--c-warning))' : 'rgb(var(--c-ink-soft))',
    }
  })
)
const ringColors = ['rgb(var(--c-primary))', 'rgb(var(--c-accent))', 'rgb(var(--c-mint))', 'rgb(var(--c-ink-soft))']
const rings = computed(() =>
  props.circles
    .map((c, i) => ({
      minutes: c.minutes,
      r: c.radius_m * scale.value,
      fill: `${ringColors[i % 4].replace('rgb', 'rgba').replace(')', ' / 0.05)')}`,
      stroke: ringColors[i % 4],
    }))
    .filter((c) => c.r < props.size / 2)
    .sort((a, b) => b.r - a.r)
)
</script>
