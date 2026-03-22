<template>
  <el-container class="app-container">
    <el-aside width="200px" class="sidebar">
      <div class="logo">
        <h2>ConfigHub</h2>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/types">
          <el-icon><Document /></el-icon>
          <span>配置类型</span>
        </el-menu-item>
        <el-menu-item index="/instances">
          <el-icon><Files /></el-icon>
          <span>配置实例</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <span class="page-title">{{ currentPageTitle }}</span>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Document, Files } from '@element-plus/icons-vue'

const route = useRoute()

const currentPageTitle = computed(() => {
  const titles = {
    '/': '仪表盘',
    '/types': '配置类型管理',
    '/types/create': '新建配置类型',
    '/types/edit': '编辑配置类型',
    '/instances': '配置实例管理',
    '/instances/create': '新建配置实例',
    '/instances/edit': '编辑配置实例'
  }
  return titles[route.path] || 'ConfigHub'
})
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2c3e50;
}

.logo h2 {
  color: #fff;
  margin: 0;
  font-size: 18px;
}

.sidebar-menu {
  border-right: none;
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
}

.page-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
