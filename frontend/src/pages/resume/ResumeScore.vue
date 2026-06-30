<template>
  <div>
    <PageHeader title="简历评分" subtitle="五维度智能评分 + 按优先级排序的改进建议" back>
      <template #actions>
        <button class="lp-btn-primary" :disabled="loading" @click="run"><span class="material-symbols-outlined" style="font-size:18px">refresh</span>{{ loading ? '评分中…' : '重新评分' }}</button>
      </template>
    </PageHeader>

    <div v-if="result" class="grid grid-cols-1 lg:grid-cols-12 gap-5">
      <div class="lg:col-span-4 lp-card p-6 flex flex-col items-center justify-center">
        <ScoreRing :value="result.score_total" :size="170" :stroke="12" />
        <p class="mt-3 font-display font-bold text-lg" :style="{ color: gradeColor }">{{ result.grade }}</p>
        <p class="text-sm text-ink-soft">综合评分</p>
      </div>

      <div class="lg:col-span-8 lp-card p-6">
        <h3 class="lp-section-title mb-4">维度得分</h3>
        <div class="grid sm:grid-cols-2 gap-x-8 gap-y-4">
          <ProgressBar
            v-for="(v, k) in result.breakdown" :key="k"
            :label="`${v.label}（权重 ${v.weight}%）`" :value="v.score" suffix=" 分"
            :color="v.score >= 85 ? 'success' : v.score >= 70 ? 'primary' : 'warning'"
          />
        </div>
        <div class="mt-6">
          <RadarChart
            :labels="Object.values(result.breakdown).map(v => v.label)"
            :series="[{ values: Object.values(result.breakdown).map(v => v.score / 20) }]"
            :max="5" :size="240"
          />
        </div>
      </div>

      <div class="lg:col-span-12 lp-card p-6">
        <h3 class="lp-section-title mb-4">改进建议（按优先级）</h3>
        <div class="space-y-2.5">
          <div v-for="(s, i) in result.suggestions" :key="i" class="flex items-start gap-3 p-3 rounded-btn bg-surface-2">
            <span class="lp-tag shrink-0" :class="levelCls(s.level)">{{ levelLabel(s.level) }}</span>
            <p class="text-sm text-ink">{{ s.text }}</p>
          </div>
        </div>
        <div class="flex gap-2 mt-5">
          <RouterLink :to="`/resume/${id}/optimize`" class="lp-btn-primary">去 AI 润色</RouterLink>
          <RouterLink :to="`/resume/${id}`" class="lp-btn-outline">返回编辑</RouterLink>
        </div>
      </div>
    </div>
    <div v-else class="flex justify-center py-24"><AiThinking text="AI 正在评分" /></div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import ScoreRing from '@/components/charts/ScoreRing.vue'
import ProgressBar from '@/components/charts/ProgressBar.vue'
import RadarChart from '@/components/charts/RadarChart.vue'
import AiThinking from '@/components/common/AiThinking.vue'

const route = useRoute()
const id = route.params.id
const result = ref(null)
const loading = ref(false)

const gradeColor = computed(() => {
  const t = result.value?.score_total || 0
  return t >= 85 ? 'rgb(var(--c-success))' : t >= 70 ? 'rgb(var(--c-primary))' : 'rgb(var(--c-warning))'
})
function levelLabel(l) { return { critical: '🔴 关键', suggest: '🟡 建议', optimize: '🟢 优化' }[l] || l }
function levelCls(l) { return { critical: 'bg-danger/12 text-danger', suggest: 'bg-warning/15 text-warning', optimize: 'bg-success/15 text-success' }[l] }

async function run() {
  loading.value = true
  try { result.value = await api.post(`/resumes/${id}/score`) } finally { loading.value = false }
}
onMounted(run)
</script>
