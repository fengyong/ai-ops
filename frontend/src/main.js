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
import router from './router'
import { usePermissionStore } from './stores/permission'
import { processVNodePermission } from './permission/interceptor'

const app = createApp(App)
const pinia = createPinia()

// 注册所有图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(pinia)
app.use(router)
app.use(ElementPlus)

// 全局混入，拦截所有组件的渲染
app.mixin({
  beforeCreate() {
    const originalRender = this.$options.render
    
    if (originalRender) {
      this.$options.render = function(...args) {
        const vnode = originalRender.apply(this, args)
        return processVNodePermission(vnode, this)
      }
    }
  }
})

// 应用启动时获取权限
const permissionStore = usePermissionStore()
permissionStore.fetchPermissions().then(() => {
  app.mount('#app')
})
