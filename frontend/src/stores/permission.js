import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/api/config'

export const usePermissionStore = defineStore('permission', () => {
  const sideMenus = ref([])
  const menus = ref([])
  const missingPermissions = ref([])
  const allPermissions = ref([])
  
  async function fetchPermissions() {
    try {
      const res = await api.get('/permissions/')
      sideMenus.value = res.data.side_menus || []
      menus.value = res.data.menus || []
      missingPermissions.value = res.data.missing_permissions || []
      allPermissions.value = res.data.all_permissions || []

      // 日志窗口打印权限信息
      console.log('%c[权限系统] API调用完成', 'color: #409EFF; font-weight: bold;')
      console.log('%c[权限系统] 当前用户:', 'color: #67C23A;', res.data.username || '未登录')
      console.log('%c[权限系统] 动态菜单:', 'color: #67C23A;', menus.value)
      console.log('%c[权限系统] 缺失权限列表:', 'color: #E6A23C; font-weight: bold;', missingPermissions.value)
      if (missingPermissions.value.length === 0) {
        console.log('%c[权限系统] 恭喜！您拥有所有权限', 'color: #67C23A;')
      } else {
        console.log(`%c[权限系统] 共缺失 ${missingPermissions.value.length} 个权限`, 'color: #F56C6C;')
      }
      
      return res.data
    } catch (error) {
      console.error('获取权限失败:', error)
      sideMenus.value = []
      menus.value = []
      missingPermissions.value = []
      allPermissions.value = []
      throw error
    }
  }
  
  function hasPermission(permissionName) {
    return !missingPermissions.value.includes(permissionName)
  }
  
  function hasMenuPermission(menuName) {
    return sideMenus.value.includes(menuName)
  }
  
  // 获取可用于动态路由的菜单列表
  const dynamicMenus = computed(() => {
    return menus.value.filter(menu => menu.path && menu.component)
  })
  
  // 获取侧边栏显示的菜单列表
  const sidebarMenus = computed(() => {
    return menus.value.filter(menu => menu.is_active !== false)
  })
  
  // 根据路径获取菜单信息
  function getMenuByPath(path) {
    return menus.value.find(menu => menu.path === path)
  }
  
  // 根据路径获取页面标题
  function getPageTitle(path) {
    const menu = getMenuByPath(path)
    return menu?.title || 'ConfigHub'
  }
  
  return {
    sideMenus,
    menus,
    missingPermissions,
    allPermissions,
    fetchPermissions,
    hasPermission,
    hasMenuPermission,
    dynamicMenus,
    sidebarMenus,
    getMenuByPath,
    getPageTitle
  }
})
