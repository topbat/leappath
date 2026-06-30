<template>
  <div class="max-w-2xl">
    <PageHeader title="个人中心" subtitle="账号设置 · 求职偏好 · 配额" />

    <div class="lp-card p-6 mb-5">
      <div class="flex items-center gap-4 mb-6">
        <div class="w-16 h-16 rounded-full bg-primary text-on-primary flex items-center justify-center font-display font-extrabold text-2xl">{{ (form.nickname || 'U')[0] }}</div>
        <div>
          <h3 class="font-display font-bold text-ink text-lg">{{ form.nickname }}</h3>
          <p class="text-sm text-ink-soft">{{ user.user?.email || '演示账号' }}</p>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 gap-4">
        <Field label="昵称"><input v-model="form.nickname" class="lp-input" /></Field>
        <Field label="当前城市"><input v-model="form.current_city" class="lp-input" /></Field>
        <Field label="最高学历"><input v-model="form.education_level" class="lp-input" /></Field>
        <Field label="工作年限"><input v-model.number="form.years_of_experience" type="number" class="lp-input" /></Field>
        <Field label="期望薪资下限"><input v-model.number="form.expected_salary_min" type="number" class="lp-input" /></Field>
        <Field label="期望薪资上限"><input v-model.number="form.expected_salary_max" type="number" class="lp-input" /></Field>
      </div>
      <button class="lp-btn-primary mt-5" @click="save">{{ saved ? '已保存 ✓' : '保存修改' }}</button>
    </div>

    <div class="lp-card p-6 mb-5">
      <h3 class="lp-section-title mb-4">主题外观</h3>
      <div class="grid grid-cols-2 gap-3">
        <button v-for="t in themes" :key="t.key" class="rounded-card border-2 p-4 text-left transition-all" :class="theme.theme === t.key ? 'border-primary' : 'border-border'" @click="theme.set(t.key)">
          <div class="flex gap-1 mb-2"><i class="w-5 h-5 rounded-full" :style="{ background: t.c1 }"></i><i class="w-5 h-5 rounded-full" :style="{ background: t.c2 }"></i></div>
          <p class="font-display font-bold text-ink">{{ t.label }}</p>
          <p class="text-xs text-ink-soft">{{ t.desc }}</p>
        </button>
      </div>
    </div>

    <div class="lp-card p-6">
      <h3 class="lp-section-title mb-4">AI 配额（演示）</h3>
      <ProgressBar label="本月模拟面试" :value="2" :max="10" suffix=" 次" color="primary" />
      <div class="mt-4 flex gap-2">
        <button class="lp-btn-outline" @click="logout">退出登录</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import PageHeader from '@/components/common/PageHeader.vue'
import Field from '@/components/resume/Field.vue'
import ProgressBar from '@/components/charts/ProgressBar.vue'
import { useUserStore } from '@/stores/user'
import { useThemeStore } from '@/stores/theme'

const router = useRouter()
const user = useUserStore()
const theme = useThemeStore()
const saved = ref(false)
const form = reactive({ nickname: '', current_city: '', education_level: '', years_of_experience: 0, expected_salary_min: 0, expected_salary_max: 0 })
const themes = [
  { key: 'leap', label: '专业权威', desc: '深企业蓝 · Inter', c1: '#1A56DB', c2: '#0D9488' },
  { key: 'flux', label: '灵动活力', desc: '亮紫 · 玻璃拟态', c1: '#7C3AED', c2: '#FE7D66' },
]

async function save() {
  await user.updateProfile({ ...form })
  saved.value = true
  setTimeout(() => (saved.value = false), 1500)
}
function logout() { user.logout(); router.push('/login') }

onMounted(async () => {
  if (!user.user) await user.fetchMe()
  if (user.user) Object.keys(form).forEach((k) => { if (user.user[k] != null) form[k] = user.user[k] })
})
</script>
