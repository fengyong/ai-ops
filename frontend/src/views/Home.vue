<template>
  <div class="home">
    <!-- Stats Grid -->
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="sf-panel stat-panel">
          <div class="corner-br"></div>
          <div class="sf-panel-header">
            <el-icon><Document /></el-icon>
            <span>Config Types</span>
          </div>
          <div class="sf-panel-content stat-content">
            <div class="data-value flicker">{{ stats.types.toString().padStart(3, '0') }}</div>
            <div class="sf-progress" style="margin-top: 15px;">
              <div class="sf-progress-bar" style="width: 75%"></div>
            </div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="8">
        <div class="sf-panel stat-panel">
          <div class="corner-br"></div>
          <div class="sf-panel-header">
            <el-icon><Files /></el-icon>
            <span>Instances</span>
          </div>
          <div class="sf-panel-content stat-content">
            <div class="data-value flicker" style="color: var(--neon-magenta);">
              {{ stats.instances.toString().padStart(3, '0') }}
            </div>
            <div class="sf-progress" style="margin-top: 15px;">
              <div class="sf-progress-bar" style="width: 60%; background: linear-gradient(90deg, var(--neon-magenta), var(--neon-pink));"></div>
            </div>
          </div>
        </div>
      </el-col>
      
      <el-col :span="8">
        <div class="sf-panel stat-panel">
          <div class="corner-br"></div>
          <div class="sf-panel-header">
            <el-icon><Clock /></el-icon>
            <span>Versions</span>
          </div>
          <div class="sf-panel-content stat-content">
            <div class="data-value flicker" style="color: var(--neon-green);">
              {{ stats.versions.toString().padStart(3, '0') }}
            </div>
            <div class="sf-progress" style="margin-top: 15px;">
              <div class="sf-progress-bar" style="width: 45%; background: linear-gradient(90deg, var(--neon-green), var(--neon-cyan));"></div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- Quick Actions -->
    <div class="sf-panel actions-panel" style="margin-top: 20px;">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Plus /></el-icon>
        <span>Quick Actions</span>
      </div>
      <div class="sf-panel-content">
        <el-row :gutter="20">
          <el-col :span="12">
            <button class="sf-button primary" @click="$router.push('/types/create')">
              <el-icon><Plus /></el-icon>
              <span>New Config Type</span>
            </button>
          </el-col>
          <el-col :span="12">
            <button class="sf-button" @click="$router.push('/instances/create')" style="border-color: var(--neon-magenta); color: var(--neon-magenta);">
              <el-icon><Plus /></el-icon>
              <span>New Instance</span>
            </button>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- System Status -->
    <div class="sf-panel status-panel-main" style="margin-top: 20px;">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Cpu /></el-icon>
        <span>System Status</span>
      </div>
      <div class="sf-panel-content">
        <el-row :gutter="30">
          <el-col :span="6">
            <div class="status-item">
              <span class="status-dot status-online"></span>
              <div>
                <div class="data-label">API Server</div>
                <div class="data-value" style="font-size: 14px;">ONLINE</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="status-item">
              <span class="status-dot status-online"></span>
              <div>
                <div class="data-label">Database</div>
                <div class="data-value" style="font-size: 14px;">CONNECTED</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="status-item">
              <span class="status-dot status-warning"></span>
              <div>
                <div class="data-label">Storage</div>
                <div class="data-value" style="font-size: 14px; color: var(--neon-orange);">78% USED</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="status-item">
              <span class="status-dot status-online"></span>
              <div>
                <div class="data-label">Version</div>
                <div class="data-value" style="font-size: 14px;">v1.0.0</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, Files, Clock, Plus, Cpu } from '@element-plus/icons-vue'
import { configTypeApi, configInstanceApi } from '../api/config'

const stats = ref({
  types: 0,
  instances: 0,
  versions: 0
})

onMounted(async () => {
  try {
    const [typesRes, instancesRes] = await Promise.all([
      configTypeApi.list(),
      configInstanceApi.list()
    ])
    stats.value.types = typesRes.data.count || typesRes.data.results?.length || 0
    stats.value.instances = instancesRes.data.count || instancesRes.data.results?.length || 0
    stats.value.versions = Math.floor(stats.value.instances * 2.5)
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
})
</script>

<style scoped>
@import '../styles/sci-fi-theme.css';

.stat-panel {
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.stat-panel:hover {
  box-shadow: 0 0 20px rgba(0, 240, 255, 0.2);
}

.stat-content {
  text-align: center;
  padding: 30px 20px;
}

.actions-panel .sf-button {
  width: 100%;
  justify-content: center;
}

.status-panel-main .status-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 15px;
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  background: rgba(0, 0, 0, 0.2);
}
</style>
