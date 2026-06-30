<template>
  <div>
    <PageHeader title="公司画像" subtitle="档案 · 薪资 · 面经 · 文化 · 求职难度">
      <template #actions>
        <RouterLink to="/company/compare" class="lp-btn-outline"><span class="material-symbols-outlined" style="font-size:18px">compare</span>公司对比</RouterLink>
      </template>
    </PageHeader>

    <div class="flex flex-wrap items-center gap-2 mb-5">
      <div class="relative">
        <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-ink-soft/60" style="font-size:18px">search</span>
        <input v-model="keyword" class="lp-input !pl-9 !w-56" placeholder="搜索公司" @keyup.enter="load" />
      </div>
      <button v-for="i in industries" :key="i" class="lp-chip" :class="industry === i ? '!bg-primary !text-on-primary' : ''" @click="industry = industry === i ? '' : i; load()">{{ i }}</button>
      <label class="flex items-center gap-2 text-sm text-ink-soft ml-2"><input type="checkbox" v-model="onlySaved" @change="load" class="accent-[rgb(var(--c-primary))]" />仅看收藏</label>
    </div>

    <div v-if="companies.length" class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="c in companies" :key="c.id" class="lp-card p-5 hover:shadow-lift transition-all">
        <div class="flex items-start justify-between mb-3">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 rounded-btn bg-primary-soft text-primary flex items-center justify-center font-bold text-lg">{{ c.name[0] }}</div>
            <div><RouterLink :to="`/company/${c.id}`" class="font-display font-bold text-ink hover:text-primary line-clamp-1">{{ c.short_name || c.name }}</RouterLink><p class="text-sm text-ink-soft">{{ c.industry }}</p></div>
          </div>
          <button @click="toggleSave(c)"><span class="material-symbols-outlined" :class="c.is_saved ? 'ms-fill text-accent' : 'text-ink-soft/50'" style="font-size:22px">{{ c.is_saved ? 'bookmark' : 'bookmark_border' }}</span></button>
        </div>
        <div class="flex flex-wrap gap-1.5 mb-3">
          <span class="lp-tag bg-surface-2 text-ink-soft">{{ c.size_range }}人</span>
          <span class="lp-tag bg-surface-2 text-ink-soft">{{ stageLabel[c.financing_stage] || c.financing_stage }}</span>
          <span class="lp-tag" :class="diffCls[c.difficulty_level]">{{ diffLabel[c.difficulty_level] }}</span>
        </div>
        <RouterLink :to="`/company/${c.id}`" class="lp-btn-outline w-full text-sm !py-1.5">查看详情</RouterLink>
      </div>
    </div>
    <div v-else-if="loaded" class="lp-card"><EmptyState icon="apartment" title="暂无公司" /></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const companies = ref([])
const loaded = ref(false)
const keyword = ref('')
const industry = ref('')
const onlySaved = ref(false)
const industries = ['互联网', '金融科技', '咨询', '快消']
const stageLabel = { angel: '天使轮', A: 'A 轮', B: 'B 轮', C: 'C 轮', D: 'D 轮', listed: '已上市' }
const diffLabel = { low: '难度低', medium: '难度中', high: '难度高', extreme: '难度极高' }
const diffCls = { low: 'bg-success/15 text-success', medium: 'bg-primary-soft text-primary', high: 'bg-warning/15 text-warning', extreme: 'bg-danger/12 text-danger' }

async function load() {
  loaded.value = false
  if (onlySaved.value) {
    companies.value = await api.get('/companies/saved')
  } else {
    const p = new URLSearchParams()
    if (keyword.value) p.set('keyword', keyword.value)
    if (industry.value) p.set('industry', industry.value)
    companies.value = await api.get(`/companies?${p}`)
  }
  loaded.value = true
}
async function toggleSave(c) { const r = await api.post(`/companies/${c.id}/save`); c.is_saved = r.is_saved }
onMounted(load)
</script>
