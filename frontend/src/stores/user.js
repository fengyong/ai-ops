import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/config'

export const useUserStore = defineStore('user', () => {
  const username = ref(localStorage.getItem('username') || '')
  const isAuthenticated = ref(!!localStorage.getItem('username'))

  function login(user) {
    username.value = user
    isAuthenticated.value = true
    localStorage.setItem('username', user)
  }

  function logout() {
    username.value = ''
    isAuthenticated.value = false
    localStorage.removeItem('username')
  }

  async function fetchUserInfo() {
    try {
      const res = await api.get('/user-info/')
      if (res.data.username) {
        login(res.data.username)
      }
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  return {
    username,
    isAuthenticated,
    login,
    logout,
    fetchUserInfo
  }
})
