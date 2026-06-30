<template>
  <div>
    <PageHeader :title="form.title || '编辑简历'" back>
      <template #actions>
        <input v-model="form.title" class="lp-input !w-48" placeholder="简历标题" />
        <button class="lp-btn-outline" @click="save"><span class="material-symbols-outlined" style="font-size:18px">save</span>{{ saving ? '保存中…' : '保存' }}</button>
        <RouterLink v-if="resumeId" :to="`/resume/${resumeId}/score`" class="lp-btn-primary">评分</RouterLink>
      </template>
    </PageHeader>

    <!-- 步骤条 -->
    <div class="flex items-center gap-1 mb-6 overflow-x-auto pb-2">
      <template v-for="(s, i) in steps" :key="s.key">
        <button
          class="flex items-center gap-2 px-3 py-1.5 rounded-pill whitespace-nowrap transition-all"
          :class="i === step ? 'bg-primary text-on-primary' : 'bg-surface-2 text-ink-soft'"
          @click="step = i"
        >
          <span class="w-5 h-5 rounded-full text-xs flex items-center justify-center" :class="i === step ? 'bg-white/25' : 'bg-surface'">{{ i + 1 }}</span>
          {{ s.label }}
        </button>
        <span v-if="i < steps.length - 1" class="text-ink-soft/40">›</span>
      </template>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
      <!-- 表单区 -->
      <div class="lp-card p-6">
        <h3 class="lp-section-title mb-4">{{ steps[step].label }}</h3>

        <!-- 个人信息 -->
        <div v-if="cur === 'personal_info'" class="space-y-3">
          <Field label="姓名"><input v-model="d.personal_info.name" class="lp-input" /></Field>
          <Field label="求职意向"><input v-model="d.personal_info.intent" class="lp-input" /></Field>
          <div class="grid grid-cols-2 gap-3">
            <Field label="电话"><input v-model="d.personal_info.phone" class="lp-input" /></Field>
            <Field label="邮箱"><input v-model="d.personal_info.email" class="lp-input" /></Field>
          </div>
          <Field label="城市"><input v-model="d.personal_info.city" class="lp-input" /></Field>
        </div>

        <!-- 教育 -->
        <ListEditor v-else-if="cur === 'education'" :items="d.education.items" :fields="eduFields" add-label="添加教育经历" />

        <!-- 工作经历 -->
        <ListEditor v-else-if="cur === 'experience'" :items="d.experience.items" :fields="expFields" add-label="添加工作经历" textarea-key="desc" />

        <!-- 项目 -->
        <ListEditor v-else-if="cur === 'project'" :items="d.project.items" :fields="projFields" add-label="添加项目" textarea-key="desc" />

        <!-- 技能 -->
        <div v-else-if="cur === 'skill'">
          <Field label="技能标签（回车添加）">
            <input class="lp-input" placeholder="如 Java、Redis…" @keyup.enter="addSkill" />
          </Field>
          <div class="flex flex-wrap gap-2 mt-3">
            <span v-for="(t, i) in d.skill.tags" :key="i" class="lp-chip">
              {{ t }}<button class="text-ink-soft/60 hover:text-danger" @click="d.skill.tags.splice(i, 1)">×</button>
            </span>
          </div>
        </div>

        <!-- 自我评价 -->
        <div v-else-if="cur === 'self_evaluation'">
          <Field label="自我评价"><textarea v-model="d.self_evaluation.text" rows="6" class="lp-input"></textarea></Field>
          <p class="text-xs text-ink-soft mt-2">提示：可前往「AI 润色」用 STAR 法则优化经历描述。</p>
        </div>

        <div class="flex justify-between mt-6 pt-4 border-t border-border">
          <button class="lp-btn-ghost" :disabled="step === 0" @click="step--">上一步</button>
          <button v-if="step < steps.length - 1" class="lp-btn-primary" @click="step++">下一步</button>
          <button v-else class="lp-btn-primary" @click="save">完成并保存</button>
        </div>
      </div>

      <!-- A4 预览 -->
      <div class="lp-card p-6 lg:sticky lg:top-20 self-start">
        <div class="flex items-center gap-2 mb-3 text-ink-soft text-sm"><span class="material-symbols-outlined" style="font-size:18px">visibility</span>实时预览</div>
        <div class="bg-white text-[#222] rounded-lg shadow-card border border-border p-6 aspect-[1/1.414] overflow-y-auto text-sm">
          <div class="border-b-2 pb-3 mb-3" style="border-color:rgb(var(--c-primary))">
            <h2 class="text-xl font-bold" style="color:rgb(var(--c-primary))">{{ d.personal_info.name || '你的姓名' }}</h2>
            <p class="text-[#555] mt-0.5">{{ d.personal_info.intent || '求职意向' }}</p>
            <p class="text-xs text-[#777] mt-1">{{ [d.personal_info.phone, d.personal_info.email, d.personal_info.city].filter(Boolean).join(' · ') }}</p>
          </div>
          <PreviewBlock title="教育经历" v-if="d.education.items.length">
            <div v-for="(e, i) in d.education.items" :key="i" class="mb-1.5">
              <div class="flex justify-between"><b>{{ e.school }}</b><span class="text-xs text-[#777]">{{ e.start }} - {{ e.end }}</span></div>
              <p class="text-xs text-[#555]">{{ e.major }} · {{ e.degree }}</p>
            </div>
          </PreviewBlock>
          <PreviewBlock title="工作经历" v-if="d.experience.items.length">
            <div v-for="(e, i) in d.experience.items" :key="i" class="mb-2">
              <div class="flex justify-between"><b>{{ e.company }}</b><span class="text-xs text-[#777]">{{ e.start }} - {{ e.end }}</span></div>
              <p class="text-xs text-[#555]">{{ e.role }}</p>
              <p class="text-xs text-[#444] mt-0.5 whitespace-pre-line">{{ e.desc }}</p>
            </div>
          </PreviewBlock>
          <PreviewBlock title="项目经验" v-if="d.project.items.length">
            <div v-for="(e, i) in d.project.items" :key="i" class="mb-2">
              <b>{{ e.name }}</b><span class="text-xs text-[#777]"> · {{ e.role }}</span>
              <p class="text-xs text-[#444] mt-0.5 whitespace-pre-line">{{ e.desc }}</p>
            </div>
          </PreviewBlock>
          <PreviewBlock title="技能" v-if="d.skill.tags.length">
            <div class="flex flex-wrap gap-1">
              <span v-for="(t, i) in d.skill.tags" :key="i" class="text-xs px-2 py-0.5 rounded bg-[#eef]" style="color:rgb(var(--c-primary))">{{ t }}</span>
            </div>
          </PreviewBlock>
          <PreviewBlock title="自我评价" v-if="d.self_evaluation.text">
            <p class="text-xs text-[#444]">{{ d.self_evaluation.text }}</p>
          </PreviewBlock>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '@/api/client'
