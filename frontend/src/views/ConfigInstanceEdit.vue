<template>
  <div class="config-instance-edit">
    <el-card>
      <template #header>
        <span>{{ isEdit ? '编辑配置实例' : '新建配置实例' }}</span>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="配置类型" prop="config_type">
          <el-select v-model="form.config_type" :disabled="isEdit" @change="onTypeChange">
            <el-option
              v-for="type in configTypes"
              :key="type.name"
              :label="type.title"
              :value="type.name"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="配置名称" prop="name">
          <el-input v-model="form.name" :disabled="isEdit" placeholder="如: production_db" />
        </el-form-item>

        <el-form-item label="格式" prop="format">
          <el-radio-group v-model="form.format" :disabled="!selectedType">
            <el-radio-button label="json">JSON</el-radio-button>
            <el-radio-button label="toml">TOML</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="配置内容" prop="content" v-if="selectedType">
          <div class="content-editor">
            <el-tabs v-model="editMode">
              <el-tab-pane label="代码编辑" name="code">
                <el-input
                  v-model="contentText"
                  type="textarea"
                  :rows="20"
                  :placeholder="contentPlaceholder"
                />
              </el-tab-pane>
              <el-tab-pane label="表单编辑" name="form" v-if="form.format === 'json'">
                <div class="form-editor">
                  <p class="form-hint">基于 JSON Schema 的表单编辑（需要安装 @lljj/vue-json-schema-form）</p>
                  <el-input
                    v-model="contentText"
                    type="textarea"
                    :rows="15"
                    placeholder="暂使用代码编辑模式"
                  />
                </div>
              </el-tab-pane>
            </el-tabs>
            <div v-if="contentError" class="content-error">{{ contentError }}</div>
          </div>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submit" :loading="saving">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
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
  config_type: [{ required: true, message: '请选择配置类型', trigger: 'change' }],
  name: [{ required: true, message: '请输入配置名称', trigger: 'blur' }],
  format: [{ required: true, message: '请选择格式', trigger: 'change' }]
}

const onTypeChange = (typeName) => {
  const type = configTypes.value.find(t => t.name === typeName)
  if (type) {
    form.value.format = type.format
    // 根据 schema 生成示例内容
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
  // 简单的 TOML 生成
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
    } else {
      // TOML 验证会在后端进行
    }
    form.value.content = contentText.value
    contentError.value = ''
    return true
  } catch (e) {
    contentError.value = '格式错误: ' + e.message
    return false
  }
}

const submit = async () => {
  if (!validateContent()) {
    ElMessage.error('请修正内容格式错误')
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
    ElMessage.success('保存成功')
    router.push('/instances')
  } catch (error) {
    const msg = error.response?.data?.error || error.response?.data?.detail || '保存失败'
    ElMessage.error(msg)
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  // 加载配置类型列表
  try {
    const res = await configTypeApi.list()
    configTypes.value = res.data.results || res.data
  } catch (error) {
    ElMessage.error('加载配置类型失败')
  }

  // 如果是编辑模式，加载配置实例
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
      ElMessage.error('加载配置实例失败')
    }
  }
})
</script>

<style scoped>
.content-editor {
  width: 100%;
}

.form-editor {
  padding: 20px;
  background: #f5f7fa;
  border-radius: 4px;
}

.form-hint {
  color: #909399;
  margin-bottom: 10px;
}

.content-error {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}
</style>
