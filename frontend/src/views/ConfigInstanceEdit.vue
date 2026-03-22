<template>
  <div class="config-instance-edit">
    <el-card>
      <template #header>
        <span>{{ isEdit ? '编辑配置实例' : '新建配置实例' }}</span>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="配置类型" prop="config_type">
          <!-- 编辑模式下显示文本，新建模式下显示下拉框 -->
          <el-input v-if="isEdit" :model-value="configTypeDisplay" disabled />
          <el-select v-else v-model="form.config_type" placeholder="选择配置类型" @change="onConfigTypeChange">
            <el-option
              v-for="type in configTypes"
              :key="type.name"
              :label="`${type.title} (${type.name})`"
              :value="type.name"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="实例名称" prop="name">
          <el-input v-model="form.name" :disabled="isEdit" placeholder="如: production_db" />
        </el-form-item>

        <el-form-item label="格式" prop="format">
          <el-radio-group v-model="form.format" @change="onFormatChange">
            <el-radio value="json">JSON</el-radio>
            <el-radio value="toml">TOML</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="配置内容" prop="content_text" class="content-editor">
          <!-- JSON 格式：显示表单编辑和代码编辑选项 -->
          <template v-if="form.format === 'json'">
            <el-radio-group v-model="jsonEditMode" size="small" style="margin-bottom: 10px;">
              <el-radio-button value="form" v-if="hasSchema">表单编辑</el-radio-button>
              <el-radio-button value="code">代码编辑</el-radio-button>
            </el-radio-group>
            
            <div class="editor-wrapper">
              <!-- JSON 表单编辑 -->
              <JsonSchemaEditor
                v-if="jsonEditMode === 'form' && hasSchema"
                ref="schemaEditor"
                v-model="parsedContent"
                :schema="currentSchema"
                @change="onSchemaChange"
              />
              <!-- JSON 代码编辑 -->
              <CodeEditor
                v-else
                v-model="form.content_text"
                language="json"
                @change="onCodeChange"
              />
            </div>
          </template>
          
          <!-- TOML 格式：只显示代码编辑 -->
          <template v-else>
            <CodeEditor
              v-model="form.content_text"
              language="toml"
              @change="onCodeChange"
            />
          </template>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm" :loading="saving">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import JsonSchemaEditor from '../components/JsonSchemaEditor.vue'
import CodeEditor from '../components/CodeEditor.vue'
import { configInstanceApi, configTypeApi } from '../api/config'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const saving = ref(false)
const configTypes = ref([])
const jsonEditMode = ref('code') // 'form' 或 'code'
const schemaEditor = ref(null)
const parsedContent = ref({})
const currentSchema = ref({})

const isEdit = computed(() => !!route.params.id)

const hasSchema = computed(() => {
  return currentSchema.value && Object.keys(currentSchema.value).length > 0
})

// 当前配置类型的显示文本（标题 + name）
const configTypeDisplay = computed(() => {
  if (!form.value.config_type) return ''
  const type = configTypes.value.find(t => t.name === form.value.config_type)
  if (type) {
    return `${type.title} (${type.name})`
  }
  return form.value.config_type
})

const form = ref({
  config_type: '',
  config_type_id: null,  // 配置类型的 ID，用于提交
  name: '',
  format: 'json',
  content_text: '',
  content: ''  // 用于提交给后端的字段
})

const rules = {
  config_type: [{ required: true, message: '请选择配置类型', trigger: 'change' }],
  name: [{ required: true, message: '请输入实例名称', trigger: 'blur' }],
  format: [{ required: true, message: '请选择格式', trigger: 'change' }],
  content_text: [{ required: true, message: '请输入配置内容', trigger: 'blur' }]
}

// 当格式改变时
const onFormatChange = (format) => {
  if (format === 'json' && hasSchema.value) {
    jsonEditMode.value = 'form'
  } else {
    jsonEditMode.value = 'code'
  }
}

