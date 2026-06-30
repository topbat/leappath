import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useThemeStore } from './stores/theme'
import './style.css'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// 应用持久化的主题
useThemeStore(pinia).apply()

app.mount('#app')
