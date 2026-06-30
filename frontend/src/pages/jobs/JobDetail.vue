<template>
  <div v-if="job">
    <PageHeader :title="job.title" :subtitle="`${job.company?.name || ''} · ${job.location_city || ''}`" back>
      <template #actions>
        <button class="lp-btn-outline" @click="analyzeMatch"><span class="material-symbols-outlined" style="font-size:18px">insights</span>匹配分析</button>
        <button class="lp-btn-primary" @click="apply"><span class="material-symbols-outlined" style="font-size:18px">send</span>加入投递</button>
      </template>
    </PageHeader>

    <div class="grid lg:grid-cols-12 gap-5">
      <div class="lg:col-span-8 space-y-5">
        <div class="lp-card p-6">
          <div class="flex flex-wrap items-center gap-3 mb-4">
            <span class="font-display text-xl font-extrabold text-accent">{{ salaryText }}</span>
            <span class="lp-chip">{{ job.experience_required || '经验不限' }}</span>
            <span class="lp-chip">{{ job.education_required || '学历不限' }}</span>
            <span v-for="t in job.job_tags || []" :key="t" class="lp-tag bg-primary-soft text-primary">{{ t }}</span>
          </div>
          <h3 class="lp-section-title mb-2">职位描述</h3>
          <p class="text-ink whitespace-pre-line mb-4">{{ job.job_description }}</p>
          <h3 class="lp-section-title mb-2">任职要求</h3>
          <p class="text-ink whitespace-pre-line">{{ job.job_requirements }}</p>
        </div>

        <!-- 差距分析 -->
        <div v-if="match" class="lp-card p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="lp-section-title">匹配度与差距分析</h3>
            <MatchBadge :value="match.overall" />
          </div>
          <div class="grid sm:grid-cols-2 gap-x-8 gap-y-3 mb-4">
            <ProgressBar v-for="(v, k) in match.dimensions" :key="k" :label="dimLabel[k]" :value="v" :color="v >= 80 ? 'success' : v >= 60 ? 'primary' : 'warning'" />
          </div>
          <div class="grid sm:grid-cols-2 gap-4">
            <div>
              <p class="text-sm font-semibold text-success mb-2">✅ 匹配点</p>
              <div class="flex flex-wrap gap-1.5"><span v-for="k in match.matched" :key="k" class="lp-tag bg-success/15 text-success">{{ k }}</span></div>
            </div>
            <div>
              <p class="text-sm font-semibold text-danger mb-2">❌ 差距点</p>
              <div class="flex flex-wrap gap-1.5"><span v-for="k in match.missing" :key="k" class="lp-tag bg-danger/12 text-danger">{{ k }}</span></div>
            </div>
          </div>
          <div v-if="match.gaps?.length" class="mt-4 space-y-2">
            <p class="text-sm font-semibold text-ink mb-1">💡 补齐建议</p>
            <div v-for="(g, i) in match.gaps" :key="i" class="text-sm text-ink-soft p-2.5 rounded-btn bg-surface-2">{{ g.suggestion }}</div>
          </div>
        </div>
      </div>

      <div class="lg:col-span-4 space-y-5">
        <div v-if="job.company" class="lp-card p-6">
          <h3 class="lp-section-title mb-3">公司信息</h3>
          <div class="flex items-center gap-3 mb-3">
            <div class="w-12 h-12 rounded-btn bg-primary-soft text-primary flex items-center justify-center font-bold text-lg">{{ job.company.name[0] }}</div>
            <div><p class="font-display font-bold text-ink">{{ job.company.short_name || job.company.name }}</p><p class="text-sm text-ink-soft">{{ job.company.industry }} · {{ job.company.size_range }}人</p></div>
          </div>
          <RouterLink :to="`/company/${job.company_id}`" class="lp-btn-outline w-full">查看公司画像</RouterLink>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex justify-center py-24"><AiThinking text="加载职位" /></div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import ProgressBar from '@/components/charts/ProgressBar.vue'
import MatchBadge from '@/components/jobs/MatchBadge.vue'
import AiThinking from '@/components/common/AiThinking.vue'

const route = useRoute()
const id = route.params.id
const job = ref(null)
const match = ref(null)
const dimLabel = { skill: '技能匹配', experience: '经验匹配', education: '学历匹配', salary: '薪资匹配', location: '地点匹配' }

const salaryText = computed(() => {
  if (!job.value?.salary_min) return '面议'
  return `${Math.round(job.value.salary_min / 1000)}-${Math.round(job.value.salary_max / 1000)}K`
})
async function analyzeMatch() {
  match.value = await api.post('/jobs/match', { jd_text: (job.value.job_description || '') + ' ' + (job.value.job_requirements || '') })
}
async function apply() {
  await api.post('/jobs/applications', {
    position_id: job.value.id,
    company_name: job.value.company?.name || '公司',
    position_title: job.value.title,
    salary_label: salaryText.value,
    status: 'saved',
  })
  alert('已加入投递看板')
}
onMounted(async () => { job.value = await api.get(`/jobs/positions/${id}`); analyzeMatch() })
</script>
