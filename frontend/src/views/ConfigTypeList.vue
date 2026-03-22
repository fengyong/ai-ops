<template>
  <div class="config-type-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配置类型管理</span>
          <el-button type="primary" @click="$router.push('/types/create')">
            <el-icon><Plus /></el-icon> 新建类型
          </el-button>
        </div>
      </template>

      <el-table :data="types" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="类型标识" width="150" />
        <el-table-column prop="title" label="显示名称" width="180" />
        <el-table-column prop="format" label="格式" width="100">
          <template #default="{ row }">
            <el-tag :type="row.format === 'json' ? 'success' : 'warning'">
              {{ row.format.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="instance_count" label="实例数" width="100" />
        <el-table-column prop="description" label="描述" show-overflow-tooltip />
        <el-table-column prop="updated_at" label="更新时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.updated_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="editType(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteType(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { configTypeApi } from '../api/config'

const router = useRouter()
const types = ref([])
const loading = ref(false)

const loadTypes = async () => {
  loading.value = true
  try {
    const res = await configTypeApi.list()
    types.value = res.data.results || res.data
  } catch (error) {
    ElMessage.error('加载配置类型失败')
  } finally {
    loading.value = false
  }
}

const editType = (row) => {
  router.push(`/types/edit/${row.name}`)
}

const deleteType = async (row) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除配置类型 "${row.title}" 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    await configTypeApi.delete(row.name)
    ElMessage.success('删除成功')
    loadTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}

onMounted(loadTypes)
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
