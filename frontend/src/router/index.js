import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'

// 组件映射表 - 用于动态路由解析
const componentMap = {
  'Home': () => import('../views/Home.vue'),
  'ConfigTypeList': () => import('../views/ConfigTypeList.vue'),
  'ConfigTypeEdit': () => import('../views/ConfigTypeEdit.vue'),
  'ConfigInstanceList': () => import('../views/ConfigInstanceList.vue'),
  'ConfigInstanceEdit': () => import('../views/ConfigInstanceEdit.vue')
}

// 基础路由（不需要权限控制的页面）
const baseRoutes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  }
]

// 动态路由存储
let dynamicRoutes = []

const router = createRouter({
  history: createWebHistory(),
  routes: baseRoutes
})

// 根据后端菜单数据生成动态路由
export function generateRoutesFromMenus(menus) {
  const routes = []
  
  for (const menu of menus) {
    // 只处理有组件的菜单
    if (!menu.component) continue
    
    const componentLoader = componentMap[menu.component]
    if (!componentLoader) {
      console.warn(`[路由] 未找到组件: ${menu.component}`)
      continue
    }
    
    console.log(`[路由] 生成路由: ${menu.path} -> ${menu.component}`)
    
    routes.push({
      path: menu.path,
      name: menu.name,
      component: componentLoader,
      meta: {
        permission: menu.permission_name || menu.name,
        title: menu.title,
        requiresAuth: true
      }
    })
    
    // 处理子路由（如编辑页面）
    if (menu.children && Array.isArray(menu.children)) {
      for (const child of menu.children) {
        if (!child.component) continue
        
        const childLoader = componentMap[child.component]
        if (!childLoader) continue
        
        routes.push({
          path: child.path,
          name: child.name,
          component: childLoader,
          meta: {
            permission: child.permission_name || menu.permission_name || menu.name,
            title: child.title,
            requiresAuth: true
          }
        })
      }
    }
  }
  
  return routes
}

// 添加动态路由到路由器
export function addDynamicRoutes(menus) {
  // 清除旧的路由
  dynamicRoutes.forEach(route => {
    router.removeRoute(route.name)
  })
  
  // 生成新路由
  dynamicRoutes = generateRoutesFromMenus(menus)
  
  // 添加新路由
  dynamicRoutes.forEach(route => {
    router.addRoute(route)
  })
  
  console.log('[路由] 动态路由已更新:', dynamicRoutes.map(r => r.path))
  return dynamicRoutes
}

// 路由守卫
router.beforeEach((to, from, next) => {
  const username = localStorage.getItem('username')
  const isAuthenticated = !!username
  
  // 检查是否是动态路由（在基础路由中找不到）
  const baseRoutePaths = ['/login', '/']
  const isDynamicRoute = !baseRoutePaths.includes(to.path) && to.matched.length === 0
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/')
  } else if (isDynamicRoute && isAuthenticated) {
    // 动态路由可能还没加载，等待一下再试
    console.log('[路由守卫] 等待动态路由加载:', to.path)
    setTimeout(() => {
      next({ ...to, replace: true })
    }, 100)
  } else {
    next()
  }
})

export default router
