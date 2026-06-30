<template>
  <div>
    <PageHeader title="简历优化" subtitle="逐条 STAR 化润色，量化成果，匹配目标行业关键词" back>
      <template #actions>
        <select v-model="style" class="lp-input !w-36">
          <option value="professional">专业严谨</option>
          <option value="concise">简洁有力</option>
          <option value="data">数据驱动</option>
        </select>
      </template>
    </PageHeader>

    <!-- 定向优化（JD） -->
    <div class="lp-card p-5 mb-5">
      <div class="flex items-center gap-2 mb-3"><span class="material-symbols-outlined text-primary" style="font-size:20px">target</span><h3 class="font-display font-bold text-ink">定向优化（粘贴目标 JD）</h3></div>
      <textarea v-model="jd" rows="3" class="lp-input" placeholder="粘贴目标职位 JD，AI 将据此提取关键词并给出匹配度…"></textarea>
      <div class="flex items-center gap-3 mt-3">
        <button class="lp-btn-primary" :disabled="matching || !jd" @click="runMatch">{{ matching ? '分析中…' : '分析匹配度' }}</button>
        <template v-if="matchResult">
          <MatchBadge :value="matchResult.overall" />
          <span class="text-sm text-ink-soft">缺失关键词：</span>
          <span v-for="k in matchResult.missing.slice(0,5)" :key="k" class="lp-chip !bg-danger/10 !text-danger">{{ k }}</span>
        </template>
      </div>
    </div>

    <!-- 逐条润色 -->
    <div class="lp-card p-5 mb-5">
      <div class="flex items-center justify-between mb-3">
        <h3 class="font-display font-bold text-ink">逐条润色</h3>
        <span class="text-sm text-ink-soft">已处理 {{ doneCount }}/{{ originals.length }} 项</span>
      </div>
      <ProgressBar :value="doneCount" :max="originals.length || 1" :show-value="false" suffix="" class="mb-4" />

      <div v-for="(o, i) in originals" :key="i" class="rounded-card border border-border p-4 mb-3" :class="results[i]?.accepted ? 'border-success/40 bg-success/5' : ''">
        <div class="flex items-center gap-2 mb-2 text-sm text-ink-soft"><span class="material-symbols-outlined" style="font-size:16px">edit_note</span>原文</div>
        <p class="text-ink mb-3">{{ o }}</p>
        <div v-if="results[i]">
          <div class="flex items-center gap-2 mb-2 text-sm text-primary"><span class="material-symbols-outlined ms-fill" style="font-size:16px">auto_awesome</span>AI 建议（{{ results[i].style_label }}）</div>
          <textarea v-model="results[i].polished" rows="3" class="lp-input mb-2"></textarea>
          <p v-if="results[i].needs_confirm?.length" class="text-xs text-warning mb-2">⚠️ 待确认量化值：{{ results[i].needs_confirm.join('、') }}（请按真实情况核对）</p>
          <div class="flex gap-2">
            <button class="lp-btn-primary text-sm !py-1.5" @click="results[i].accepted = true"><span class="material-symbols-outlined" style="font-size:16px">check</span>采纳</button>
            <button class="lp-btn-outline text-sm !py-1.5" @click="repolish(i)">重新润色</button>
            <button class="lp-btn-ghost text-sm !py-1.5 text-danger" @click="results[i] = null">拒绝</button>
          </div>
        </div>
        <button v-else class="lp-btn-outline text-sm !py-1.5" :disabled="loadingIdx === i" @click="polish(i)">
          <span class="material-symbols-outlined" style="font-size:16px">auto_awesome</span>{{ loadingIdx === i ? '润色中…' : 'AI 润色这条' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import ProgressBar from '@/components/charts/ProgressBar.vue'
import MatchBadge from '@/components/jobs/MatchBadge.vue'

const route = useRoute()
const id = route.params.id
const style = ref('professional')
const jd = ref('')
const matching = ref(false)
const matchResult = ref(null)
const originals = ref([])
const results = ref([])
const loadingIdx = ref(-1)

const doneCount = computed(() => results.value.filter((r) => r && r.accepted).length)

async function load() {
  const r = await api.get(`/resumes/${id}`)
  const exp = (r.sections || []).find((s) => s.section_type === 'experience')
  const proj = (r.sections || []).find((s) => s.section_type === 'project')
  const list = []
  ;(exp?.content?.items || []).forEach((e) => e.desc && list.push(e.desc))
  ;(proj?.content?.items || []).forEach((e) => e.desc && list.push(e.desc))
  if (!list.length) list.push('负责公司后端 API 开发，提升了系统性能')
  originals.value = list
  results.value = new Array(list.length).fill(null)
}
async function polish(i) {
  loadingIdx.value = i
  try {
    results.value[i] = await api.post(`/resumes/${id}/polish`, { text: originals.value[i], style: style.value, target: jd.value })
  } finally {
    loadingIdx.value = -1
  }
}
async function repolish(i) { await polish(i) }
async function runMatch() {
  matching.value = true
  try {
    matchResult.value = await api.post(`/resumes/${id}/match`, { jd_text: jd.value })
  } finally {
    matching.value = false
  }
}
onMounted(load)
</script>
