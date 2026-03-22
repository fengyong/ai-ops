<template>
  <div class="config-type-edit">
    <el-card>
      <template #header>
        <span>{{ isEdit ? '编辑配置类型' : '新建配置类型' }}</span>
      </template>

      <el-form :model="form" :rules="rules" ref="formRef" label-width="120px">
        <el-form-item label="类型标识" prop="name">
          <el-input v-model="form.name" :disabled="isEdit" placeholder="如: database_config" />
        </el-form-item>

        <el-form-item label="显示名称" prop="title">
          <el-input v-model="form.title" placeholder="如: 数据库配置" />
        </el-form-item>

        <el-form-item label="格式" prop="format">
          <el-radio-group v-model="form.format">
            <el-radio value="json">JSON</el-radio>
            <el-radio value="toml">TOML</el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="描述">
          <el-input v-model="form.description" type="textarea" rows="3" placeholder="可选描述" />
        </el-form-item>

        <el-form-item label="JSON Schema" prop="schema">
          <el-tabs v-model="editMode">
            <el-tab-pane label="表单编辑" name="form">
              <JsonSchemaEditor
                ref="schemaEditor"
                v-model="form.schema"
                :schema="jsonSchemaMetaSchema"
                @change="onSchemaChange"
              />
            </el-tab-pane>
            <el-tab-pane label="代码编辑" name="code">
              <CodeEditor
                v-model="schemaText"
                language="json"
                @change="onCodeChange"
              />
            </el-tab-pane>
          </el-tabs>
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
import { configTypeApi } from '../api/config'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const saving = ref(false)
const schemaText = ref('')
const editMode = ref('form')
const schemaEditor = ref(null)

const isEdit = computed(() => !!route.params.name)

const form = ref({
  name: '',
  title: '',
  format: 'json',
  description: '',
  schema: {
    type: 'object',
    properties: {}
  }
})

// JSON Schema 的元 Schema（用于编辑 Schema 本身）
const jsonSchemaMetaSchema = {
  type: 'object',
  title: 'JSON Schema',
  properties: {
    type: {
      type: 'string',
      title: '类型',
      enum: ['object', 'array', 'string', 'number', 'integer', 'boolean'],
      default: 'object'
    },
    title: {
      type: 'string',
      title: '标题'
    },
    description: {
      type: 'string',
      title: '描述'
    },
    properties: {
      type: 'object',
      title: '属性定义',
      format: 'table'
    },
    required: {
      type: 'array',
      title: '必填字段',
      items: {
        type: 'string'
      }
    }
  }
}

const rules = {
  name: [
    { required: true, message: '请输入类型标识', trigger: 'blur' },
    { pattern: /^[a-z][a-z0-9_]*$/, message: '只能包含小写字母、数字和下划线', trigger: 'blur' }
  ],
  title: [{ required: true, message: '请输入显示名称', trigger: 'blur' }],
  format: [{ required: true, message: '请选择格式', trigger: 'change' }]
}

// 当表单编辑器内容改变时
const onSchemaChange = (value) => {
  form.value.schema = value
  // 同步到代码编辑器
  try {
    schemaText.value = JSON.stringify(value, null, 2)
  } catch (e) {
    console.error('转换 JSON 失败:', e)
  }
}

// 当代码编辑器内容改变时
const onCodeChange = () => {
  try {
    const parsed = JSON.parse(schemaText.value)
    form.value.schema = parsed
  } catch (e) {
    // JSON 格式错误，不更新表单编辑器
  }
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  // 验证 Schema 是否为有效 JSON
  try {
    JSON.stringify(form.value.schema)
  } catch (e) {
    ElMessage.error('JSON Schema 格式错误')
    return
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await configTypeApi.update(route.params.name, form.value)
      ElMessage.success('更新成功')
    } else {
      await configTypeApi.create(form.value)
      ElMessage.success('创建成功')
    }
    router.push('/types')
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

onMounted(async () => {
  if (isEdit.value) {
    try {
      const res = await configTypeApi.get(route.params.name)
      form.value = { ...res.data }
      schemaText.value = JSON.stringify(res.data.schema || {}, null, 2)
    } catch (error) {
      ElMessage.error('加载配置类型失败')
    }
  } else {
    // 默认 Schema 模板
    form.value.schema = {
      type: 'object',
      properties: {
        example: { type: 'string', title: '示例字段' }
      }
    }
    schemaText.value = JSON.stringify(form.value.schema, null, 2)
  }
})
</script>

<style scoped>
.config-type-edit {
  max-width: 900px;
  margin: 0 auto;
}
</style>
