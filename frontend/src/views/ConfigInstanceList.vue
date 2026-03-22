<template>
  <div class="config-instance-list">
    <!-- Search Panel -->
    <div class="sf-panel search-panel">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Search /></el-icon>
        <span>Search Filters</span>
      </div>
      <div class="sf-panel-content">
        <el-row :gutter="20" align="middle">
          <el-col :span="6">
            <div class="filter-item">
              <label class="data-label">Config Type</label>
              <select v-model="searchForm.config_type" class="sf-input">
                <option value="">All Types</option>
                <option v-for="type in configTypes" :key="type.name" :value="type.name">
                  {{ type.title }}
                </option>
              </select>
            </div>
          </el-col>
          <el-col :span="4">
            <div class="filter-item">
              <label class="data-label">Format</label>
              <select v-model="searchForm.format" class="sf-input">
                <option value="">All</option>
                <option value="json">JSON</option>
                <option value="toml">TOML</option>
              </select>
            </div>
          </el-col>
          <el-col :span="8">
            <div class="filter-item">
              <label class="data-label">Search</label>
              <input 
                v-model="searchForm.search" 
                placeholder="Config name..."
                class="sf-input font-tech-mono"
              />
            </div>
          </el-col>
          <el-col :span="6">
            <div class="filter-actions">
              <button class="sf-button primary" @click="loadInstances">
                <el-icon><Search /></el-icon>
                <span>Search</span>
              </button>
              <button class="sf-button" @click="$router.push('/instances/create')" style="margin-left: 10px;">
                <el-icon><Plus /></el-icon>
                <span>New</span>
              </button>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>

    <!-- Results Panel -->
    <div class="sf-panel results-panel" style="margin-top: 20px;">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Files /></el-icon>
        <span>Config Instances</span>
        <span class="count-badge font-tech-mono">{{ total }} items</span>
      </div>
      <div class="sf-panel-content">
        <table class="sf-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Format</th>
              <th>Version</th>
              <th>Updated</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody v-if="!loading">
            <tr v-for="instance in instances" :key="instance.id" class="slide-in">
              <td class="font-tech-mono">{{ instance.name }}</td>
              <td>{{ instance.config_type_title }}</td>
              <td>
                <span class="sf-tag" :class="instance.format">
                  {{ instance.format.toUpperCase() }}
                </span>
              </td>
              <td class="font-tech-mono">
                <span class="version-badge">v{{ instance.version }}</span>
              </td>
              <td class="font-tech-mono text-dimmed">{{ formatDate(instance.updated_at) }}</td>
              <td>
                <button class="sf-button" style="padding: 6px 12px; font-size: 10px;" @click="editInstance(instance)">
                  EDIT
                </button>
                <button class="sf-button" style="padding: 6px 12px; font-size: 10px; margin-left: 6px; border-color: var(--neon-magenta); color: var(--neon-magenta);" @click="viewVersions(instance)">
                  VER
                </button>
                <button class="sf-button danger" style="padding: 6px 12px; font-size: 10px; margin-left: 6px;" @click="deleteInstance(instance)">
                  DEL
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Loading State -->
        <div v-if="loading" class="loading-state">
          <div class="data-label">Loading instances...</div>
          <div class="sf-progress" style="margin-top: 15px;">
            <div class="sf-progress-bar" style="width: 70%;"></div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!loading && instances.length === 0" class="empty-state">
          <el-icon :size="48" class="text-dimmed"><Files /></el-icon>
          <div class="data-label" style="margin-top: 15px;">No instances found</div>
          <button class="sf-button primary" style="margin-top: 20px;" @click="$router.push('/instances/create')">
            Create First Instance
          </button>
        </div>

        <!-- Pagination -->
        <div v-if="total > pageSize" class="pagination">
          <button 
            class="sf-button" 
            :disabled="page === 1"
            @click="page--; loadInstances()"
            style="padding: 6px 12px;"
          >
            &lt; Prev
          </button>
          <span class="page-info font-tech-mono">
            Page {{ page }} of {{ Math.ceil(total / pageSize) }}
          </span>
          <button 
            class="sf-button" 
            :disabled="page >= Math.ceil(total / pageSize)"
            @click="page++; loadInstances()"
            style="padding: 6px 12px;"
          >
            Next &gt;
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
import { Plus, Files, Search } from '@element-plus/icons-vue'
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
    ElMessage.error('Failed to load instances')
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
  ElMessage.info(`Version history for "${row.name}"`)
}

const deleteInstance = async (row) => {
  try {
    await ElMessageBox.confirm(
      `Delete config instance "${row.name}"?`,
      'Confirm Delete',
      { 
        type: 'warning',
        confirmButtonText: 'Delete',
        cancelButtonText: 'Cancel'
      }
    )
    await configInstanceApi.delete(row.id)
    ElMessage.success('Deleted successfully')
    loadInstances()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Delete failed')
    }
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString()
}

onMounted(() => {
  loadInstances()
  loadConfigTypes()
})
</script>

<style scoped>
@import '../styles/sci-fi-theme.css';

.search-panel .filter-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.search-panel .filter-item label {
  margin-bottom: 0;
}

.filter-actions {
  display: flex;
  align-items: flex-end;
  height: 100%;
  padding-bottom: 0;
}

.results-panel .count-badge {
  margin-left: auto;
  padding: 4px 12px;
  background: rgba(0, 240, 255, 0.1);
  border: 1px solid var(--border-dimmed);
  border-radius: 4px;
  font-size: 12px;
  color: var(--neon-cyan);
}

.version-badge {
  padding: 2px 8px;
  background: rgba(0, 240, 255, 0.1);
  border-radius: 2px;
  font-size: 11px;
}

.loading-state, .empty-state {
  padding: 40px;
  text-align: center;
}

.text-dimmed {
  color: var(--text-dimmed);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid var(--border-subtle);
}

.page-info {
  color: var(--text-secondary);
  font-size: 12px;
}
</style>
