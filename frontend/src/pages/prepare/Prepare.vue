<template>
  <div>
    <PageHeader title="求职准备" subtitle="题库练习 · AI 批改 · 薪资谈判 · Offer 评估" />

    <div class="flex gap-1 mb-5 bg-surface-2 p-1 rounded-pill w-fit overflow-x-auto">
      <button v-for="t in tabs" :key="t.key" class="px-4 py-1.5 rounded-pill text-sm font-medium whitespace-nowrap transition-all" :class="tab === t.key ? 'bg-surface text-primary shadow-card' : 'text-ink-soft'" @click="tab = t.key">{{ t.label }}</button>
    </div>

    <!-- 题库 -->
    <div v-show="tab === 'questions'" class="grid lg:grid-cols-3 gap-5">
      <div class="lp-card p-5 h-fit">
        <h3 class="lp-section-title mb-3">分类</h3>
        <div class="space-y-1">
          <button v-for="c in catList" :key="c.key" class="w-full text-left px-3 py-2 rounded-btn text-sm" :class="cat === c.key ? 'bg-primary-soft text-primary font-semibold' : 'text-ink-soft hover:bg-surface-2'" @click="cat = c.key; loadQuestions()">{{ c.label }}</button>
        </div>
      </div>
      <div class="lg:col-span-2 space-y-3">
        <div v-for="q in questions" :key="q.id" class="lp-card p-5">
          <div class="flex items-start justify-between mb-2">
            <h4 class="font-display font-bold text-ink flex-1">{{ q.question }}</h4>
            <span class="lp-tag shrink-0" :class="diffCls[q.difficulty]">{{ diffLabel[q.difficulty] }}</span>
          </div>
          <div class="flex flex-wrap gap-1.5 mb-3"><span v-for="t in q.tags || []" :key="t" class="lp-tag bg-surface-2 text-ink-soft text-xs">{{ t }}</span></div>
          <button class="text-sm text-primary font-semibold" @click="q._open = !q._open">{{ q._open ? '收起作答' : '在线作答 / 看答案' }}</button>
          <div v-if="q._open" class="mt-3 space-y-3">
            <textarea v-model="q._answer" rows="3" class="lp-input" placeholder="输入你的回答，AI 将批改…"></textarea>
            <div class="flex gap-2">
              <button class="lp-btn-primary !py-1.5 text-sm" :disabled="q._loading" @click="submitPractice(q)">{{ q._loading ? '批改中…' : 'AI 批改' }}</button>
              <button class="lp-btn-outline !py-1.5 text-sm" @click="q._showAnswer = !q._showAnswer">参考答案</button>
            </div>
            <div v-if="q._feedback" class="rounded-card border border-border p-3">
              <div class="flex flex-wrap gap-2 mb-2"><span v-for="(t, i) in q._feedback.ai_feedback.tags" :key="i" class="lp-tag text-xs" :class="tagCls(t.type)">{{ t.text }}</span></div>
              <p class="text-sm text-ink-soft">💡 {{ q._feedback.ai_feedback.suggestion }}</p>
            </div>
            <div v-if="q._showAnswer" class="rounded-card bg-primary-soft p-3 text-sm text-ink">
              <p class="font-semibold text-primary mb-1">参考答案</p>{{ q.answer }}
              <ul class="mt-2 list-disc list-inside text-ink-soft"><li v-for="(t, i) in q.answer_tips || []" :key="i">{{ t }}</li></ul>
            </div>
          </div>
        </div>
        <EmptyState v-if="!questions.length" icon="quiz" title="该分类暂无题目" />
      </div>
    </div>

    <!-- 笔试练习 -->
    <div v-show="tab === 'exam'" class="lp-card p-6">
      <h3 class="lp-section-title mb-3">笔试练习</h3>
      <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <div v-for="e in examTypes" :key="e.label" class="rounded-card border border-border p-4 hover:border-primary transition-all cursor-pointer" @click="alert(`进入「${e.label}」限时练习环境（演示）`)">
          <span class="material-symbols-outlined text-primary" style="font-size:28px">{{ e.icon }}</span>
          <p class="font-display font-bold text-ink mt-2">{{ e.label }}</p>
          <p class="text-sm text-ink-soft">{{ e.desc }}</p>
        </div>
      </div>
    </div>

    <!-- 薪资谈判 -->
    <div v-show="tab === 'salary'" class="grid lg:grid-cols-2 gap-5">
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">谈判模拟与建议</h3>
        <div class="grid grid-cols-2 gap-3 mb-3">
          <input v-model.number="negoForm.base_offer" type="number" class="lp-input" placeholder="对方报价 base（月）" />
          <input v-model.number="negoForm.market_avg" type="number" class="lp-input" placeholder="市场均价（月）" />
        </div>
        <button class="lp-btn-primary w-full" :disabled="negoLoading" @click="getAdvice">{{ negoLoading ? '生成中…' : 'AI 生成谈判策略' }}</button>
      </div>
      <div class="lp-card p-6">
        <div v-if="advice">
          <h3 class="lp-section-title mb-3">话术与策略</h3>
          <p class="text-sm font-semibold text-ink mb-1">📋 标准话术</p>
          <div v-for="(s, i) in advice.scripts" :key="i" class="text-sm text-ink-soft p-2.5 rounded-btn bg-surface-2 mb-2">{{ s }}</div>
          <p class="text-sm font-semibold text-ink mb-1 mt-3">🎯 策略</p>
          <p class="text-sm text-ink-soft">{{ advice.strategy }}</p>
          <p class="text-sm font-semibold text-danger mb-1 mt-3">⚠️ 避坑</p>
          <ul class="text-sm text-ink-soft list-disc list-inside"><li v-for="(p, i) in advice.pitfalls" :key="i">{{ p }}</li></ul>
        </div>
        <EmptyState v-else icon="payments" title="填写信息后生成谈判建议" />
      </div>
    </div>

    <!-- Offer 评估 -->
    <div v-show="tab === 'offer'" class="grid lg:grid-cols-2 gap-5">
      <div class="lp-card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="lp-section-title">我的 Offer</h3>
          <button class="lp-btn-outline !py-1.5 text-sm" @click="showOfferForm = !showOfferForm">+ 添加</button>
        </div>
        <div v-if="showOfferForm" class="space-y-2 mb-4 p-3 rounded-card bg-surface-2">
          <div class="grid grid-cols-2 gap-2">
            <input v-model="offerForm.company_name" class="lp-input" placeholder="公司" />
            <input v-model="offerForm.position_title" class="lp-input" placeholder="职位" />
            <input v-model.number="offerForm.base_salary" type="number" class="lp-input" placeholder="月 base" />
            <input v-model.number="offerForm.bonus_months" type="number" class="lp-input" placeholder="年终(月)" />
          </div>
          <button class="lp-btn-primary w-full !py-1.5 text-sm" @click="addOffer">保存 Offer</button>
        </div>
        <div v-for="o in offers" :key="o.id" class="flex items-center justify-between p-3 rounded-btn hover:bg-surface-2">
          <div><p class="font-medium text-ink text-sm">{{ o.company_name }} · {{ o.position_title }}</p><p class="text-xs text-ink-soft">总包约 {{ Math.round((o.total_annual||0)/10000) }}w · {{ o.work_city }}</p></div>
          <button class="text-ink-soft/50 hover:text-danger" @click="delOffer(o)"><span class="material-symbols-outlined" style="font-size:18px">delete</span></button>
        </div>
      </div>
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">多 Offer 对比</h3>
        <button class="lp-btn-primary w-full mb-4" @click="compareOffers">生成雷达对比 + 推荐指数</button>
        <div v-if="compared.length">
          <RadarChart
            :labels="Object.keys(compared[0].radar)"
            :series="compared.map((o, i) => ({ values: Object.values(o.radar), color: i === 0 ? 'rgb(var(--c-primary) / 0.2)' : 'rgb(var(--c-accent) / 0.15)', stroke: i === 0 ? 'rgb(var(--c-primary))' : 'rgb(var(--c-accent))' }))"
            :max="5" :size="260" class="mx-auto block"
          />
          <div class="mt-4 space-y-2">
            <div v-for="(o, i) in compared" :key="o.id" class="flex items-center justify-between p-2.5 rounded-btn" :class="i === 0 ? 'bg-success/10' : 'bg-surface-2'">
              <span class="text-sm text-ink">{{ i === 0 ? '🏆 ' : '' }}{{ o.company_name }}</span>
              <span class="font-display font-bold" :style="{ color: i === 0 ? 'rgb(var(--c-success))' : 'rgb(var(--c-ink-soft))' }">推荐指数 {{ o.recommend_index }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import RadarChart from '@/components/charts/RadarChart.vue'

const tabs = [
  { key: 'questions', label: '常见/技术题库' }, { key: 'exam', label: '笔试练习' },
  { key: 'salary', label: '薪资谈判' }, { key: 'offer', label: 'Offer 评估' },
]
const tab = ref('questions')
const catList = [
  { key: '', label: '全部' }, { key: 'common', label: '常见面试题' },
  { key: 'technical', label: '技术题库' }, { key: 'aptitude', label: '行测/笔试' },
]
const cat = ref('')
const questions = ref([])
const diffLabel = { easy: '初级', medium: '中级', hard: '高级' }
const diffCls = { easy: 'bg-success/15 text-success', medium: 'bg-primary-soft text-primary', hard: 'bg-warning/15 text-warning' }
const examTypes = [
  { label: '行测', icon: 'psychology_alt', desc: '逻辑·数量·言语' },
  { label: '性格测试', icon: 'mood', desc: 'MBTI·职业倾向' },
  { label: '技术笔试', icon: 'terminal', desc: '在线编程环境' },
  { label: '限时模式', icon: 'timer', desc: '真实时间压力' },
]
const negoForm = reactive({ base_offer: 30000, market_avg: 35000 })
const advice = ref(null)
const negoLoading = ref(false)
const offers = ref([])
const compared = ref([])
const showOfferForm = ref(false)
const offerForm = reactive({ company_name: '', position_title: '', base_salary: 30000, bonus_months: 4 })

function tagCls(t) { return { good: 'bg-success/15 text-success', warn: 'bg-warning/15 text-warning', tip: 'bg-primary-soft text-primary' }[t] }
async function loadQuestions() {
  const p = new URLSearchParams()
  if (cat.value) p.set('category', cat.value)
  const list = await api.get(`/prepare/questions?${p}`)
  questions.value = list.map((q) => ({ ...q, _open: false, _answer: '', _feedback: null, _showAnswer: false, _loading: false }))
}
async function submitPractice(q) {
  q._loading = true
  try { q._feedback = await api.post('/prepare/practice', { question_id: q.id, question_text: q.question, user_answer: q._answer }) }
  finally { q._loading = false }
}
async function getAdvice() { negoLoading.value = true; try { advice.value = await api.post('/prepare/negotiation', { ...negoForm }) } finally { negoLoading.value = false } }
async function loadOffers() { offers.value = await api.get('/prepare/offers') }
async function addOffer() { await api.post('/prepare/offers', { ...offerForm, evaluation: { salary: 4, growth: 4, wlb: 3, location: 4, stability: 4, team: 4 } }); showOfferForm.value = false; await loadOffers() }
async function delOffer(o) { await api.del(`/prepare/offers/${o.id}`); await loadOffers() }
async function compareOffers() { compared.value = await api.post('/prepare/offers/compare', {}) }

onMounted(() => { loadQuestions(); loadOffers() })
</script>
