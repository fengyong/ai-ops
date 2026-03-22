<template>
  <div class="config-type-list">
    <div class="sf-panel">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Document /></el-icon>
        <span>Config Types</span>
        <button class="sf-button primary" @click="$router.push('/types/create')" style="margin-left: auto;">
          <el-icon><Plus /></el-icon>
          <span>New Type</span>
        </button>
      </div>
      <div class="sf-panel-content">
        <table class="sf-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Format</th>
              <th>Instances</th>
              <th>Description</th>
              <th>Updated</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody v-if="!loading">
            <tr v-for="type in types" :key="type.name" class="slide-in">
              <td class="font-tech-mono">{{ type.name }}</td>
              <td>{{ type.title }}</td>
              <td>
                <span class="sf-tag" :class="type.format">
                  {{ type.format.toUpperCase() }}
                </span>
              </td>
              <td class="font-tech-mono">{{ type.instance_count || 0 }}</td>
              <td class="text-dimmed">{{ type.description || '-' }}</td>
              <td class="font-tech-mono text-dimmed">{{ formatDate(type.updated_at) }}</td>
              <td>
                <button class="sf-button" style="padding: 6px 12px; font-size: 10px;" @click="editType(type)">
                  EDIT
                </button>
                <button class="sf-button danger" style="padding: 6px 12px; font-size: 10px; margin-left: 8px;" @click="deleteType(type)">
                  DEL
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        
        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="data-label">Loading data...</div>
          <div class="sf-progress" style="margin-top: 15px;">
            <div class="sf-progress-bar" style="width: 60%;"></div>
          </div>
        </div>
        
        <!-- Empty State -->
        <div v-if="!loading && types.length === 0" class="empty-state">
          <el-icon :size="48" class="text-dimmed"><Document /></el-icon>
          <div class="data-label" style="margin-top: 15px;">No config types found</div>
          <button class="sf-button primary" style="margin-top: 20px;" @click="$router.push('/types/create')">
            Create First Type
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Document } from '@element-plus/icons-vue'
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
    ElMessage.error('Failed to load config types')
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
      `Delete config type "${row.title}"?`,
      'Confirm Delete',
      { 
        type: 'warning',
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel'
      }
    )
    await configTypeApi.delete(row.name)
    ElMessage.success('Deleted successfully')
    loadTypes()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Delete failed')
    }
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

onMounted(loadTypes)
</script>

<style scoped>
@import '../styles/sci-fi-theme.css';

.sf-panel-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.loading-state {
  padding: 40px;
  text-align: center;
}

.empty-state {
  padding: 60px;
  text-align: center;
}

.text-dimmed {
  color: var(--text-dimmed);
}
</style>
