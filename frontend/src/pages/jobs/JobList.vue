<template>
  <div>
    <PageHeader title="职位匹配" subtitle="智能匹配度 · 差距分析 · 每日推荐">
      <template #actions>
        <RouterLink to="/jobs/applications" class="lp-btn-outline"><span class="material-symbols-outlined" style="font-size:18px">view_kanban</span>投递追踪</RouterLink>
        <button class="lp-btn-primary" @click="showAdd = true"><span class="material-symbols-outlined" style="font-size:18px">add</span>粘贴 JD</button>
      </template>
    </PageHeader>

    <!-- 筛选 -->
    <div class="flex flex-wrap items-center gap-2 mb-5">
      <div class="relative">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-ink-soft/60" style="font-size:18px">search</span>
        <input v-model="keyword" class="lp-input !pl-9 !w-56" placeholder="搜索职位" @keyup.enter="load" />
      </div>
      <button v-for="c in cities" :key="c" class="lp-chip" :class="city === c ? '!bg-primary !text-on-primary' : ''" @click="city = city === c ? '' : c; load()">{{ c }}</button>
      <label class="flex items-center gap-2 text-sm text-ink-soft ml-2"><input type="checkbox" v-model="onlyRecommended" class="accent-[rgb(var(--c-primary))]" @change="load" />仅看高匹配推荐</label>
    </div>

    <div v-if="jobs.length" class="grid sm:grid-cols-2 gap-4">
      <RouterLink v-for="j in jobs" :key="j.id" :to="`/jobs/${j.id}`" class="lp-card p-5 hover:shadow-lift hover:border-primary/40 transition-all">
        <div class="flex items-start justify-between mb-2">
          <div class="flex items-center gap-3">
            <div class="w-11 h-11 rounded-btn bg-primary-soft text-primary flex items-center justify-center font-bold">{{ (j.company?.name || '公')[0] }}</div>
            <div>
              <h3 class="font-display font-bold text-ink">{{ j.title }}</h3>
              <p class="text-sm text-ink-soft">{{ j.company?.name }} · {{ j.location_city }}</p>
            </div>
          </div>
          <MatchBadge v-if="j.match != null" :value="j.match" />
        </div>
        <div class="flex items-center justify-between mt-3">
          <span class="font-display font-bold text-accent">{{ salaryText(j) }}</span>
          <div class="flex gap-1">
            <span v-for="t in (j.job_tags || []).slice(0,2)" :key="t" class="lp-tag bg-surface-2 text-ink-soft">{{ t }}</span>
          </div>
        </div>
      </RouterLink>
    </div>
    <div v-else-if="loaded" class="lp-card"><EmptyState icon="work" title="暂无职位" /></div>

    <!-- 添加 JD 弹窗 -->
    <div v-if="showAdd" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showAdd = false">
      <div class="lp-card p-6 w-full max-w-lg lp-fade">
        <h3 class="lp-section-title mb-4">手动添加职位 / 投递</h3>
        <div class="grid grid-cols-2 gap-3 mb-3">
          <input v-model="addForm.company_name" class="lp-input" placeholder="公司名" />
          <input v-model="addForm.position_title" class="lp-input" placeholder="职位名" />
        </div>
        <textarea v-model="addForm.jd" rows="4" class="lp-input mb-3" placeholder="粘贴 JD 文本（用于匹配度分析）"></textarea>
        <div v-if="addMatch" class="mb-3 flex items-center gap-2"><MatchBadge :value="addMatch.overall" /><span class="text-sm text-ink-soft">匹配度分析完成</span></div>
        <div class="flex justify-end gap-2">
          <button class="lp-btn-outline" :disabled="!addForm.jd" @click="analyze">分析匹配度</button>
          <button class="lp-btn-primary" @click="addApplication">加入投递看板</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import MatchBadge from '@/components/jobs/MatchBadge.vue'

const route = useRoute()
const jobs = ref([])
const loaded = ref(false)
const keyword = ref(route.query.q || '')
const city = ref('')
const onlyRecommended = ref(true)
const cities = ['深圳', '广州', '杭州', '北京', '上海']
const showAdd = ref(false)
const addForm = reactive({ company_name: '', position_title: '', jd: '' })
const addMatch = ref(null)

function salaryText(j) {
  if (!j.salary_min) return '面议'
  return `${Math.round(j.salary_min / 1000)}-${Math.round(j.salary_max / 1000)}K`
}
async function load() {
  loaded.value = false
  if (onlyRecommended.value && !keyword.value && !city.value) {
    jobs.value = await api.get('/jobs/recommended')
  } else {
    const params = new URLSearchParams()
    if (city.value) params.set('city', city.value)
    if (keyword.value) params.set('keyword', keyword.value)
    jobs.value = await api.get(`/jobs/positions?${params}`)
  }
  loaded.value = true
}
async function analyze() {
  addMatch.value = await api.post('/jobs/match', { jd_text: addForm.jd })
}
async function addApplication() {
  await api.post('/jobs/applications', {
    company_name: addForm.company_name || '未命名公司',
    position_title: addForm.position_title || '未命名职位',
    status: 'saved',
    notes: addForm.jd,
  })
  showAdd.value = false
  alert('已加入投递看板的「待投递」列')
}
onMounted(load)
</script>
