<template>
  <div class="config-type-edit">
    <div class="sf-panel">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Edit /></el-icon>
        <span>{{ isEdit ? 'Edit Config Type' : 'New Config Type' }}</span>
      </div>
      <div class="sf-panel-content">
        <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Type ID" prop="name">
                <input 
                  v-model="form.name" 
                  :disabled="isEdit" 
                  placeholder="e.g. database_config"
                  class="sf-input font-tech-mono"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Display Name" prop="title">
                <input 
                  v-model="form.title" 
                  placeholder="e.g. Database Configuration"
                  class="sf-input"
                />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="Format" prop="format">
            <div class="format-selector">
              <div 
                v-for="fmt in ['json', 'toml']" 
                :key="fmt"
                class="format-option"
                :class="{ active: form.format === fmt }"
                @click="form.format = fmt"
              >
                <span class="sf-tag" :class="fmt">{{ fmt.toUpperCase() }}</span>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="Description" prop="description">
            <textarea 
              v-model="form.description" 
              rows="3"
              class="sf-input"
              placeholder="Describe this configuration type..."
            ></textarea>
          </el-form-item>

          <el-form-item label="JSON Schema" prop="schema">
            <div class="schema-editor">
              <div class="schema-info">
                <el-icon><InfoFilled /></el-icon>
                <span>Define the structure for auto-generated forms</span>
              </div>
              <textarea
                v-model="schemaText"
                rows="15"
                @blur="validateSchema"
                class="sf-input font-tech-mono"
                style="font-size: 12px;"
              ></textarea>
              <div v-if="schemaError" class="schema-error">
                <el-icon><Warning /></el-icon>
                {{ schemaError }}
              </div>
            </div>
          </el-form-item>

          <el-form-item>
            <button 
              class="sf-button primary" 
              @click="submit" 
              :disabled="saving"
              style="min-width: 120px;"
            >
              <span v-if="saving">Saving...</span>
              <span v-else>{{ isEdit ? 'Update' : 'Create' }}</span>
            </button>
            <button 
              class="sf-button" 
              @click="$router.back()"
              style="margin-left: 10px;"
            >
              Cancel
            </button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Edit, InfoFilled, Warning } from '@element-plus/icons-vue'
import { configTypeApi } from '../api/config'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const saving = ref(false)
const schemaText = ref('')
const schemaError = ref('')

const isEdit = computed(() => !!route.params.name)

const form = ref({
  name: '',
  title: '',
  format: 'json',
  description: '',
  schema: {}
})

const defaultSchema = {
  type: 'object',
  title: 'Configuration',
  properties: {
    name: {
      type: 'string',
      title: 'Name'
    },
    enabled: {
      type: 'boolean',
      title: 'Enabled',
      default: true
    }
  }
}

const rules = {
  name: [
    { required: true, message: 'Please enter type ID', trigger: 'blur' },
    { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: 'Must start with letter, alphanumeric only', trigger: 'blur' }
  ],
  title: [{ required: true, message: 'Please enter display name', trigger: 'blur' }],
  format: [{ required: true, message: 'Please select format', trigger: 'change' }]
}

watch(() => form.value.schema, (newVal) => {
  if (typeof newVal === 'object') {
    schemaText.value = JSON.stringify(newVal, null, 2)
  }
}, { immediate: true })

const validateSchema = () => {
  try {
    const parsed = JSON.parse(schemaText.value)
    form.value.schema = parsed
    schemaError.value = ''
    return true
  } catch (e) {
    schemaError.value = 'JSON Error: ' + e.message
    return false
  }
}

const submit = async () => {
  if (!validateSchema()) {
    ElMessage.error('Please fix schema errors')
    return
  }

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    if (isEdit.value) {
      await configTypeApi.update(route.params.name, form.value)
    } else {
      await configTypeApi.create(form.value)
    }
    ElMessage.success(isEdit.value ? 'Updated successfully' : 'Created successfully')
    router.push('/types')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'Save failed')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const res = await configTypeApi.get(route.params.name)
      form.value = res.data
    } catch (error) {
      ElMessage.error('Failed to load config type')
    }
  } else {
    form.value.schema = defaultSchema
    schemaText.value = JSON.stringify(defaultSchema, null, 2)
  }
})
</script>

<style scoped>
@import '../styles/sci-fi-theme.css';

.format-selector {
  display: flex;
  gap: 15px;
}

.format-option {
  padding: 10px 20px;
  border: 1px solid var(--border-dimmed);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.format-option:hover {
  border-color: var(--neon-cyan);
  background: rgba(0, 240, 255, 0.05);
}

.format-option.active {
  border-color: var(--neon-cyan);
  background: rgba(0, 240, 255, 0.1);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
}

.schema-editor {
  width: 100%;
}

.schema-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 15px;
  background: rgba(0, 240, 255, 0.05);
  border: 1px solid var(--border-subtle);
  border-radius: 4px;
  margin-bottom: 10px;
  color: var(--text-secondary);
  font-size: 12px;
}

.schema-error {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 10px;
  padding: 10px 15px;
  background: rgba(255, 0, 68, 0.1);
  border: 1px solid var(--neon-red);
  border-radius: 4px;
  color: var(--neon-red);
  font-size: 12px;
}

:deep(.el-form-item__label) {
  color: var(--neon-cyan);
  font-family: 'Orbitron', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 8px;
}
</style>
