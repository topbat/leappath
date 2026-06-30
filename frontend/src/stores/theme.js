import { defineStore } from 'pinia'

const KEY = 'leappath_theme'

export const useThemeStore = defineStore('theme', {
  state: () => ({
    theme: localStorage.getItem(KEY) || 'leap', // 'leap' | 'flux'
  }),
  getters: {
    label: (s) => (s.theme === 'leap' ? '专业权威' : '灵动活力'),
    isFlux: (s) => s.theme === 'flux',
  },
  actions: {
    apply() {
      document.documentElement.setAttribute('data-theme', this.theme)
    },
    set(theme) {
      this.theme = theme
      localStorage.setItem(KEY, theme)
      this.apply()
    },
    toggle() {
      this.set(this.theme === 'leap' ? 'flux' : 'leap')
    },
  },
})
