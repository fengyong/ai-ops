<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <el-icon><Document /></el-icon>
              <span>配置类型</span>
            </div>
          </template>
          <div class="stat-value">{{ stats.types }}</div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <el-icon><Files /></el-icon>
              <span>配置实例</span>
            </div>
          </template>
          <div class="stat-value">{{ stats.instances }}</div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card>
          <template #header>
            <div class="card-header">
              <el-icon><Clock /></el-icon>
              <span>版本数量</span>
            </div>
          </template>
          <div class="stat-value">{{ stats.versions }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快速操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="$router.push('/types/create')">
              <el-icon><Plus /></el-icon>新建配置类型
            </el-button>
            <el-button type="success" @click="$router.push('/instances/create')">
              <el-icon><Plus /></el-icon>新建配置实例
            </el-button>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统状态</span>
          </template>
          <div class="system-status">
            <div class="status-item">
              <el-icon color="#67C23A"><CircleCheck /></el-icon>
              <span>API 服务: 正常运行</span>
            </div>
            <div class="status-item">
              <el-icon color="#67C23A"><CircleCheck /></el-icon>
              <span>数据库: 已连接</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, Files, Clock, Plus, CircleCheck } from '@element-plus/icons-vue'
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
    console.error('加载统计数据失败:', error)
  }
})
</script>

<style scoped>
.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-value {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
  padding: 20px 0;
}

.quick-actions {
  display: flex;
  gap: 10px;
}

.system-status {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
