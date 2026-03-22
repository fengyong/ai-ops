<template>
  <div class="config-instance-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配置实例列表</span>
          <el-button type="primary" @click="$router.push('/instances/create')">
            <el-icon><Plus /></el-icon>新建实例
          </el-button>
        </div>
      </template>

      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="配置类型">
          <el-select v-model="searchForm.config_type" placeholder="全部类型" clearable>
            <el-option
              v-for="type in configTypes"
              :key="type.name"
              :label="type.title"
              :value="type.name"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="格式">
          <el-select v-model="searchForm.format" placeholder="全部格式" clearable>
            <el-option label="JSON" value="json" />
            <el-option label="TOML" value="toml" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <!-- 智能权限控制 - 按钮文字即权限标识 -->
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="success" @click="handleExport">导出</el-button>
          <el-button type="warning" @click="handleImport">导入</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="instances" v-loading="loading" stripe>
        <el-table-column prop="name" label="实例名称" width="150" />
        <el-table-column prop="config_type_title" label="配置类型" width="150" />
        <el-table-column prop="format" label="格式" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.format === 'json' ? 'success' : 'warning'">
              {{ scope.row.format.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="viewInstance(scope.row)">查看</el-button>
            <el-button link type="primary" @click="editInstance(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="deleteInstance(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="loadInstances"
        @current-change="loadInstances"
        style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>

    <!-- 日志面板 -->
    <el-card class="log-panel" :body-style="{ padding: '10px' }">
      <template #header>
        <div class="log-header">
          <span>操作日志</span>
          <el-button link type="primary" @click="clearLogs">清空</el-button>
        </div>
      </template>
      <div class="log-content" ref="logContainer">
        <div 
          v-for="(log, index) in logs" 
          :key="index" 
          :class="['log-item', log.type]"
        >
          <span class="log-time">{{ log.time }}</span>
          <span class="log-type">[{{ log.type.toUpperCase() }}]</span>
          <span class="log-message">{{ log.message }}</span>
        </div>
        <div v-if="logs.length === 0" class="log-empty">暂无日志</div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { configInstanceApi, configTypeApi } from '../api/config'
import { usePermissionStore } from '../stores/permission'

const router = useRouter()
const permissionStore = usePermissionStore()
const instances = ref([])
const configTypes = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const logs = ref([])
const logContainer = ref(null)

const searchForm = ref({
  config_type: '',
  format: ''
})

// 添加日志
const addLog = (type, message) => {
  const time = new Date().toLocaleTimeString()
  logs.value.push({ time, type, message })
  // 限制日志数量
  if (logs.value.length > 50) {
    logs.value.shift()
  }
  // 滚动到底部
  nextTick(() => {
    if (logContainer.value) {
      logContainer.value.scrollTop = logContainer.value.scrollHeight
    }
  })
}

// 清空日志
const clearLogs = () => {
  logs.value = []
}

// 检查权限并记录日志
const handleSearch = () => {
  addLog('info', '点击搜索按钮')
  loadInstances()
}

const handleReset = () => {
  addLog('info', '点击重置按钮')
  resetSearch()
}

const loadInstances = async () => {
  loading.value = true
  addLog('info', `开始加载配置实例列表 - 页码: ${page.value}, 每页: ${pageSize.value}`)
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      ...searchForm.value
    }
    const res = await configInstanceApi.list(params)
    instances.value = res.data.results || []
    total.value = res.data.count || 0
    addLog('success', `加载成功 - 共 ${total.value} 条记录`)
  } catch (error) {
    addLog('error', `加载配置实例失败: ${error.message || '未知错误'}`)
    ElMessage.error('加载配置实例失败')
  } finally {
    loading.value = false
  }
}

const loadConfigTypes = async () => {
  try {
    const res = await configTypeApi.list()
    configTypes.value = res.data.results || []
    addLog('info', `加载配置类型成功 - 共 ${configTypes.value.length} 种类型`)
  } catch (error) {
    addLog('error', `加载配置类型失败: ${error.message || '未知错误'}`)
    console.error('加载配置类型失败:', error)
  }
}

const resetSearch = () => {
  searchForm.value = { config_type: '', format: '' }
  addLog('info', '重置搜索条件')
  loadInstances()
}

const handleExport = () => {
  addLog('info', '点击导出按钮')
  ElMessage.success('导出功能')
}

const handleImport = () => {
  addLog('info', '点击导入按钮')
  ElMessage.success('导入功能')
}

const viewInstance = (row) => {
  addLog('info', `查看实例: ${row.name}`)
  router.push(`/instances/edit/${row.id}`)
}

const editInstance = (row) => {
  addLog('info', `编辑实例: ${row.name}`)
  router.push(`/instances/edit/${row.id}`)
}

const deleteInstance = async (row) => {
  addLog('info', `尝试删除实例: ${row.name}`)
  try {
    await ElMessageBox.confirm('确定要删除该配置实例吗？', '提示', {
      type: 'warning'
    })
    await configInstanceApi.delete(row.id)
    addLog('success', `删除成功: ${row.name}`)
    ElMessage.success('删除成功')
    loadInstances()
  } catch (error) {
    if (error !== 'cancel') {
      addLog('error', `删除失败: ${error.message || '未知错误'}`)
      ElMessage.error('删除失败')
    } else {
      addLog('info', '取消删除操作')
    }
  }
}

onMounted(() => {
  addLog('info', '页面加载完成')
  addLog('info', `当前用户权限状态 - 搜索: ${permissionStore.hasPermission('配置实例.搜索')}, 重置: ${permissionStore.hasPermission('配置实例.重置')}`)
  loadInstances()
  loadConfigTypes()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.log-panel {
  margin-top: 20px;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-content {
  max-height: 200px;
  overflow-y: auto;
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 10px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
}

.log-item {
  padding: 4px 0;
  border-bottom: 1px solid #ebeef5;
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: #909399;
  margin-right: 8px;
}

.log-type {
  font-weight: bold;
  margin-right: 8px;
}

.log-item.info .log-type {
  color: #409eff;
}

.log-item.success .log-type {
  color: #67c23a;
}

.log-item.error .log-type {
  color: #f56c6c;
}

.log-item.warning .log-type {
  color: #e6a23c;
}

.log-message {
  color: #303133;
}

.log-empty {
  text-align: center;
  color: #909399;
  padding: 20px;
}
</style>
