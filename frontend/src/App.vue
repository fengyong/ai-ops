<template>
  <div class="app-container grid-bg">
    <!-- Scanline overlay -->
    <div class="scanlines"></div>
    
    <el-container class="main-wrapper">
      <!-- Sci-Fi Sidebar -->
      <el-aside width="220px" class="sf-sidebar">
        <div class="logo">
          <div class="logo-icon">
            <el-icon :size="28" class="neon-icon"><Setting /></el-icon>
          </div>
          <div class="logo-text">
            <h2 class="font-orbitron text-glow">CONFIG<span class="text-neon-magenta">HUB</span></h2>
            <span class="version">v1.0</span>
          </div>
        </div>
        
        <nav class="sf-nav">
          <div 
            v-for="item in menuItems" 
            :key="item.path"
            class="sf-nav-item"
            :class="{ active: $route.path === item.path }"
            @click="$router.push(item.path)"
          >
            <el-icon :size="18"><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </div>
        </nav>
        
        <!-- Status Panel -->
        <div class="status-panel">
          <div class="status-item">
            <span class="status-dot status-online"></span>
            <span class="data-label">System Online</span>
          </div>
        </div>
      </el-aside>
      
      <el-container>
        <!-- Sci-Fi Header -->
        <el-header class="sf-header">
          <div class="header-left">
            <span class="page-title font-orbitron">{{ currentPageTitle }}</span>
          </div>
          <div class="header-right">
            <div class="time-display font-tech-mono">
              {{ currentTime }}
            </div>
          </div>
        </el-header>
        
        <!-- Main Content -->
        <el-main class="sf-main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { HomeFilled, Document, Files, Setting } from '@element-plus/icons-vue'

const route = useRoute()
const currentTime = ref('')

const menuItems = [
  { path: '/', icon: 'HomeFilled', label: 'Dashboard' },
  { path: '/types', icon: 'Document', label: 'Config Types' },
  { path: '/instances', icon: 'Files', label: 'Instances' }
]

const currentPageTitle = computed(() => {
  const titles = {
    '/': 'Dashboard',
    '/types': 'Config Types',
    '/types/create': 'New Config Type',
    '/instances': 'Config Instances',
    '/instances/create': 'New Instance'
  }
  return titles[route.path] || 'ConfigHub'
})

const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleTimeString('en-US', { 
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

let timer = null
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 1000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
@import './styles/sci-fi-theme.css';

.app-container {
  height: 100vh;
  background-color: var(--deep-space);
  position: relative;
}

.main-wrapper {
  height: 100vh;
  position: relative;
  z-index: 1;
}

/* Logo Section */
.logo {
  height: 80px;
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-bottom: 1px solid var(--border-subtle);
  gap: 12px;
}

.logo-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--neon-cyan);
  border-radius: 4px;
  background: rgba(0, 240, 255, 0.1);
}

.neon-icon {
  color: var(--neon-cyan);
  filter: drop-shadow(0 0 5px var(--neon-cyan));
}

.logo-text h2 {
  margin: 0;
  font-size: 16px;
  letter-spacing: 2px;
}

.version {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  color: var(--text-dimmed);
  letter-spacing: 1px;
}

/* Status Panel */
.status-panel {
  position: absolute;
  bottom: 20px;
  left: 20px;
  right: 20px;
  padding: 15px;
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.3);
}

.status-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Header */
.sf-header {
  background: rgba(18, 18, 26, 0.95);
  border-bottom: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  backdrop-filter: blur(10px);
}

.page-title {
  font-size: 18px;
  color: var(--neon-cyan);
  letter-spacing: 3px;
  text-transform: uppercase;
}

.time-display {
  font-size: 16px;
  color: var(--neon-cyan);
  text-shadow: 0 0 10px rgba(0, 240, 255, 0.5);
  letter-spacing: 2px;
}

/* Main Content */
.sf-main-content {
  background: transparent;
  padding: 20px;
  overflow-y: auto;
}

/* Override Element Plus styles */
:deep(.el-card) {
  background: rgba(18, 18, 26, 0.9);
  border: 1px solid var(--border-dimmed);
  border-radius: 4px;
}

:deep(.el-card__header) {
  border-bottom: 1px solid var(--border-subtle);
  color: var(--neon-cyan);
  font-family: 'Orbitron', sans-serif;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 2px;
}

:deep(.el-table) {
  background: transparent;
  color: var(--text-primary);
}

:deep(.el-table th) {
  background: rgba(0, 240, 255, 0.1);
  color: var(--neon-cyan);
  font-family: 'Orbitron', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

:deep(.el-table tr) {
  background: transparent;
}

:deep(.el-table td) {
  border-bottom: 1px solid var(--border-subtle);
}

:deep(.el-table--enable-row-hover .el-table__body tr:hover > td) {
  background: rgba(0, 240, 255, 0.05);
}

:deep(.el-button--primary) {
  background: rgba(0, 240, 255, 0.1);
  border-color: var(--neon-cyan);
  color: var(--neon-cyan);
}

:deep(.el-button--primary:hover) {
  background: rgba(0, 240, 255, 0.2);
  border-color: var(--neon-cyan);
  box-shadow: 0 0 15px rgba(0, 240, 255, 0.3);
}

:deep(.el-input__wrapper) {
  background: rgba(10, 10, 15, 0.8);
  box-shadow: 0 0 0 1px var(--border-dimmed) inset;
}

:deep(.el-input__inner) {
  color: var(--text-primary);
  font-family: 'Share Tech Mono', monospace;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--neon-cyan) inset;
}

:deep(.el-form-item__label) {
  color: var(--text-secondary);
  font-family: 'Orbitron', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
}
</style>
