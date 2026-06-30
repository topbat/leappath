<template>
  <div v-if="data">
    <!-- 欢迎 -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
      <div>
        <h1 class="font-display text-2xl lg:text-3xl font-extrabold text-ink tracking-tight">
          {{ greeting }}，{{ data.user.nickname }} 👋
        </h1>
        <p class="text-ink-soft mt-1">
          本周有 <span class="text-primary font-bold">{{ data.application_stats.interview }}</span> 场面试，
          共 <span class="text-primary font-bold">{{ data.application_stats.total }}</span> 个职位在流程中，
          距目标入职还有 <span class="text-accent font-bold">{{ daysLeft }}</span> 天。
        </p>
      </div>
      <div class="flex gap-2">
        <RouterLink to="/resume/list" class="lp-btn-primary"><span class="material-symbols-outlined" style="font-size:20px">add</span>创建简历</RouterLink>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-12 gap-5">
      <!-- 左：进度 + 推荐 -->
      <div class="lg:col-span-8 space-y-5">
        <!-- 进度概览 -->
        <div class="lp-card p-6">
          <div class="flex items-center justify-between mb-5">
            <h2 class="lp-section-title">求职进度概览</h2>
            <span class="lp-tag bg-primary-soft text-primary">整体 {{ data.progress.overall }}%</span>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <div class="flex items-center gap-4">
              <ScoreRing :value="data.progress.resume" :size="84" :stroke="8" label="简历" />
              <div><p class="text-sm text-ink-soft">简历完善度</p><p class="font-display font-bold text-ink">{{ ratingText(data.progress.resume) }}</p></div>
            </div>
            <div class="flex items-center gap-4">
              <ScoreRing :value="data.progress.interview" :size="84" :stroke="8" label="面试" />
              <div><p class="text-sm text-ink-soft">面试练习</p><p class="font-display font-bold text-ink">{{ ratingText(data.progress.interview) }}</p></div>
            </div>
            <div class="flex items-center gap-4">
              <ScoreRing :value="data.progress.skill" :size="84" :stroke="8" label="技能" />
              <div><p class="text-sm text-ink-soft">技能提升</p><p class="font-display font-bold text-ink">{{ ratingText(data.progress.skill) }}</p></div>
            </div>
          </div>
        </div>

        <!-- 推荐职位 -->
        <div class="lp-card p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="lp-section-title">为你推荐</h2>
            <RouterLink to="/jobs/list" class="text-sm text-primary font-semibold flex items-center gap-1">查看全部 <span class="material-symbols-outlined" style="font-size:16px">arrow_forward</span></RouterLink>
          </div>
          <div v-if="jobs.length" class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <RouterLink
              v-for="j in jobs.slice(0, 3)" :key="j.id" :to="`/jobs/${j.id}`"
              class="rounded-card border border-border p-4 hover:border-primary hover:shadow-card transition-all group"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="w-9 h-9 rounded-btn bg-primary-soft text-primary flex items-center justify-center font-bold">{{ (j.company?.name || '公')[0] }}</div>
                <MatchBadge :value="j.match" />
              </div>
              <h3 class="font-display font-bold text-ink group-hover:text-primary line-clamp-1">{{ j.title }}</h3>
              <p class="text-sm text-ink-soft line-clamp-1">{{ j.company?.name }}</p>
              <p class="text-sm font-semibold text-accent mt-2">{{ salaryText(j) }}</p>
            </RouterLink>
          </div>
          <EmptyState v-else icon="work" title="暂无推荐职位" />
        </div>
      </div>

      <!-- 右：今日任务 + 投递统计 -->
      <div class="lg:col-span-4 space-y-5">
        <!-- 今日任务 -->
        <div class="lp-card p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="lp-section-title">今日任务</h2>
            <RouterLink to="/plan" class="text-sm text-primary font-semibold">{{ data.today_task_done }}/{{ data.today_tasks.length }}</RouterLink>
          </div>
          <div v-if="data.today_tasks.length" class="space-y-2">
            <label
              v-for="t in data.today_tasks" :key="t.id"
              class="flex items-center gap-3 p-2.5 rounded-btn hover:bg-surface-2 cursor-pointer transition-all"
            >
              <input type="checkbox" :checked="t.is_completed" class="w-5 h-5 accent-[rgb(var(--c-primary))]" @change="toggleTask(t)" />
              <span class="text-sm" :class="t.is_completed ? 'line-through text-ink-soft/60' : 'text-ink'">{{ t.title }}</span>
            </label>
          </div>
          <EmptyState v-else icon="task_alt" title="今天还没有任务" />
        </div>

        <!-- 投递统计 -->
        <div class="lp-card p-6">
          <h2 class="lp-section-title mb-4">投递追踪</h2>
          <div class="grid grid-cols-3 gap-3 text-center">
            <div v-for="s in stats" :key="s.key" class="rounded-btn bg-surface-2 py-3">
              <p class="font-display text-xl font-extrabold" :style="{ color: s.color }">{{ s.value }}</p>
              <p class="text-xs text-ink-soft mt-0.5">{{ s.label }}</p>
            </div>
          </div>
          <RouterLink to="/jobs/applications" class="lp-btn-outline w-full mt-4">打开投递看板</RouterLink>
        </div>

        <!-- 快速入口 -->
        <div class="lp-card p-6">
          <h2 class="lp-section-title mb-4">快速入口</h2>
          <div class="grid grid-cols-2 gap-3">
            <RouterLink v-for="q in quick" :key="q.to" :to="q.to" class="flex flex-col items-center gap-2 p-4 rounded-card bg-surface-2 hover:bg-primary-soft hover:text-primary transition-all">
              <span class="material-symbols-outlined" style="font-size:26px">{{ q.icon }}</span>
              <span class="text-xs font-medium">{{ q.label }}</span>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex justify-center py-24"><AiThinking text="加载工作台" /></div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '@/api/client'
