<template>
  <div v-if="report">
    <PageHeader title="面试报告" :subtitle="`${typeLabel} · 时长 ${duration} · ${date}`" back>
      <template #actions>
        <RouterLink to="/interview/setup" class="lp-btn-primary">再次练习</RouterLink>
      </template>
    </PageHeader>

    <div class="grid lg:grid-cols-12 gap-5">
      <div class="lg:col-span-4 lp-card p-6 flex flex-col items-center justify-center">
        <ScoreRing :value="report.overall_score" :max="10" :size="170" :stroke="12" />
        <p class="mt-3 font-display font-bold text-lg" :style="{ color: report.overall_score >= 7 ? 'rgb(var(--c-success))' : 'rgb(var(--c-warning))' }">{{ report.overall_score >= 8 ? '优秀' : report.overall_score >= 6 ? '良好' : '待提升' }}</p>
        <p class="text-sm text-ink-soft">综合评分 / 10</p>
      </div>

      <div class="lg:col-span-8 lp-card p-6">
        <h3 class="lp-section-title mb-4">能力维度</h3>
        <div class="grid sm:grid-cols-2 gap-x-8 gap-y-4 mb-4">
          <ProgressBar v-for="(v, k) in report.score_breakdown" :key="k" :label="k" :value="v" :max="10" suffix=" / 10" :color="v >= 8 ? 'success' : v >= 6 ? 'primary' : 'warning'" />
        </div>
        <RadarChart :labels="Object.keys(report.score_breakdown)" :series="[{ values: Object.values(report.score_breakdown) }]" :max="10" :size="220" />
      </div>

      <div class="lg:col-span-6 lp-card p-6">
        <h3 class="lp-section-title mb-3 text-success">优势</h3>
        <ul class="space-y-2">
          <li v-for="(s, i) in report.strengths" :key="i" class="flex gap-2 text-sm text-ink"><span class="material-symbols-outlined text-success" style="font-size:18px">check_circle</span>{{ s }}</li>
        </ul>
      </div>
      <div class="lg:col-span-6 lp-card p-6">
        <h3 class="lp-section-title mb-3 text-warning">待提升</h3>
        <ul class="space-y-2">
          <li v-for="(s, i) in report.weaknesses" :key="i" class="flex gap-2 text-sm text-ink"><span class="material-symbols-outlined text-warning" style="font-size:18px">error</span>{{ s }}</li>
        </ul>
      </div>

      <div class="lg:col-span-12 lp-card p-6">
        <h3 class="lp-section-title mb-3">提升建议</h3>
        <div class="grid sm:grid-cols-3 gap-3 mb-5">
          <div v-for="(s, i) in report.suggestions" :key="i" class="rounded-card bg-primary-soft p-4 text-sm text-primary font-medium">{{ s }}</div>
        </div>
        <h3 class="lp-section-title mb-3">逐题回顾</h3>
        <div class="space-y-2">
          <div v-for="q in report.question_reviews" :key="q.question_number" class="flex items-center gap-3 p-2.5 rounded-btn bg-surface-2">
            <span class="font-display font-bold text-ink-soft w-8">Q{{ q.question_number }}</span>
            <div class="flex-1">
              <div class="flex items-center gap-1 text-warning">
                <span v-for="n in 5" :key="n" class="material-symbols-outlined" :class="n <= Math.round(q.score / 2) ? 'ms-fill' : ''" style="font-size:16px">star</span>
                <span class="text-ink-soft text-sm ml-1">{{ q.score }}/9</span>
              </div>
              <p class="text-sm text-ink-soft">{{ q.comment }}</p>
            </div>
          </div>
        </div>
        <div class="mt-5 p-4 rounded-card border border-border bg-surface-2 text-sm text-ink-soft">{{ report.summary }}</div>
      </div>
    </div>
  </div>
  <div v-else class="flex justify-center py-24"><AiThinking text="生成报告中" /></div>
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
const report = ref(null)
const labels = { technical: '技术面', behavioral: '行为面', hr: 'HR 面', case: '案例面' }
const typeLabel = computed(() => labels[report.value?.session?.interview_type] || '面试')
const duration = computed(() => {
  const s = report.value?.session?.duration_seconds || 0
  return s ? `${Math.round(s / 60)} 分钟` : '—'
})
const date = computed(() => report.value?.session?.completed_at?.slice(0, 10) || '')

onMounted(async () => {
  try { report.value = await api.get(`/interviews/sessions/${id}/report`) }
  catch { report.value = await api.post(`/interviews/sessions/${id}/finish`).then(() => api.get(`/interviews/sessions/${id}/report`)) }
})
</script>