// 当配置类型改变时，加载对应的 schema
const onConfigTypeChange = async (typeName) => {
  // 确保配置类型列表已加载
  if (configTypes.value.length === 0) {
    try {
      const res = await configTypeApi.list()
      configTypes.value = res.data.results || []
    } catch (error) {
      console.error('加载配置类型失败:', error)
      return
    }
  }
  
  const selectedType = configTypes.value.find(t => t.name === typeName)
  if (selectedType) {
    // 保存配置类型的 ID 用于提交
    form.value.config_type_id = selectedType.id
    
    if (selectedType.schema && Object.keys(selectedType.schema).length > 0) {
      currentSchema.value = selectedType.schema
      // 如果是 JSON 格式，默认使用表单编辑
      if (form.value.format === 'json') {
        jsonEditMode.value = 'form'
      }
      // 初始化空对象
      if (!form.value.content_text || form.value.content_text === '{}') {
        parsedContent.value = {}
      }
    } else {
      currentSchema.value = {}
      jsonEditMode.value = 'code'
    }
  }
}

// 当表单编辑器内容改变时
const onSchemaChange = (value) => {
  parsedContent.value = value
  // 同步到代码编辑器和提交字段
  try {
    const jsonStr = JSON.stringify(value, null, 2)
    form.value.content_text = jsonStr
    form.value.content = jsonStr
  } catch (e) {
    console.error('转换 JSON 失败:', e)
  }
}

// 当代码编辑器内容改变时
const onCodeChange = () => {
  // 同步 content 字段用于提交
  form.value.content = form.value.content_text
  try {
    const parsed = JSON.parse(form.value.content_text)
    parsedContent.value = parsed
  } catch (e) {
    // JSON 格式错误，不更新表单编辑器
  }
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  // 确保 content 字段有值
  form.value.content = form.value.content_text

  // 验证 JSON/TOML 格式
  try {
    if (form.value.format === 'json') {
      JSON.parse(form.value.content_text)
    }
  } catch (e) {
    ElMessage.error('JSON 格式错误: ' + e.message)
    return
  }

  // 构建提交数据，只包含后端需要的字段
  const submitData = {
    config_type: form.value.config_type_id || form.value.config_type,
    name: form.value.name,
    format: form.value.format,
    content: form.value.content_text
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await configInstanceApi.update(route.params.id, submitData)
      ElMessage.success('更新成功')
    } else {
      await configInstanceApi.create(submitData)
      ElMessage.success('创建成功')
    }
    router.push('/instances')
  } catch (error) {
    console.error('保存失败:', error.response?.data)
    ElMessage.error(error.response?.data?.detail || JSON.stringify(error.response?.data) || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  // 先加载配置类型列表
  try {
    const res = await configTypeApi.list()
    configTypes.value = res.data.results || []
  } catch (error) {
    console.error('加载配置类型失败:', error)
  }

  if (isEdit.value) {
    try {
      const res = await configInstanceApi.get(route.params.id)
      form.value = { ...res.data }
      // 设置 config_type_id 用于提交（后端返回的是 ID）
      form.value.config_type_id = res.data.config_type
      // 将 config_type 转换为 name（用于显示）
      const selectedType = configTypes.value.find(t => t.id === res.data.config_type)
      if (selectedType) {
        form.value.config_type = selectedType.name
      }
      // 解析内容
      try {
        parsedContent.value = JSON.parse(res.data.content_text || '{}')
      } catch (e) {
        parsedContent.value = {}
      }
      // 如果有配置类型，加载 schema
      if (selectedType) {
        if (selectedType.schema && Object.keys(selectedType.schema).length > 0) {
          currentSchema.value = selectedType.schema
          // 根据格式设置编辑模式
          if (form.value.format === 'json') {
            jsonEditMode.value = 'form'
          }
        }
      }
    } catch (error) {
      ElMessage.error('加载配置实例失败')
    }
  } else {
    // 默认内容模板
    form.value.content_text = '{}'
    parsedContent.value = {}
  }
})
</script>

<style scoped>
.config-instance-edit {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.content-editor :deep(.el-form-item__content) {
  width: 100%;
}

.editor-wrapper {
  width: 100%;
  min-height: 500px;
}
</style>
