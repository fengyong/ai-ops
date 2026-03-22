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
          <el-button type="primary" @click="loadInstances">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
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
  format: ''
})

const loadInstances = async () => {
  loading.value = true
  try {
    const params = {
      page: page.value,
      page_size: pageSize.value,
      ...searchForm.value
    }
    const res = await configInstanceApi.list(params)
    instances.value = res.data.results || []
    total.value = res.data.count || 0
  } catch (error) {
    ElMessage.error('加载配置实例失败')
  } finally {
    loading.value = false
  }
}

const loadConfigTypes = async () => {
  try {
    const res = await configTypeApi.list()
    configTypes.value = res.data.results || []
  } catch (error) {
    console.error('加载配置类型失败:', error)
  }
}

const resetSearch = () => {
  searchForm.value = { config_type: '', format: '' }
  loadInstances()
}

const viewInstance = (row) => {
  router.push(`/instances/edit/${row.id}`)
}

const editInstance = (row) => {
  router.push(`/instances/edit/${row.id}`)
}

const deleteInstance = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该配置实例吗？', '提示', {
      type: 'warning'
    })
    await configInstanceApi.delete(row.id)
    ElMessage.success('删除成功')
    loadInstances()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
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
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}
</style>
