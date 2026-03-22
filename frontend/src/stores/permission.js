import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/api/config'

export const usePermissionStore = defineStore('permission', () => {
  const sideMenus = ref([])
  const missingPermissions = ref([])
  
  async function fetchPermissions() {
    try {
      const res = await api.get('/permissions/')
      sideMenus.value = res.data.side_menus || []
      missingPermissions.value = res.data.missing_permissions || []
    } catch (error) {
      console.error('获取权限失败:', error)
      sideMenus.value = []
      missingPermissions.value = []
    }
  }
  
  function hasPermission(permissionName) {
    return !missingPermissions.value.includes(permissionName)
  }
  
  function hasMenuPermission(menuName) {
    return sideMenus.value.includes(menuName)
  }
  
  return {
    sideMenus,
    missingPermissions,
    fetchPermissions,
    hasPermission,
    hasMenuPermission
  }
})
