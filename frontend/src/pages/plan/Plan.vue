<template>
  <div>
    <PageHeader title="求职规划" subtitle="能力评估 · 时间线 · 每日任务 · 学习路径" />

    <!-- Tab -->
    <div class="flex gap-1 mb-5 bg-surface-2 p-1 rounded-pill w-fit">
      <button v-for="t in tabs" :key="t.key" class="px-4 py-1.5 rounded-pill text-sm font-medium transition-all" :class="tab === t.key ? 'bg-surface text-primary shadow-card' : 'text-ink-soft'" @click="tab = t.key">{{ t.label }}</button>
    </div>

    <!-- 能力评估 -->
    <div v-show="tab === 'assessment'" class="grid lg:grid-cols-2 gap-5">
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">能力自评（1-5 分）</h3>
        <div v-for="s in skills" :key="s.name" class="mb-3">
          <div class="flex justify-between text-sm mb-1"><span class="text-ink">{{ s.name }}</span><span class="text-ink-soft">{{ s.self_score }} / 5</span></div>
          <input type="range" min="1" max="5" v-model.number="s.self_score" class="w-full accent-[rgb(var(--c-primary))]" />
        </div>
        <button class="lp-btn-primary w-full mt-3" :disabled="assessing" @click="runAssess"><span class="material-symbols-outlined" style="font-size:18px">auto_awesome</span>{{ assessing ? '评估中…' : 'AI 辅助评估 + 差距分析' }}</button>
      </div>
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">能力画像 vs 目标</h3>
        <div v-if="assessment" class="flex justify-center">
          <RadarChart
            :labels="assessment.radar_chart_data.radar.map(r => r.name)"
            :series="[
              { values: assessment.radar_chart_data.radar.map(r => r.target), color: 'rgb(var(--c-border) / 0.3)', stroke: 'rgb(var(--c-ink-soft))' },
              { values: assessment.radar_chart_data.radar.map(r => r.ai), color: 'rgb(var(--c-primary) / 0.2)', stroke: 'rgb(var(--c-primary))' },
            ]"
            :max="5" :size="280"
          />
        </div>
        <EmptyState v-else icon="radar" title="完成自评后生成雷达图" />
        <div v-if="assessment?.gap_analysis?.length" class="mt-4 space-y-2">
          <p class="text-sm font-semibold text-ink">技能差距</p>
          <div v-for="(g, i) in assessment.gap_analysis" :key="i" class="flex items-center gap-2 text-sm p-2 rounded-btn bg-surface-2">
            <span class="lp-tag" :class="g.level === 'critical' ? 'bg-danger/12 text-danger' : 'bg-warning/15 text-warning'">{{ g.level === 'critical' ? '关键差距' : '加分项' }}</span>
            <span class="text-ink-soft">{{ g.suggestion }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 时间线 -->
    <div v-show="tab === 'timeline'" class="lp-card p-6">
      <div class="flex items-center justify-between mb-5">
        <h3 class="lp-section-title">求职时间线（倒推式）</h3>
        <div class="flex items-center gap-2">
          <input type="date" v-model="targetDate" class="lp-input !w-44" />
          <button class="lp-btn-outline !py-1.5 text-sm" @click="saveTarget">设定目标入职日</button>
        </div>
      </div>
      <div class="relative pl-8">
        <div class="absolute left-3 top-2 bottom-2 w-0.5 bg-border"></div>
        <div v-for="(p, i) in plan?.timeline || []" :key="i" class="relative mb-6">
          <div class="absolute -left-[22px] w-5 h-5 rounded-full bg-primary border-4 border-bg"></div>
          <div class="lp-card p-4">
            <div class="flex items-center justify-between">
              <h4 class="font-display font-bold text-ink">{{ p.phase }}</h4>
              <span class="text-xs text-ink-soft">{{ phaseDate(p.weeks_before) }}</span>
            </div>
            <p class="text-sm text-ink-soft mt-1">{{ p.desc }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 每日任务 -->
    <div v-show="tab === 'tasks'" class="grid lg:grid-cols-3 gap-5">
      <div class="lg:col-span-2 lp-card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="lp-section-title">今日任务</h3>
          <span class="text-sm text-ink-soft">{{ doneTasks }}/{{ tasks.length }} 已完成</span>
        </div>
        <div class="space-y-2">
          <div v-for="t in tasks" :key="t.id" class="flex items-center gap-3 p-3 rounded-btn hover:bg-surface-2">
            <input type="checkbox" :checked="t.is_completed" class="w-5 h-5 accent-[rgb(var(--c-primary))]" @change="toggleTask(t)" />
            <span class="flex-1 text-sm" :class="t.is_completed ? 'line-through text-ink-soft/60' : 'text-ink'">{{ t.title }}</span>
            <span class="lp-tag bg-surface-2 text-ink-soft text-xs">{{ taskTypeLabel[t.task_type] || '其他' }}</span>
            <button class="text-ink-soft/50 hover:text-danger" @click="delTask(t)"><span class="material-symbols-outlined" style="font-size:18px">delete</span></button>
          </div>
        </div>
        <div class="flex gap-2 mt-4">
          <input v-model="newTask" class="lp-input" placeholder="添加新任务…" @keyup.enter="addTask" />
          <button class="lp-btn-primary" @click="addTask">添加</button>
        </div>
      </div>
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">进度看板</h3>
        <ScoreRing :value="plan?.current_progress || 0" :size="130" :stroke="10" label="整体进度" class="mx-auto block" />
        <div class="mt-5 space-y-3">
          <ProgressBar label="简历" :value="80" color="success" />
          <ProgressBar label="技能" :value="plan?.current_progress || 60" color="primary" />
          <ProgressBar label="面试练习" :value="40" color="warning" />
        </div>
      </div>
    </div>

    <!-- 学习路径 -->
    <div v-show="tab === 'learning'" class="grid sm:grid-cols-2 gap-4">
      <div v-for="lp in learning" :key="lp.id" class="lp-card p-5">
        <div class="flex items-center justify-between mb-2">
          <h4 class="font-display font-bold text-ink">{{ lp.skill_name }}</h4>
          <span class="lp-tag bg-primary-soft text-primary">{{ lp.completed_hours }}/{{ lp.estimated_hours }}h</span>
        </div>
        <ProgressBar :value="lp.completed_hours" :max="lp.estimated_hours" :show-value="false" suffix="" class="mb-3" />
        <div class="space-y-1.5">
          <div v-for="(r, i) in lp.resources" :key="i" class="flex items-center gap-2 text-sm text-ink-soft">
            <span class="material-symbols-outlined text-primary" style="font-size:16px">{{ resIcon[r.type] || 'link' }}</span>{{ r.title }}
          </div>
        </div>
      </div>
      <EmptyState v-if="!learning.length" icon="school" title="暂无学习路径" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import RadarChart from '@/components/charts/RadarChart.vue'
import ScoreRing from '@/components/charts/ScoreRing.vue'
import ProgressBar from '@/components/charts/ProgressBar.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const tabs = [
  { key: 'assessment', label: '能力评估' }, { key: 'timeline', label: '时间线' },
  { key: 'tasks', label: '每日任务' }, { key: 'learning', label: '学习路径' },
]
const tab = ref('assessment')
const plan = ref(null)
const tasks = ref([])
const learning = ref([])
const assessment = ref(null)
const assessing = ref(false)
const newTask = ref('')
const targetDate = ref('')
const skills = ref([
  { name: '编程能力', category: 'hard', self_score: 4, target_score: 5 },
  { name: '系统设计', category: 'hard', self_score: 3, target_score: 5 },
  { name: '算法', category: 'hard', self_score: 3, target_score: 4 },
  { name: '沟通表达', category: 'soft', self_score: 4, target_score: 5 },
  { name: '团队协作', category: 'soft', self_score: 4, target_score: 5 },
  { name: '行业知识', category: 'domain', self_score: 3, target_score: 4 },
])
const taskTypeLabel = { apply: '投递', study: '学习', practice: '练习', interview: '面试', other: '其他' }
const resIcon = { course: 'play_circle', book: 'menu_book', project: 'code', cert: 'verified' }
const doneTasks = computed(() => tasks.value.filter((t) => t.is_completed).length)

function phaseDate(weeks) {
  if (!plan.value?.target_start_date) return ''
  const d = new Date(plan.value.target_start_date)
  d.setDate(d.getDate() - weeks * 7)
  return d.toISOString().slice(0, 10)
}
async function runAssess() {
  assessing.value = true
  try {
    assessment.value = await api.post('/plan/assessment', { skills: skills.value, assessment_type: 'ai' })
  } finally { assessing.value = false }
}
async function saveTarget() {
  if (!targetDate.value) return
  plan.value = await api.put('/plan', { target_start_date: targetDate.value })
}
async function toggleTask(t) { t.is_completed = !t.is_completed; await api.put(`/plan/tasks/${t.id}`, { is_completed: t.is_completed }) }
async function addTask() {
  if (!newTask.value.trim()) return
  await api.post('/plan/tasks', { title: newTask.value, task_type: 'other' })
  newTask.value = ''
  tasks.value = await api.get('/plan/tasks')
}
async function delTask(t) { await api.del(`/plan/tasks/${t.id}`); tasks.value = await api.get('/plan/tasks') }

onMounted(async () => {
  plan.value = await api.get('/plan')
  targetDate.value = plan.value.target_start_date || ''
  tasks.value = await api.get('/plan/tasks')
  learning.value = await api.get('/plan/learning')
  assessment.value = await api.get('/plan/assessment')
})
</script>
