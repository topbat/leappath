<template>
  <div>
    <PageHeader title="公司对比" subtitle="多维横向对比，辅助决策" back />

    <div class="lp-card p-5 mb-5">
      <p class="text-sm text-ink-soft mb-2">选择要对比的公司（最多 4 家）</p>
      <div class="flex flex-wrap gap-2">
        <button v-for="c in all" :key="c.id" class="lp-chip" :class="selected.includes(c.id) ? '!bg-primary !text-on-primary' : ''" @click="toggle(c.id)">{{ c.short_name || c.name }}</button>
      </div>
    </div>

    <div v-if="rows.length" class="lp-card p-6 overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="text-left text-ink-soft border-b border-border">
            <th class="py-2 pr-4 font-medium">维度</th>
            <th v-for="r in rows" :key="r.id" class="py-2 px-4 font-display font-bold text-ink">{{ r.name }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dim in dims" :key="dim.key" class="border-b border-border/60">
            <td class="py-3 pr-4 text-ink-soft">{{ dim.label }}</td>
            <td v-for="r in rows" :key="r.id" class="py-3 px-4 text-ink">{{ dim.fmt(r) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <EmptyState v-else icon="compare" title="请选择至少 2 家公司进行对比" />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const all = ref([])
const selected = ref([])
const rows = ref([])
const stageLabel = { angel: '天使轮', A: 'A 轮', B: 'B 轮', C: 'C 轮', listed: '已上市' }
const diffLabel = { low: '低', medium: '中', high: '高', extreme: '极高' }
const dims = [
  { key: 'industry', label: '行业', fmt: (r) => r.industry || '—' },
  { key: 'size', label: '规模', fmt: (r) => (r.size_range || '—') + ' 人' },
  { key: 'stage', label: '融资阶段', fmt: (r) => stageLabel[r.financing_stage] || r.financing_stage || '—' },
  { key: 'city', label: '城市', fmt: (r) => r.location_city || '—' },
  { key: 'salary', label: '平均月薪', fmt: (r) => (r.avg_salary ? Math.round(r.avg_salary / 1000) + 'K' : '—') },
  { key: 'difficulty', label: '求职难度', fmt: (r) => diffLabel[r.difficulty_level] || '—' },
  { key: 'culture', label: '文化标签', fmt: (r) => (r.culture_tags || []).slice(0, 3).join(' / ') || '—' },
]
function toggle(id) {
  const i = selected.value.indexOf(id)
  if (i >= 0) selected.value.splice(i, 1)
  else if (selected.value.length < 4) selected.value.push(id)
}
watch(selected, async (ids) => {
  if (ids.length >= 2) rows.value = await api.post('/companies/compare', { company_ids: ids })
  else rows.value = []
}, { deep: true })
onMounted(async () => {
  all.value = await api.get('/companies')
  selected.value = all.value.slice(0, 2).map((c) => c.id)
})
</script>
