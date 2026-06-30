<template>
  <div>
    <PageHeader title="面试记录" subtitle="历次模拟面试与报告" back />
    <div v-if="list.length" class="space-y-3">
      <div v-for="s in list" :key="s.id" class="lp-card p-4 flex items-center gap-4">
        <div class="w-11 h-11 rounded-btn bg-primary-soft text-primary flex items-center justify-center"><span class="material-symbols-outlined" style="font-size:24px">forum</span></div>
        <div class="flex-1 min-w-0">
          <p class="font-display font-bold text-ink">{{ labels[s.interview_type] || '面试' }} · {{ s.position || '通用岗位' }}</p>
          <p class="text-sm text-ink-soft">{{ s.created_at?.slice(0, 16).replace('T', ' ') }} · {{ statusLabel[s.status] }}</p>
        </div>
        <RouterLink v-if="s.status === 'completed'" :to="`/interview/report/${s.id}`" class="lp-btn-outline !py-1.5 text-sm">查看报告</RouterLink>
        <RouterLink v-else :to="`/interview/session/${s.id}`" class="lp-btn-primary !py-1.5 text-sm">继续</RouterLink>
      </div>
    </div>
    <div v-else-if="loaded" class="lp-card"><EmptyState icon="forum" title="还没有面试记录"><RouterLink to="/interview/setup" class="lp-btn-primary mt-4">开始第一次模拟面试</RouterLink></EmptyState></div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import EmptyState from '@/components/common/EmptyState.vue'

const list = ref([])
const loaded = ref(false)
const labels = { technical: '技术面', behavioral: '行为面', hr: 'HR 面', case: '案例面' }
const statusLabel = { in_progress: '进行中', completed: '已完成', abandoned: '已放弃' }
onMounted(async () => { list.value = await api.get('/interviews/sessions'); loaded.value = true })
</script>