import ScoreRing from '@/components/charts/ScoreRing.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import AiThinking from '@/components/common/AiThinking.vue'
import MatchBadge from '@/components/jobs/MatchBadge.vue'

const data = ref(null)
const jobs = ref([])

const greeting = computed(() => {
  const h = new Date().getHours()
  return h < 6 ? '凌晨好' : h < 12 ? '早上好' : h < 14 ? '中午好' : h < 18 ? '下午好' : '晚上好'
})
const daysLeft = computed(() => {
  if (!data.value?.target_start_date) return '—'
  const d = Math.ceil((new Date(data.value.target_start_date) - new Date()) / 86400000)
  return d > 0 ? d : 0
})
const stats = computed(() => {
  const s = data.value.application_stats
  return [
    { key: 'applied', label: '已投递', value: s.applied, color: 'rgb(var(--c-primary))' },
    { key: 'interview', label: '面试中', value: s.interview, color: 'rgb(var(--c-accent))' },
    { key: 'offer', label: '已 Offer', value: s.offer, color: 'rgb(var(--c-success))' },
  ]
})
const quick = [
  { to: '/resume/list', label: '简历优化', icon: 'edit_document' },
  { to: '/interview/setup', label: '模拟面试', icon: 'forum' },
  { to: '/jobs/list', label: '职位搜索', icon: 'search' },
  { to: '/company/list', label: '公司查询', icon: 'apartment' },
]

function ratingText(v) { return v >= 80 ? '优秀' : v >= 60 ? '良好' : v >= 30 ? '进行中' : '待开始' }
function salaryText(j) {
  if (!j.salary_min) return '面议'
  return `${Math.round(j.salary_min / 1000)}-${Math.round(j.salary_max / 1000)}K`
}
async function toggleTask(t) {
  t.is_completed = !t.is_completed
  await api.put(`/plan/tasks/${t.id}`, { is_completed: t.is_completed })
}

onMounted(async () => {
  data.value = await api.get('/dashboard')
  jobs.value = await api.get('/jobs/recommended')
})
</script>
