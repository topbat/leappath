<template>
  <div>
    <PageHeader title="模拟面试" subtitle="AI 面试官 · 动态追问 · 即时反馈 · 综合报告">
      <template #actions>
        <RouterLink to="/interview/history" class="lp-btn-outline"><span class="material-symbols-outlined" style="font-size:18px">history</span>历史记录</RouterLink>
      </template>
    </PageHeader>

    <div class="grid lg:grid-cols-3 gap-5">
      <div class="lg:col-span-2 space-y-5">
        <div class="lp-card p-6">
          <h3 class="lp-section-title mb-4">选择面试类型</h3>
          <div class="grid sm:grid-cols-2 gap-3">
            <button
              v-for="t in types" :key="t.key"
              class="text-left rounded-card border p-4 transition-all"
              :class="form.interview_type === t.key ? 'border-primary bg-primary-soft' : 'border-border hover:border-primary/50'"
              @click="form.interview_type = t.key"
            >
              <div class="flex items-center gap-2 mb-1">
                <span class="material-symbols-outlined text-primary" style="font-size:22px">{{ t.icon }}</span>
                <span class="font-display font-bold text-ink">{{ t.label }}</span>
              </div>
              <p class="text-sm text-ink-soft">{{ t.desc }}</p>
            </button>
          </div>
        </div>

        <div class="lp-card p-6 space-y-4">
          <h3 class="lp-section-title">面试设置</h3>
          <div class="grid sm:grid-cols-2 gap-4">
            <Field label="目标职位"><input v-model="form.position" class="lp-input" placeholder="如 后端开发工程师" /></Field>
            <Field label="目标公司（可选）"><input v-model="form.company_name" class="lp-input" placeholder="如 腾讯" /></Field>
            <Field label="行业方向">
              <select v-model="form.industry" class="lp-input">
                <option v-for="i in industries" :key="i" :value="i">{{ i }}</option>
              </select>
            </Field>
            <Field label="难度">
              <div class="flex gap-2">
                <button v-for="dd in difficulties" :key="dd.key" class="flex-1 py-2 rounded-btn text-sm font-medium transition-all" :class="form.difficulty === dd.key ? 'bg-primary text-on-primary' : 'bg-surface-2 text-ink-soft'" @click="form.difficulty = dd.key">{{ dd.label }}</button>
              </div>
            </Field>
          </div>
          <Field label="题目数量">
            <input v-model.number="form.total_questions" type="range" min="3" max="10" class="w-full accent-[rgb(var(--c-primary))]" />
            <span class="text-sm text-ink-soft">共 {{ form.total_questions }} 题</span>
          </Field>
        </div>
      </div>

      <div class="lp-card p-6 h-fit lg:sticky lg:top-20">
        <div class="flex items-center gap-2 mb-4"><span class="material-symbols-outlined ms-fill text-primary" style="font-size:24px">smart_toy</span><h3 class="font-display font-bold text-ink">即将开始</h3></div>
        <ul class="space-y-2 text-sm text-ink-soft mb-5">
          <li class="flex gap-2"><span class="material-symbols-outlined text-success" style="font-size:18px">check_circle</span>{{ typeLabel }} · {{ diffLabel }}难度</li>
          <li class="flex gap-2"><span class="material-symbols-outlined text-success" style="font-size:18px">check_circle</span>{{ form.position || '通用岗位' }}</li>
          <li class="flex gap-2"><span class="material-symbols-outlined text-success" style="font-size:18px">check_circle</span>{{ form.total_questions }} 道题，支持动态追问</li>
          <li class="flex gap-2"><span class="material-symbols-outlined text-success" style="font-size:18px">check_circle</span>每轮即时反馈 + 结束综合报告</li>
        </ul>
        <button class="lp-btn-primary w-full py-2.5" :disabled="starting" @click="start">
          <span class="material-symbols-outlined" style="font-size:20px">play_arrow</span>{{ starting ? '准备中…' : '开始面试' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import Field from '@/components/resume/Field.vue'

const router = useRouter()
const starting = ref(false)
const types = [
  { key: 'technical', label: '技术面', icon: 'code', desc: '算法、系统设计、项目深挖' },
  { key: 'behavioral', label: '行为面', icon: 'psychology', desc: 'STAR 行为问题、情景题' },
  { key: 'hr', label: 'HR 面', icon: 'diversity_3', desc: '薪资期望、职业规划、文化匹配' },
  { key: 'case', label: '案例面', icon: 'cases', desc: '咨询/产品案例分析' },
]
const industries = ['互联网', '金融', '咨询', '快消', '制造业', '医疗', '教育', '新能源']
const difficulties = [{ key: 'easy', label: '初级' }, { key: 'medium', label: '中级' }, { key: 'hard', label: '高级' }]
const form = reactive({ interview_type: 'technical', position: '后端开发工程师', company_name: '', industry: '互联网', difficulty: 'medium', total_questions: 6 })

const typeLabel = computed(() => types.find((t) => t.key === form.interview_type)?.label)
const diffLabel = computed(() => difficulties.find((d) => d.key === form.difficulty)?.label)

async function start() {
  starting.value = true
  try {
    const s = await api.post('/interviews/sessions', { ...form })
    router.push(`/interview/session/${s.id}`)
  } finally {
    starting.value = false
  }
}
</script>
