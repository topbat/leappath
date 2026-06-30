<template>
  <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`">
    <!-- grid rings -->
    <polygon
      v-for="(lvl, li) in levels" :key="'g' + li"
      :points="ringPoints(lvl)" fill="none" stroke="rgb(var(--c-border))" stroke-width="1"
    />
    <!-- axes -->
    <line v-for="(a, i) in axes" :key="'a' + i" :x1="cx" :y1="cy" :x2="a.x" :y2="a.y" stroke="rgb(var(--c-border))" stroke-width="1" />
    <!-- series -->
    <polygon
      v-for="(s, si) in series" :key="'s' + si"
      :points="seriesPoints(s.values)" :fill="s.color || 'rgb(var(--c-primary) / 0.18)'"
      :stroke="s.stroke || 'rgb(var(--c-primary))'" stroke-width="2"
      style="transition: all .6s ease"
    />
    <!-- labels -->
    <text
      v-for="(a, i) in axes" :key="'t' + i" :x="a.lx" :y="a.ly"
      text-anchor="middle" dominant-baseline="middle"
      class="fill-ink-soft" style="font-size:11px"
    >{{ labels[i] }}</text>
  </svg>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  labels: { type: Array, required: true },
  series: { type: Array, required: true }, // [{values:[...], color, stroke}]
  max: { type: Number, default: 5 },
  size: { type: Number, default: 260 },
})
const cx = props.size / 2
const cy = props.size / 2
const radius = props.size / 2 - 34
const levels = [0.25, 0.5, 0.75, 1]
const n = computed(() => props.labels.length)

function point(i, ratio) {
  const ang = (Math.PI * 2 * i) / n.value - Math.PI / 2
  return { x: cx + radius * ratio * Math.cos(ang), y: cy + radius * ratio * Math.sin(ang) }
}
const axes = computed(() =>
  props.labels.map((_, i) => {
    const p = point(i, 1)
    const lp = point(i, 1.18)
    return { x: p.x, y: p.y, lx: lp.x, ly: lp.y }
  })
)
function ringPoints(lvl) {
  return props.labels.map((_, i) => { const p = point(i, lvl); return `${p.x},${p.y}` }).join(' ')
}
function seriesPoints(values) {
  return values.map((v, i) => { const p = point(i, Math.min(1, v / props.max)); return `${p.x},${p.y}` }).join(' ')
}
</script>
