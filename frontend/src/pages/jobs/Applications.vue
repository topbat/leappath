<template>
  <div>
    <PageHeader title="投递追踪" subtitle="看板式管理，拖拽卡片即可流转状态">
      <template #actions>
        <button class="lp-btn-primary" @click="showAdd = true"><span class="material-symbols-outlined" style="font-size:18px">add</span>添加投递</button>
      </template>
    </PageHeader>

    <div v-if="board" class="flex gap-4 overflow-x-auto pb-4">
      <div
        v-for="col in board.stages" :key="col.key"
        class="flex-shrink-0 w-72"
        @dragover.prevent
        @drop="onDrop(col.key)"
      >
        <div class="flex items-center gap-2 mb-2 px-1">
          <span class="w-2.5 h-2.5 rounded-full" :style="{ background: stageColor[col.key] }"></span>
          <span class="font-display font-bold text-ink-soft text-sm">{{ col.label }}</span>
          <span class="text-xs text-ink-soft/60">({{ col.items.length }})</span>
        </div>
        <div class="space-y-2.5 min-h-[60vh] rounded-card bg-surface-2/50 p-2.5 border border-border/50">
          <div
            v-for="a in col.items" :key="a.id"
            class="lp-card p-3.5 cursor-grab active:cursor-grabbing hover:shadow-card transition-all"
            :class="col.key === 'offer' || col.key === 'accepted' ? '!border-success/40' : ''"
            draggable="true"
            @dragstart="dragging = a"
          >
            <div class="flex items-start justify-between mb-1">
              <span class="lp-tag bg-primary-soft text-primary text-[10px]">{{ a.position_title }}</span>
              <button class="text-ink-soft/50 hover:text-danger" @click="remove(a)"><span class="material-symbols-outlined" style="font-size:16px">close</span></button>
            </div>
            <h4 class="font-display font-bold text-ink text-sm">{{ a.company_name }}</h4>
            <p v-if="a.salary_label" class="text-sm text-accent font-semibold mt-0.5">{{ a.salary_label }}</p>
            <p v-if="a.applied_date" class="text-xs text-ink-soft mt-1.5 flex items-center gap-1"><span class="material-symbols-outlined" style="font-size:14px">event</span>{{ a.applied_date }}</p>
          </div>
          <p v-if="!col.items.length" class="text-center text-xs text-ink-soft/50 py-6">拖动卡片到此</p>
        </div>
      </div>
    </div>

    <!-- 添加 -->
    <div v-if="showAdd" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showAdd = false">
      <div class="lp-card p-6 w-full max-w-md lp-fade">
        <h3 class="lp-section-title mb-4">添加投递记录</h3>
        <div class="space-y-3">
          <input v-model="form.company_name" class="lp-input" placeholder="公司名" />
          <input v-model="form.position_title" class="lp-input" placeholder="职位名" />
          <input v-model="form.salary_label" class="lp-input" placeholder="薪资（如 25-40K）" />
          <select v-model="form.status" class="lp-input">
            <option v-for="s in board.stages" :key="s.key" :value="s.key">{{ s.label }}</option>
          </select>
        </div>
        <div class="flex justify-end gap-2 mt-4">
          <button class="lp-btn-ghost" @click="showAdd = false">取消</button>
          <button class="lp-btn-primary" @click="add">添加</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'

const board = ref(null)
const dragging = ref(null)
const showAdd = ref(false)
const form = reactive({ company_name: '', position_title: '', salary_label: '', status: 'saved' })
const stageColor = {
  saved: '#94a3b8', applied: 'rgb(var(--c-primary))', screening: '#a855f7',
  interview: 'rgb(var(--c-accent))', offer: 'rgb(var(--c-success))', accepted: '#16a34a', rejected: 'rgb(var(--c-danger))',
}

async function load() { board.value = await api.get('/jobs/applications') }
async function onDrop(stage) {
  if (!dragging.value || dragging.value.status === stage) return
  await api.put(`/jobs/applications/${dragging.value.id}`, { status: stage })
  dragging.value = null
  await load()
}
async function remove(a) {
  if (!confirm(`删除 ${a.company_name} 的投递记录？`)) return
  await api.del(`/jobs/applications/${a.id}`)
  await load()
}
async function add() {
  await api.post('/jobs/applications', { ...form })
  showAdd.value = false
  Object.assign(form, { company_name: '', position_title: '', salary_label: '', status: 'saved' })
  await load()
}
onMounted(load)
</script>
