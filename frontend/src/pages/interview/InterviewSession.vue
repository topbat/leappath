<template>
  <div v-if="session" class="max-w-3xl mx-auto">
    <!-- 顶部状态 -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-2">
        <button class="lp-btn-ghost !py-1.5" @click="$router.push('/interview/setup')"><span class="material-symbols-outlined" style="font-size:18px">arrow_back</span>退出</button>
        <span class="lp-tag bg-primary-soft text-primary">{{ typeLabel }} · {{ session.position || '通用' }}</span>
      </div>
      <div class="flex items-center gap-3 text-sm text-ink-soft">
        <span class="flex items-center gap-1"><span class="material-symbols-outlined" style="font-size:18px">timer</span>{{ timer }}</span>
        <span class="flex items-center gap-1"><span class="material-symbols-outlined" style="font-size:18px">quiz</span>{{ answered }}/{{ session.total_questions }}</span>
      </div>
    </div>

    <!-- 进度 -->
    <ProgressBar :value="answered" :max="session.total_questions" :show-value="false" suffix="" class="mb-4" />

    <!-- 对话区 -->
    <div ref="scrollArea" class="lp-card p-5 space-y-4 mb-4 min-h-[50vh] max-h-[60vh] overflow-y-auto">
      <div v-for="m in messages" :key="m.id" class="lp-fade">
        <!-- AI -->
        <div v-if="m.role === 'interviewer'" class="flex gap-3">
          <div class="w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center shrink-0"><span class="material-symbols-outlined ms-fill" style="font-size:20px">smart_toy</span></div>
          <div class="flex-1">
            <div class="rounded-card rounded-tl-sm bg-surface-2 p-3.5 text-ink">{{ m.content }}</div>
          </div>
        </div>
        <!-- 用户 -->
        <div v-else-if="m.role === 'user'" class="flex gap-3 flex-row-reverse">
          <div class="w-9 h-9 rounded-full bg-accent text-white flex items-center justify-center shrink-0"><span class="material-symbols-outlined" style="font-size:20px">person</span></div>
          <div class="flex-1 max-w-[80%]">
            <div class="rounded-card rounded-tr-sm bg-primary text-on-primary p-3.5 ml-auto w-fit">{{ m.content }}</div>
            <!-- 即时反馈 -->
            <div v-if="m.feedback" class="mt-2 rounded-card border border-border p-3">
              <div class="flex flex-wrap gap-2 mb-2">
                <span v-for="(t, i) in m.feedback.tags" :key="i" class="lp-tag text-xs" :class="tagCls(t.type)">{{ tagIcon(t.type) }} {{ t.text }}</span>
              </div>
              <p class="text-sm text-ink-soft">💡 {{ m.feedback.suggestion }}</p>
            </div>
          </div>
        </div>
        <!-- 系统 -->
        <div v-else class="text-center"><span class="text-sm text-ink-soft">{{ m.content }}</span></div>
      </div>
      <div v-if="thinking" class="flex gap-3"><div class="w-9 h-9 rounded-full bg-primary/20"></div><AiThinking text="面试官思考中" /></div>
    </div>

    <!-- 输入区 / 结束 -->
    <div v-if="!finished" class="lp-card p-3">
      <textarea v-model="draft" rows="2" class="w-full bg-transparent outline-none resize-none px-2 py-1 text-ink" placeholder="输入你的回答…（支持文字 / 语音）" @keydown.ctrl.enter="send"></textarea>
      <div class="flex items-center justify-between mt-1">
        <div class="flex gap-1">
          <button class="w-9 h-9 rounded-full hover:bg-surface-2 text-ink-soft flex items-center justify-center" title="语音输入（演示）" @click="voiceDemo"><span class="material-symbols-outlined" style="font-size:20px">mic</span></button>
        </div>
        <div class="flex gap-2">
          <button class="lp-btn-outline !py-1.5 text-sm" @click="finish">提前结束</button>
          <button class="lp-btn-primary !py-1.5" :disabled="!draft.trim() || thinking" @click="send"><span class="material-symbols-outlined" style="font-size:18px">send</span>发送</button>
        </div>
      </div>
    </div>
    <div v-else class="lp-card p-5 text-center">
      <p class="text-ink-soft mb-3">面试已完成！</p>
      <button class="lp-btn-primary" @click="goReport"><span class="material-symbols-outlined" style="font-size:18px">assignment</span>查看面试报告</button>
    </div>
  </div>
  <div v-else class="flex justify-center py-24"><AiThinking text="加载面试" /></div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/client'
import ProgressBar from '@/components/charts/ProgressBar.vue'
import AiThinking from '@/components/common/AiThinking.vue'

const route = useRoute()
const router = useRouter()
const id = route.params.id
const session = ref(null)
const messages = ref([])
const draft = ref('')
const thinking = ref(false)
const finished = ref(false)
const scrollArea = ref(null)
const seconds = ref(0)
let timerId = null

const labels = { technical: '技术面', behavioral: '行为面', hr: 'HR 面', case: '案例面' }
const typeLabel = computed(() => labels[session.value?.interview_type] || '面试')
const answered = computed(() => messages.value.filter((m) => m.role === 'user').length)
const timer = computed(() => `${String(Math.floor(seconds.value / 60)).padStart(2, '0')}:${String(seconds.value % 60).padStart(2, '0')}`)

function tagCls(t) { return { good: 'bg-success/15 text-success', warn: 'bg-warning/15 text-warning', tip: 'bg-primary-soft text-primary' }[t] }
function tagIcon(t) { return { good: '✅', warn: '⚠️', tip: '💡' }[t] }

async function scrollDown() { await nextTick(); if (scrollArea.value) scrollArea.value.scrollTop = scrollArea.value.scrollHeight }

async function load() {
  session.value = await api.get(`/interviews/sessions/${id}`)
  messages.value = session.value.messages || []
  if (session.value.status === 'completed') finished.value = true
  scrollDown()
}
async function send() {
  if (!draft.value.trim()) return
  const content = draft.value
  draft.value = ''
  thinking.value = true
  try {
    const res = await api.post(`/interviews/sessions/${id}/answer`, { content })
    messages.value.push(...res.messages)
    if (res.status === 'completed') { finished.value = true; await finish(false) }
  } finally {
    thinking.value = false
    scrollDown()
  }
}
async function finish(confirmFirst = true) {
  if (confirmFirst && !confirm('确定要结束面试并生成报告吗？')) return
  thinking.value = true
  try {
    await api.post(`/interviews/sessions/${id}/finish`)
    finished.value = true
  } finally { thinking.value = false }
}
function goReport() { router.push(`/interview/report/${id}`) }
function voiceDemo() { draft.value += (draft.value ? ' ' : '') + '（语音转写示例）我在项目中通过引入缓存把接口 QPS 从 1500 提升到 4200。' }

onMounted(() => { load(); timerId = setInterval(() => seconds.value++, 1000) })
onUnmounted(() => clearInterval(timerId))
</script>
