<template>
  <div v-if="route.meta.plain">
    <RouterView />
  </div>
  <AppShell v-else>
    <RouterView v-slot="{ Component }">
      <component :is="Component" class="lp-fade" />
    </RouterView>
  </AppShell>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import AppShell from '@/components/layout/AppShell.vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const user = useUserStore()

onMounted(() => {
  // 演示模式下后端会回退到演示用户，这里仅尝试拉取
  user.fetchMe()
})
</script>
