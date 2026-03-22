<template>
  <div class="home">
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>配置类型</span>
              <el-icon><Document /></el-icon>
            </div>
          </template>
          <div class="stat-number">{{ stats.types }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>配置实例</span>
              <el-icon><Files /></el-icon>
            </div>
          </template>
          <div class="stat-number">{{ stats.instances }}</div>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <span>总版本数</span>
              <el-icon><Clock /></el-icon>
            </div>
          </template>
          <div class="stat-number">{{ stats.versions }}</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card class="quick-actions">
      <template #header>
        <span>快速操作</span>
      </template>
      <el-row :gutter="20">
        <el-col :span="12">
          <el-button type="primary" @click="$router.push('/types/create')">
            <el-icon><Plus /></el-icon> 新建配置类型
          </el-button>
        </el-col>
        <el-col :span="12">
          <el-button type="success" @click="$router.push('/instances/create')">
            <el-icon><Plus /></el-icon> 新建配置实例
          </el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Document, Files, Clock, Plus } from '@element-plus/icons-vue'
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
  } catch (error) {
    console.error('Failed to load stats:', error)
  }
})
</script>

<style scoped>
.stat-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-number {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  text-align: center;
  padding: 20px 0;
}

.quick-actions {
  margin-top: 20px;
}

.quick-actions .el-button {
  width: 100%;
}
</style>
