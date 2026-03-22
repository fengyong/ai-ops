import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import ConfigTypeList from '../views/ConfigTypeList.vue'
import ConfigTypeEdit from '../views/ConfigTypeEdit.vue'
import ConfigInstanceList from '../views/ConfigInstanceList.vue'
import ConfigInstanceEdit from '../views/ConfigInstanceEdit.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { permission: '首页', requiresAuth: true }
  },
  {
    path: '/types',
    name: 'ConfigTypeList',
    component: ConfigTypeList,
    meta: { permission: '配置类型', requiresAuth: true }
  },
  {
    path: '/types/create',
    name: 'ConfigTypeCreate',
    component: ConfigTypeEdit,
    meta: { permission: '配置类型', requiresAuth: true }
  },
  {
    path: '/types/edit/:name',
    name: 'ConfigTypeEdit',
    component: ConfigTypeEdit,
    meta: { permission: '配置类型', requiresAuth: true }
  },
  {
    path: '/instances',
    name: 'ConfigInstanceList',
    component: ConfigInstanceList,
    meta: { permission: '配置实例', requiresAuth: true }
  },
  {
    path: '/instances/create',
    name: 'ConfigInstanceCreate',
    component: ConfigInstanceEdit,
    meta: { permission: '配置实例', requiresAuth: true }
  },
  {
    path: '/instances/edit/:id',
    name: 'ConfigInstanceEdit',
    component: ConfigInstanceEdit,
    meta: { permission: '配置实例', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const username = localStorage.getItem('username')
  const isAuthenticated = !!username
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
