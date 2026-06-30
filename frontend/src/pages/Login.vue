<template>
  <div class="min-h-screen flex items-center justify-center bg-bg px-4 relative overflow-hidden">
    <!-- 背景装饰 -->
    <div class="absolute -top-32 -right-32 w-96 h-96 rounded-full bg-primary/10 blur-3xl"></div>
    <div class="absolute -bottom-32 -left-32 w-96 h-96 rounded-full bg-accent/10 blur-3xl"></div>

    <div class="w-full max-w-md lp-card glass p-8 relative z-10 lp-fade">
      <div class="flex flex-col items-center text-center mb-6">
        <Logo :show-text="false" :size="56" />
        <h1 class="font-display text-2xl font-extrabold text-ink mt-4">跃途 LeapPath</h1>
        <p class="text-ink-soft text-sm mt-1">不止帮你找到工作，更帮你找到「对」的工作</p>
      </div>

      <div class="flex gap-2 mb-5">
        <ThemeToggle />
      </div>

      <div class="space-y-4">
        <div>
          <label class="text-sm font-medium text-ink-soft mb-1.5 block">账号</label>
          <input v-model="account" class="lp-input" placeholder="邮箱 / 手机号" />
        </div>
        <div>
          <label class="text-sm font-medium text-ink-soft mb-1.5 block">密码</label>
          <input v-model="password" type="password" class="lp-input" placeholder="请输入密码" @keyup.enter="submit" />
        </div>
        <p v-if="error" class="text-sm text-danger">{{ error }}</p>
        <button class="lp-btn-primary w-full py-2.5" :disabled="loading" @click="submit">
          {{ loading ? '登录中…' : isRegister ? '注册并登录' : '登录' }}
        </button>
        <button class="lp-btn-ghost w-full text-sm" @click="isRegister = !isRegister">
          {{ isRegister ? '已有账号？去登录' : '没有账号？去注册' }}
        </button>
      </div>

      <div class="mt-6 pt-5 border-t border-border">
        <button class="lp-btn-outline w-full" @click="demoLogin">
          <span class="material-symbols-outlined" style="font-size:20px">bolt</span>
          一键体验（演示账号）
        </button>
        <p class="text-xs text-ink-soft/70 text-center mt-2">demo@leappath.app / leappath</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import Logo from '@/components/common/Logo.vue'
import ThemeToggle from '@/components/common/ThemeToggle.vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const user = useUserStore()
const account = ref('demo@leappath.app')
const password = ref('leappath')
const nickname = ref('')
const isRegister = ref(false)
const loading = ref(false)
const error = ref('')

async function submit() {
  error.value = ''
  loading.value = true
  try {
    if (isRegister.value) await user.register(account.value, password.value, nickname.value)
    else await user.login(account.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
async function demoLogin() {
  account.value = 'demo@leappath.app'
  password.value = 'leappath'
  isRegister.value = false
  await submit()
}
</script>
