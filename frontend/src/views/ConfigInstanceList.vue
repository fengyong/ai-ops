<template>
  <div class="config-instance-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配置实例管理</span>
          <el-button type="primary" @click="$router.push('/instances/create')">
            <el-icon><Plus /></el-icon> 新建实例
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
        <el-form-item label="搜索">
          <el-input v-model="searchForm.search" placeholder="配置名称" clearable />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadInstances">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="instances" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="配置名称" width="180" />
        <el-table-column prop="config_type_title" label="配置类型" width="150" />
        <el-table-column prop="format" label="格式" width="100">
          <template #default="{ row }">
            <el-tag :type="row.format === 'json' ? 'success' : 'warning'">
              {{ row.format.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="version" label="版本" width="80" />
        <el-table-column prop="updated_at" label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editInstance(row)">编辑</el-button>
            <el-button size="small" type="info" @click="viewVersions(row)">版本</el-button>
            <el-button size="small" type="danger" @click="deleteInstance(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
        v-if="total > 0"
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="loadInstances"
        style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { configInstanceApi, configTypeApi } from '../api/config'

const router = useRouter()
const instances = ref([])
const configTypes = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)

const searchForm = ref({
  config_type: '',
  format: '',
  search: ''
})

const loadInstances = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      ...searchForm.value
    }
    const res = await configInstanceApi.list(params)
    instances.value = res.data.results || res.data
    total.value = res.data.count || instances.value.length
  } catch (error) {
    ElMessage.error('加载配置实例失败')
  } finally {
    loading.value = false
  }
}

const loadConfigTypes = async () => {
  try {
    const res = await configTypeApi.list()
    configTypes.value = res.data.results || res.data
  } catch (error) {
    console.error('Failed to load config types:', error)
  }
}

const editInstance = (row) => {
  router.push(`/instances/edit/${row.id}`)
}

const viewVersions = (row) => {
  // TODO: 打开版本历史对话框
  ElMessage.info(`查看 "${row.name}" 的版本历史`)
}

const deleteInstance = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除配置实例 "${row.name}" 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    await configInstanceApi.delete(row.id)
    ElMessage.success('删除成功')
    loadInstances()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

onMounted(() => {
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
}
</style>
