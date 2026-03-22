<template>
  <el-container class="app-container">
    <el-aside :width="isCollapse ? '64px' : '200px'" class="sidebar" :class="{ 'collapsed': isCollapse }">
      <div class="logo" :class="{ 'collapsed': isCollapse }">
        <h2 v-if="!isCollapse">ConfigHub</h2>
        <el-icon v-else class="logo-icon"><Setting /></el-icon>
      </div>
      <div class="collapse-btn" @click.stop="toggleCollapse">
        <el-icon :class="{ 'rotate': isCollapse }">
          <ArrowLeft v-if="!isCollapse" />
          <ArrowRight v-else />
        </el-icon>
      </div>
      <el-menu
        :default-active="$route.path"
        router
        class="sidebar-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        :collapse="isCollapse"
      >
        <el-menu-item index="/">
          <el-icon><HomeFilled /></el-icon>
          <template #title>
            <span>首页</span>
          </template>
        </el-menu-item>
        <el-menu-item index="/types">
          <el-icon><Document /></el-icon>
          <template #title>
            <span>配置类型</span>
          </template>
        </el-menu-item>
        <el-menu-item index="/instances">
          <el-icon><Files /></el-icon>
          <template #title>
            <span>配置实例</span>
          </template>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="header">
        <span class="page-title">{{ currentPageTitle }}</span>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><User /></el-icon>
              <span class="username">{{ userStore.username || '未登录' }}</span>
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main class="main-content" :class="{ 'expanded': isCollapse }">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { HomeFilled, Document, Files, Setting, ArrowLeft, ArrowRight, User, ArrowDown, SwitchButton } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

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

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const handleCommand = async (command) => {
  if (command === 'logout') {
    try {
      const csrfToken = document.cookie
        .split('; ')
        .find(row => row.startsWith('csrftoken='))
        ?.split('=')[1] || ''
      
      const res = await fetch('/api/logout/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        credentials: 'include'
      })
      
      if (res.ok) {
        userStore.logout()
        ElMessage.success('已退出登录')
        router.push('/login')
      } else {
        const data = await res.json()
        ElMessage.error(data.error || '退出登录失败')
      }
    } catch (error) {
      console.error('退出登录错误:', error)
      ElMessage.error('退出登录失败')
    }
  }
}

onMounted(() => {
  if (!userStore.username) {
    userStore.username = 'admin'
    userStore.isAuthenticated = true
  }
})
</script>

<style scoped>
.app-container {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  position: relative;
  transition: width 0.3s ease;
}

.sidebar.collapsed {
  width: 64px !important;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #2c3e50;
  transition: all 0.3s ease;
}

.logo.collapsed {
  justify-content: center;
}

.logo h2 {
  color: #fff;
  margin: 0;
  font-size: 18px;
  transition: all 0.3s ease;
}

.logo-icon {
  color: #fff;
  font-size: 24px;
}

.collapse-btn {
  position: absolute;
  top: 20px;
  right: -10px;
  width: 24px;
  height: 24px;
  background-color: #409EFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  z-index: 10;
  transition: all 0.3s ease;
}

.collapse-btn:hover {
  background-color: #66b1ff;
  transform: scale(1.1);
}

.collapse-btn:active {
  transform: scale(0.95);
}

.rotate {
  transform: rotate(180deg);
  transition: transform 0.3s ease;
}

.sidebar-menu {
  border-right: none;
  height: calc(100vh - 60px);
}

.header {
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.page-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  margin: 0 8px;
  color: #333;
  font-size: 14px;
}

.main-content {
  background-color: #f0f2f5;
  padding: 20px;
  transition: all 0.3s ease;
}

.main-content.expanded {
  padding: 20px 20px 20px 30px;
}

/* 为编辑页面提供更多展示空间 */
:deep(.config-instance-edit),
:deep(.config-type-edit) {
  max-width: none;
  width: 100%;
}

:deep(.content-editor) {
  margin-top: 10px;
}

:deep(.editor-wrapper) {
  width: 100%;
  min-height: 600px;
}
</style>
