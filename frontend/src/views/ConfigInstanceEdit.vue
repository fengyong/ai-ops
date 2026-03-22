<template>
  <div class="config-instance-edit">
    <div class="sf-panel">
      <div class="corner-br"></div>
      <div class="sf-panel-header">
        <el-icon><Edit /></el-icon>
        <span>{{ isEdit ? 'Edit Config Instance' : 'New Config Instance' }}</span>
        <span v-if="selectedType" class="type-badge sf-tag" :class="form.format">
          {{ selectedType.title }}
        </span>
      </div>
      <div class="sf-panel-content">
        <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="Config Type" prop="config_type">
                <select 
                  v-model="form.config_type" 
                  :disabled="isEdit" 
                  @change="onTypeChange"
                  class="sf-input"
                >
                  <option value="">Select Type</option>
                  <option v-for="type in configTypes" :key="type.name" :value="type.name">
                    {{ type.title }}
                  </option>
                </select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="Instance Name" prop="name">
                <input 
                  v-model="form.name" 
                  :disabled="isEdit" 
                  placeholder="e.g. production_db"
                  class="sf-input font-tech-mono"
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
                :class="{ active: form.format === fmt, disabled: !selectedType }"
                @click="selectedType && (form.format = fmt)"
              >
                <span class="sf-tag" :class="fmt">{{ fmt.toUpperCase() }}</span>
              </div>
            </div>
          </el-form-item>

          <el-form-item label="Configuration Content" prop="content" v-if="selectedType">
            <div class="content-editor">
              <div class="editor-tabs">
                <div 
                  class="editor-tab" 
                  :class="{ active: editMode === 'code' }"
                  @click="editMode = 'code'"
                >
                  <el-icon><Code /></el-icon>
                  <span>Code Editor</span>
                </div>
                <div 
                  v-if="form.format === 'json'"
                  class="editor-tab" 
                  :class="{ active: editMode === 'form' }"
                  @click="editMode = 'form'"
                >
                  <el-icon><Grid /></el-icon>
                  <span>Form View</span>
                </div>
              </div>
              
              <div class="editor-content">
                <textarea
                  v-show="editMode === 'code'"
                  v-model="contentText"
                  rows="20"
                  :placeholder="contentPlaceholder"
                  class="sf-input font-tech-mono code-editor"
                  @blur="validateContent"
                ></textarea>
                
                <div v-show="editMode === 'form'" class="form-view">
                  <div class="form-hint">
                    <el-icon><InfoFilled /></el-icon>
                    <span>Form view based on JSON Schema (coming soon)</span>
                  </div>
                </div>
              </div>
              
              <div v-if="contentError" class="content-error">
                <el-icon><Warning /></el-icon>
                {{ contentError }}
              </div>
            </div>
          </el-form-item>

          <el-form-item v-if="!selectedType">
            <div class="select-type-hint">
              <el-icon :size="32" class="text-dimmed"><ArrowUp /></el-icon>
              <div class="data-label">Please select a config type first</div>
            </div>
          </el-form-item>

          <el-form-item>
            <button 
              class="sf-button primary" 
              @click="submit" 
              :disabled="saving || !selectedType"
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Edit, Code, Grid, InfoFilled, Warning, ArrowUp } from '@element-plus/icons-vue'
import { configInstanceApi, configTypeApi } from '../api/config'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const saving = ref(false)
const configTypes = ref([])
const contentText = ref('')
const contentError = ref('')
const editMode = ref('code')

const isEdit = computed(() => !!route.params.id)

const form = ref({
  config_type: '',
  name: '',
  format: 'json',
  content: ''
})

const selectedType = computed(() => {
  return configTypes.value.find(t => t.name === form.value.config_type)
})

const contentPlaceholder = computed(() => {
  if (form.value.format === 'json') {
    return '{\n  "key": "value"\n}'
  }
  return '[section]\nkey = "value"'
})

const rules = {
  config_type: [{ required: true, message: 'Please select config type', trigger: 'change' }],
  name: [{ required: true, message: 'Please enter instance name', trigger: 'blur' }],
  format: [{ required: true, message: 'Please select format', trigger: 'change' }]
}