import PageHeader from '@/components/common/PageHeader.vue'
import Field from '@/components/resume/Field.vue'
import ListEditor from '@/components/resume/ListEditor.vue'
import PreviewBlock from '@/components/resume/PreviewBlock.vue'

const route = useRoute()
const router = useRouter()
const resumeId = ref(route.params.id || null)
const saving = ref(false)
const step = ref(0)

const steps = [
  { key: 'personal_info', label: '个人信息' },
  { key: 'education', label: '教育经历' },
  { key: 'experience', label: '工作经历' },
  { key: 'project', label: '项目经验' },
  { key: 'skill', label: '技能' },
  { key: 'self_evaluation', label: '自我评价' },
]
const cur = computed(() => steps[step.value].key)

const form = reactive({ title: '新建简历' })
const d = reactive({
  personal_info: { name: '', intent: '', phone: '', email: '', city: '' },
  education: { items: [] },
  experience: { items: [] },
  project: { items: [] },
  skill: { tags: [] },
  self_evaluation: { text: '' },
})

const eduFields = [
  { key: 'school', label: '学校' }, { key: 'major', label: '专业' },
  { key: 'degree', label: '学历' }, { key: 'start', label: '开始' }, { key: 'end', label: '结束' },
]
const expFields = [
  { key: 'company', label: '公司' }, { key: 'role', label: '职位' },
  { key: 'start', label: '开始' }, { key: 'end', label: '结束' }, { key: 'desc', label: '工作描述' },
]
const projFields = [
  { key: 'name', label: '项目名' }, { key: 'role', label: '角色' }, { key: 'desc', label: '项目描述' },
]

function addSkill(e) {
  const v = e.target.value.trim()
  if (v && !d.skill.tags.includes(v)) d.skill.tags.push(v)
  e.target.value = ''
}

async function load() {
  if (!resumeId.value) return
  const r = await api.get(`/resumes/${resumeId.value}`)
  form.title = r.title
  for (const s of r.sections || []) {
    if (d[s.section_type]) Object.assign(d[s.section_type], s.content)
  }
}

async function save() {
  saving.value = true
  try {
    if (!resumeId.value) {
      const r = await api.post('/resumes', { title: form.title })
      resumeId.value = r.id
    } else {
      await api.put(`/resumes/${resumeId.value}`, { title: form.title })
    }
    const sections = steps.map((s, i) => ({ section_type: s.key, sort_order: i, content: d[s.key] }))
    await api.put(`/resumes/${resumeId.value}/sections`, { sections })
    router.push(`/resume/${resumeId.value}/score`)
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>
