<template>
  <div class="min-h-screen">
    <!-- 桌面侧边栏 -->
    <aside class="hidden lg:flex fixed left-0 top-0 h-full w-[260px] flex-col bg-surface border-r border-border z-40">
      <div class="px-5 py-5">
        <RouterLink to="/"><Logo :tagline="true" /></RouterLink>
      </div>
      <nav class="flex-1 px-3 space-y-1 overflow-y-auto">
        <RouterLink
          v-for="item in nav" :key="item.to" :to="item.to"
          class="group flex items-center gap-3 px-3.5 py-2.5 rounded-btn text-ink-soft hover:bg-surface-2 transition-all"
          :class="isActive(item) ? '!bg-primary-soft !text-primary font-semibold' : ''"
        >
          <span class="material-symbols-outlined" :class="isActive(item) ? 'ms-fill' : ''" style="font-size:22px">{{ item.icon }}</span>
          <span class="text-sm">{{ item.label }}</span>
          <span v-if="item.badge" class="ml-auto text-[10px] font-bold px-1.5 py-0.5 rounded-pill bg-accent/15 text-accent">{{ item.badge }}</span>
        </RouterLink>
      </nav>
      <div class="px-3 py-4 border-t border-border space-y-1">
        <RouterLink to="/profile" class="flex items-center gap-3 px-3.5 py-2.5 rounded-btn text-ink-soft hover:bg-surface-2">
          <span class="material-symbols-outlined" style="font-size:22px">settings</span>
          <span class="text-sm">个人中心</span>
        </RouterLink>
      </div>
    </aside>

    <!-- 顶部栏 -->
    <header class="fixed top-0 right-0 left-0 lg:left-[260px] h-16 glass border-b border-border z-30 flex items-center justify-between px-4 lg:px-8">
      <div class="flex items-center gap-3 flex-1 max-w-md">
        <div class="lg:hidden"><Logo :show-text="false" :size="32" /></div>
        <div class="relative w-full hidden sm:block">
          <span class="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-ink-soft/60" style="font-size:20px">search</span>
          <input v-model="search" @keyup.enter="doSearch" class="lp-input !rounded-pill !py-2 pl-10" placeholder="搜索职位、公司、简历…" />
        </div>
      </div>
      <div class="flex items-center gap-2 lg:gap-3">
        <ThemeToggle />
        <button class="w-9 h-9 rounded-full hover:bg-surface-2 flex items-center justify-center text-ink-soft relative">
          <span class="material-symbols-outlined" style="font-size:22px">notifications</span>
          <span class="absolute top-1.5 right-2 w-2 h-2 rounded-full bg-accent"></span>
        </button>
        <RouterLink to="/profile" class="flex items-center gap-2">
          <div class="w-9 h-9 rounded-full bg-primary text-on-primary flex items-center justify-center font-bold font-display">
            {{ (user.user?.nickname || 'U').slice(0, 1) }}
          </div>
        </RouterLink>
      </div>
    </header>

    <!-- 内容区 -->
    <main class="lg:ml-[260px] pt-16 pb-20 lg:pb-8 min-h-screen">
      <div class="max-w-[1180px] mx-auto px-4 lg:px-8 py-6">
        <slot />
      </div>
    </main>

    <!-- 移动端底部 Tab -->
    <nav class="lg:hidden fixed bottom-0 inset-x-0 h-16 glass border-t border-border z-40 flex justify-around items-center px-2">
      <RouterLink
        v-for="item in mobileNav" :key="item.to" :to="item.to"
        class="flex flex-col items-center justify-center gap-0.5 flex-1"
        :class="isActive(item) ? 'text-primary' : 'text-ink-soft'"
      >
        <span class="material-symbols-outlined" :class="isActive(item) ? 'ms-fill' : ''" style="font-size:24px">{{ item.icon }}</span>
        <span class="text-[10px] font-medium">{{ item.label }}</span>
      </RouterLink>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Logo from '@/components/common/Logo.vue'
import ThemeToggle from '@/components/common/ThemeToggle.vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const user = useUserStore()
const search = ref('')

const nav = [
  { to: '/', label: '工作台', icon: 'grid_view', match: ['dashboard'] },
  { to: '/resume/list', label: '简历中心', icon: 'description', match: ['resume'] },
  { to: '/interview/setup', label: '模拟面试', icon: 'forum', match: ['interview'] },
  { to: '/jobs/list', label: '职位匹配', icon: 'work', match: ['jobs-list', 'jobs-detail'] },
  { to: '/jobs/applications', label: '投递追踪', icon: 'view_kanban', match: ['jobs-applications'] },
  { to: '/plan', label: '求职规划', icon: 'insights', match: ['plan'] },
  { to: '/company/list', label: '公司画像', icon: 'apartment', match: ['company'] },
  { to: '/prepare', label: '求职准备', icon: 'quiz', match: ['prepare'] },
  { to: '/rental', label: '租房选址', icon: 'pin_drop', match: ['rental'] },
]

const mobileNav = [
  { to: '/', label: '首页', icon: 'home', match: ['dashboard'] },
  { to: '/jobs/list', label: '职位', icon: 'work', match: ['jobs-list', 'jobs-detail', 'jobs-applications'] },
  { to: '/interview/setup', label: '面试', icon: 'forum', match: ['interview'] },
  { to: '/resume/list', label: '简历', icon: 'description', match: ['resume'] },
  { to: '/profile', label: '我的', icon: 'person', match: ['profile'] },
]

function isActive(item) {
  const name = route.name || ''
  if (item.match) return item.match.some((m) => String(name).startsWith(m))
  return route.path === item.to
}
function doSearch() {
  if (search.value.trim()) router.push({ path: '/jobs/list', query: { q: search.value.trim() } })
}
</script>