const onTypeChange = (typeName) => {
  const type = configTypes.value.find(t => t.name === typeName)
  if (type) {
    form.value.format = type.format
    contentText.value = generateExample(type.schema, type.format)
  }
}

const generateExample = (schema, format) => {
  const example = {}
  if (schema && schema.properties) {
    for (const [key, prop] of Object.entries(schema.properties)) {
      if (prop.default !== undefined) {
        example[key] = prop.default
      } else if (prop.type === 'string') {
        example[key] = ''
      } else if (prop.type === 'number') {
        example[key] = 0
      } else if (prop.type === 'boolean') {
        example[key] = false
      }
    }
  }
  
  if (format === 'json') {
    return JSON.stringify(example, null, 2)
  }
  return Object.entries(example)
    .map(([k, v]) => {
      if (typeof v === 'string') return `${k} = "${v}"`
      return `${k} = ${v}`
    })
    .join('\n')
}

const validateContent = () => {
  try {
    if (form.value.format === 'json') {
      JSON.parse(contentText.value)
    }
    form.value.content = contentText.value
    contentError.value = ''
    return true
  } catch (e) {
    contentError.value = 'Format error: ' + e.message
    return false
  }
}

const submit = async () => {
  if (!validateContent()) {
    ElMessage.error('Please fix content errors')
    return
  }

  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    if (isEdit.value) {
      await configInstanceApi.update(route.params.id, form.value)
    } else {
      await configInstanceApi.create(form.value)
    }
    ElMessage.success(isEdit.value ? 'Updated successfully' : 'Created successfully')
    router.push('/instances')
  } catch (error) {
    const msg = error.response?.data?.error || error.response?.data?.detail || 'Save failed'
    ElMessage.error(msg)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  try {
    const res = await configTypeApi.list()
    configTypes.value = res.data.results || res.data
  } catch (error) {
    ElMessage.error('Failed to load config types')
  }

  if (isEdit.value) {
    try {
      const res = await configInstanceApi.get(route.params.id)
      const data = res.data
      form.value = {
        config_type: data.config_type,
        name: data.name,
        format: data.format,
        content: data.content_text
      }
      contentText.value = data.content_text
    } catch (error) {
      ElMessage.error('Failed to load config instance')
    }
  }
})
</script>

<style scoped>
@import '../styles/sci-fi-theme.css';

.type-badge {
  margin-left: auto;
}

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

.format-option:hover:not(.disabled) {
  border-color: var(--neon-cyan);
  background: rgba(0, 240, 255, 0.05);
}

.format-option.active {
  border-color: var(--neon-cyan);
  background: rgba(0, 240, 255, 0.1);
  box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
}

.format-option.disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.content-editor {
  border: 1px solid var(--border-dimmed);
  border-radius: 4px;
  overflow: hidden;
}

.editor-tabs {
  display: flex;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid var(--border-dimmed);
}

.editor-tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  cursor: pointer;
  color: var(--text-dimmed);
  font-family: 'Orbitron', sans-serif;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: all 0.3s ease;
  border-bottom: 2px solid transparent;
}

.editor-tab:hover {
  color: var(--text-primary);
  background: rgba(0, 240, 255, 0.05);
}

.editor-tab.active {
  color: var(--neon-cyan);
  border-bottom-color: var(--neon-cyan);
  background: rgba(0, 240, 255, 0.1);
}

.editor-content {
  padding: 15px;
  background: rgba(10, 10, 15, 0.5);
}

.code-editor {
  font-size: 13px;
  line-height: 1.6;
  resize: vertical;
}

.form-view {
  padding: 40px;
  text-align: center;
}

.form-hint {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: var(--text-dimmed);
  font-size: 12px;
}

.content-error {
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

.select-type-hint {
  padding: 40px;
  text-align: center;
  border: 1px dashed var(--border-dimmed);
  border-radius: 4px;
}

.text-dimmed {
  color: var(--text-dimmed);
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
