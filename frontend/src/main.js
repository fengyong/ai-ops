import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

// Font Awesome styles
import '@fortawesome/fontawesome-free/css/all.css'

// JSON Editor styles
import '@json-editor/json-editor/src/style.css'
import '@json-editor/json-editor/src/themes/bootstrap4.css'

// Sci-Fi Theme styles
import './styles/sci-fi-theme.css'

import App from './App.vue'
import router, { addDynamicRoutes } from './router'
import { usePermissionStore } from './stores/permission'
// import { setPermissionStore } from './permission/interceptor'

const app = createApp(App)
const pinia = createPinia()

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 全局权限控制 - 在 updated 钩子中处理
// 配合 index.html 中的 CSS，默认隐藏按钮，有权限后显示
app.mixin({
  updated() {
    if (!this.$route || !this.$el) return
    
    const permissionStore = usePermissionStore()
    if (!permissionStore || !permissionStore.allPermissions) return
    
    const routePermission = this.$route.meta?.permission
    if (!routePermission) return
    
    // 获取所有未处理的按钮
    const buttons = this.$el.querySelectorAll('.el-button:not([data-perm-checked])')
    
    buttons.forEach(button => {
      button.dataset.permChecked = 'true'
      
      const buttonText = button.textContent.trim()
      if (!buttonText) return
      
      const permissionName = `${routePermission}.${buttonText}`
      const hasPermission = permissionStore.hasPermission(permissionName)
      
      if (hasPermission) {
        // 有权限，显示按钮
        button.dataset.permVisible = 'true'
      }
      // 无权限保持隐藏（CSS 默认 opacity: 0）
    })
  }
})

// 应用启动时获取权限并初始化动态路由
const permissionStore = usePermissionStore()

// 设置权限存储实例到拦截器（如需要）
// setPermissionStore(permissionStore)

permissionStore.fetchPermissions().then((data) => {
  // 根据后端返回的菜单数据生成动态路由
  if (data && data.menus) {
    addDynamicRoutes(data.menus)
    console.log('[应用启动] 动态路由已生成')
  }
  app.mount('#app')
}).catch((error) => {
  console.error('[应用启动] 获取权限失败:', error)
  // 即使获取权限失败也挂载应用，显示登录页面
  app.mount('#app')
})
