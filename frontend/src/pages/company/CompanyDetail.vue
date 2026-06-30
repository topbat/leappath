<template>
  <div v-if="c">
    <PageHeader :title="c.short_name || c.name" back>
      <template #actions>
        <button class="lp-btn-outline" @click="toggleSave"><span class="material-symbols-outlined" :class="c.is_saved ? 'ms-fill text-accent' : ''" style="font-size:18px">{{ c.is_saved ? 'bookmark' : 'bookmark_border' }}</span>{{ c.is_saved ? '已收藏' : '收藏' }}</button>
        <RouterLink to="/company/compare" class="lp-btn-primary">加入对比</RouterLink>
      </template>
    </PageHeader>

    <!-- 概况 -->
    <div class="lp-card p-6 mb-5">
      <div class="flex items-start gap-4">
        <div class="w-16 h-16 rounded-card bg-primary-soft text-primary flex items-center justify-center font-bold text-2xl">{{ c.name[0] }}</div>
        <div class="flex-1">
          <h2 class="font-display text-xl font-extrabold text-ink">{{ c.name }}</h2>
          <div class="flex flex-wrap gap-2 mt-2">
            <span class="lp-chip">{{ c.industry }}</span>
            <span class="lp-chip">{{ c.size_range }}人</span>
            <span class="lp-chip">{{ stageLabel[c.financing_stage] || c.financing_stage }}</span>
            <span class="lp-chip">{{ c.location_city }}</span>
            <span class="lp-tag" :class="diffCls[c.difficulty_level]">求职难度：{{ diffLabel[c.difficulty_level] }}</span>
          </div>
          <p class="text-sm text-ink-soft mt-3">{{ c.description }}</p>
          <div class="flex flex-wrap gap-1.5 mt-3"><span v-for="t in c.tech_stack || []" :key="t" class="lp-tag bg-surface-2 text-ink-soft">{{ t }}</span></div>
        </div>
      </div>
    </div>

    <div class="grid lg:grid-cols-2 gap-5">
      <!-- 薪资 -->
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">薪资水平</h3>
        <div class="space-y-3">
          <div v-for="s in c.salaries" :key="s.id">
            <div class="flex justify-between text-sm mb-1"><span class="text-ink">{{ s.position_name }}</span><span class="font-semibold text-accent">{{ Math.round(s.salary_min/1000) }}K - {{ Math.round(s.salary_max/1000) }}K</span></div>
            <div class="h-2 rounded-pill bg-surface-2 relative overflow-hidden"><div class="absolute h-full rounded-pill bg-primary/30" :style="barStyle(s)"></div></div>
          </div>
        </div>
      </div>

      <!-- 正在招聘 -->
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">正在招聘（{{ c.positions.length }}）</h3>
        <div class="space-y-2">
          <RouterLink v-for="p in c.positions" :key="p.id" :to="`/jobs/${p.id}`" class="flex items-center justify-between p-3 rounded-btn hover:bg-surface-2">
            <div><p class="font-medium text-ink text-sm">{{ p.title }}</p><p class="text-xs text-ink-soft">{{ p.department }} · {{ p.experience_required }}</p></div>
            <span class="text-sm text-accent font-semibold">{{ Math.round(p.salary_min/1000) }}-{{ Math.round(p.salary_max/1000) }}K</span>
          </RouterLink>
          <EmptyState v-if="!c.positions.length" icon="work_off" title="暂无在招职位" />
        </div>
      </div>

      <!-- 面经 -->
      <div class="lp-card p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="lp-section-title">面经聚合（{{ c.review_summary.count }}）</h3>
        </div>
        <div v-if="c.review_summary.hot_questions.length" class="mb-3 p-3 rounded-card bg-primary-soft">
          <p class="text-sm font-semibold text-primary mb-2 flex items-center gap-1"><span class="material-symbols-outlined ms-fill" style="font-size:16px">auto_awesome</span>AI 摘要 · 高频问题</p>
          <div class="flex flex-wrap gap-1.5"><span v-for="(q, i) in c.review_summary.hot_questions" :key="i" class="lp-tag bg-surface text-ink-soft">{{ q }}</span></div>
        </div>
        <div v-for="r in c.reviews" :key="r.id" class="border-t border-border pt-3 mt-3 first:border-0 first:pt-0 first:mt-0">
          <div class="flex items-center gap-2 mb-1">
            <span class="font-medium text-ink text-sm">{{ r.position_name }} · {{ r.interview_round }}</span>
            <span class="text-warning text-xs">{{ '★'.repeat(r.interview_difficulty || 0) }}</span>
            <span class="lp-tag text-xs" :class="r.offer_result === 'offer' ? 'bg-success/15 text-success' : 'bg-surface-2 text-ink-soft'">{{ resultLabel[r.offer_result] || r.offer_result }}</span>
          </div>
          <p class="text-sm text-ink-soft">{{ r.review_content }}</p>
        </div>
      </div>

      <!-- 企业文化 -->
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">企业文化</h3>
        <div class="grid grid-cols-2 gap-2">
          <div v-for="(t, i) in c.culture_tags || []" :key="i" class="flex items-center gap-2 p-2.5 rounded-btn bg-surface-2 text-sm text-ink"><span class="material-symbols-outlined text-primary" style="font-size:18px">check_circle</span>{{ t }}</div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex justify-center py-24"><AiThinking text="加载公司画像" /></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import AiThinking from '@/components/common/AiThinking.vue'

const route = useRoute()
const c = ref(null)
const stageLabel = { angel: '天使轮', A: 'A 轮', B: 'B 轮', C: 'C 轮', D: 'D 轮', listed: '已上市' }
const diffLabel = { low: '低', medium: '中', high: '高', extreme: '极高' }
const diffCls = { low: 'bg-success/15 text-success', medium: 'bg-primary-soft text-primary', high: 'bg-warning/15 text-warning', extreme: 'bg-danger/12 text-danger' }
const resultLabel = { offer: '已 Offer', rejected: '挂', withdrawn: '撤回' }

function barStyle(s) {
  const max = 70000
  return { left: `${(s.salary_min / max) * 100}%`, width: `${((s.salary_max - s.salary_min) / max) * 100}%` }
}
async function toggleSave() { const r = await api.post(`/companies/${c.value.id}/save`); c.value.is_saved = r.is_saved }
onMounted(async () => { c.value = await api.get(`/companies/${route.params.id}`) })
</script>
