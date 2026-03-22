<template>
  <div class="config-type-list">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>配置类型列表</span>
          <el-button type="primary" @click="$router.push('/types/create')">
            <el-icon><Plus /></el-icon>新建类型
          </el-button>
        </div>
      </template>

      <el-table :data="types" v-loading="loading" stripe>
        <el-table-column prop="name" label="类型标识" width="150" />
        <el-table-column prop="title" label="显示名称" width="200" />
        <el-table-column prop="format" label="格式" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.format === 'json' ? 'success' : 'warning'">
              {{ scope.row.format.toUpperCase() }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="instance_count" label="实例数" width="100" />
        <el-table-column prop="updated_at" label="更新时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button link type="primary" @click="editType(scope.row)">编辑</el-button>
            <el-button link type="danger" @click="deleteType(scope.row)">删除</el-button>
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
    types.value = res.data.results || res.data || []
  } catch (error) {
    ElMessage.error('加载配置类型失败')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const editType = (row) => {
  router.push(`/types/edit/${row.name}`)
}

const deleteType = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该配置类型吗？', '提示', {
      type: 'warning'
    })
    await configTypeApi.delete(row.name)
    ElMessage.success('删除成功')
    loadTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
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
