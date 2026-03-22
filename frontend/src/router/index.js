import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ConfigTypeList from '../views/ConfigTypeList.vue'
import ConfigTypeEdit from '../views/ConfigTypeEdit.vue'
import ConfigInstanceList from '../views/ConfigInstanceList.vue'
import ConfigInstanceEdit from '../views/ConfigInstanceEdit.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/types',
    name: 'ConfigTypeList',
    component: ConfigTypeList
  },
  {
    path: '/types/create',
    name: 'ConfigTypeCreate',
    component: ConfigTypeEdit
  },
  {
    path: '/types/edit/:name',
    name: 'ConfigTypeEdit',
    component: ConfigTypeEdit
  },
  {
    path: '/instances',
    name: 'ConfigInstanceList',
    component: ConfigInstanceList
  },
  {
    path: '/instances/create',
    name: 'ConfigInstanceCreate',
    component: ConfigInstanceEdit
  },
  {
    path: '/instances/edit/:id',
    name: 'ConfigInstanceEdit',
    component: ConfigInstanceEdit
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
