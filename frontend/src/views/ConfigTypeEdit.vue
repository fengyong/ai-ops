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
            <el-radio-button label="json">JSON</el-radio-button>
            <el-radio-button label="toml">TOML</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>

        <el-form-item label="JSON Schema" prop="schema">
          <div class="schema-editor">
            <el-alert
              title="定义配置的结构，用于自动生成表单"
              type="info"
              :closable="false"
              style="margin-bottom: 10px"
            />
            <el-input
              v-model="schemaText"
              type="textarea"
              :rows="15"
              @blur="validateSchema"
            />
            <div v-if="schemaError" class="schema-error">{{ schemaError }}</div>
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
  title: '配置',
  properties: {
    name: {
      type: 'string',
      title: '名称'
    },
    enabled: {
      type: 'boolean',
      title: '启用'
    }
  }
}

const rules = {
  name: [
    { required: true, message: '请输入类型标识', trigger: 'blur' },
    { pattern: /^[a-zA-Z][a-zA-Z0-9_]*$/, message: '只能包含字母、数字和下划线，且以字母开头', trigger: 'blur' }
  ],
  title: [{ required: true, message: '请输入显示名称', trigger: 'blur' }],
  format: [{ required: true, message: '请选择格式', trigger: 'change' }]
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
    schemaError.value = 'JSON 格式错误: ' + e.message
    return false
  }
}

const submit = async () => {
  if (!validateSchema()) {
    ElMessage.error('请修正 Schema 错误')
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
    ElMessage.success('保存成功')
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
      form.value = res.data
    } catch (error) {
      ElMessage.error('加载配置类型失败')
    }
  } else {
    form.value.schema = defaultSchema
    schemaText.value = JSON.stringify(defaultSchema, null, 2)
  }
})
</script>

<style scoped>
.schema-editor {
  width: 100%;
}

.schema-error {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 5px;
}
</style>
