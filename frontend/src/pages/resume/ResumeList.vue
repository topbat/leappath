<template>
  <div>
    <PageHeader title="简历中心" subtitle="导入 · 创建 · 润色 · 评分 · 多版本管理">
      <template #actions>
        <button class="lp-btn-primary" @click="createResume">
          <span class="material-symbols-outlined" style="font-size:20px">add</span>创建新简历
        </button>
      </template>
    </PageHeader>

    <div v-if="resumes.length" class="space-y-4">
      <div v-for="r in resumes" :key="r.id" class="lp-card p-5 hover:shadow-lift transition-all">
        <div class="flex items-start gap-4">
          <div class="w-12 h-16 rounded-btn bg-primary-soft text-primary flex items-center justify-center shrink-0">
            <span class="material-symbols-outlined" style="font-size:28px">article</span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 flex-wrap">
              <h3 class="font-display font-bold text-ink truncate">{{ r.title }}</h3>
              <span v-if="r.is_default" class="lp-tag bg-primary-soft text-primary">默认</span>
              <span class="lp-tag" :class="r.status === 'complete' ? 'bg-success/15 text-success' : 'bg-surface-2 text-ink-soft'">{{ r.status === 'complete' ? '已完善' : '草稿' }}</span>
            </div>
            <p class="text-sm text-ink-soft mt-1">
              更新于 {{ fmtDate(r.updated_at) }}
              <span v-if="r.score_total"> · 评分 <b class="text-ink">{{ r.score_total }}</b> 分</span>
            </p>
            <div class="flex flex-wrap gap-2 mt-3">
              <RouterLink :to="`/resume/${r.id}`" class="lp-btn-ghost text-sm !py-1.5"><span class="material-symbols-outlined" style="font-size:18px">edit</span>编辑</RouterLink>
              <RouterLink :to="`/resume/${r.id}/optimize`" class="lp-btn-ghost text-sm !py-1.5 text-primary"><span class="material-symbols-outlined" style="font-size:18px">auto_awesome</span>AI 润色</RouterLink>
              <RouterLink :to="`/resume/${r.id}/score`" class="lp-btn-ghost text-sm !py-1.5"><span class="material-symbols-outlined" style="font-size:18px">grade</span>评分</RouterLink>
              <button class="lp-btn-ghost text-sm !py-1.5" @click="exportResume(r)"><span class="material-symbols-outlined" style="font-size:18px">download</span>导出</button>
              <button v-if="!r.is_default" class="lp-btn-ghost text-sm !py-1.5" @click="setDefault(r)"><span class="material-symbols-outlined" style="font-size:18px">star</span>设为默认</button>
              <button class="lp-btn-ghost text-sm !py-1.5 text-danger ml-auto" @click="removeResume(r)"><span class="material-symbols-outlined" style="font-size:18px">delete</span></button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="loaded" class="lp-card">
      <EmptyState icon="description" title="还没有简历" desc="创建你的第一份简历，开启求职之旅">
        <button class="lp-btn-primary mt-4" @click="createResume">立即创建</button>
      </EmptyState>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const router = useRouter()
const resumes = ref([])
const loaded = ref(false)

async function load() {
  resumes.value = await api.get('/resumes')
  loaded.value = true
}
async function createResume() {
  const r = await api.post('/resumes', { title: '新建简历', is_default: resumes.value.length === 0 })
  router.push(`/resume/${r.id}`)
}
async function setDefault(r) {
  await api.put(`/resumes/${r.id}`, { is_default: true })
  await load()
}
async function removeResume(r) {
  if (!confirm(`确认删除「${r.title}」？`)) return
  await api.del(`/resumes/${r.id}`)
  await load()
}
function exportResume(r) {
  alert(`已生成「${r.title}」的导出文件（演示）。\n支持 PDF / Word / 在线链接，保持模板排版。`)
}
function fmtDate(s) { return s ? s.slice(0, 10) : '—' }

onMounted(load)
</script>
