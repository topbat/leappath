import { defineStore } from 'pinia'
import { api, setToken } from '@/api/client'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    loaded: false,
  }),
  actions: {
    async fetchMe() {
      try {
        this.user = await api.get('/auth/me')
      } catch (e) {
        this.user = null
      }
      this.loaded = true
    },
    async login(account, password) {
      const res = await api.post('/auth/login', { account, password })
      setToken(res.token)
      this.user = res.user
      return res
    },
    async register(account, password, nickname) {
      const res = await api.post('/auth/register', { account, password, nickname })
      setToken(res.token)
      this.user = res.user
      return res
    },
    async updateProfile(payload) {
      this.user = await api.put('/auth/me', payload)
    },
    logout() {
      setToken('')
      this.user = null
    },
  },
})
