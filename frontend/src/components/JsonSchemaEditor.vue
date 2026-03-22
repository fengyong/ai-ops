<template>
  <div class="json-schema-editor">
    <div ref="editorContainer" class="editor-container"></div>
    <div v-if="validationErrors.length > 0" class="validation-errors">
      <el-alert
        v-for="(error, index) in validationErrors"
        :key="index"
        :title="error.message"
        type="error"
        :closable="false"
        show-icon
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { JSONEditor } from '@json-editor/json-editor'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({})
  },
  schema: {
    type: Object,
    default: () => ({})
  },
  options: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'validate'])

const editorContainer = ref(null)
const editor = ref(null)
const validationErrors = ref([])

const initEditor = () => {
  if (!editorContainer.value) return

  const defaultOptions = {
    theme: 'bootstrap4',
    iconlib: 'fontawesome5',
    disable_collapse: false,
    disable_edit_json: false,
    disable_properties: false,
    disable_array_reorder: false,
    disable_array_delete: false,
    disable_array_add: false,
    collapsed: false,
    // 数组表格模式支持
    array_controls_top: true,
    // 确保表单有足够空间
    compact: false,
    ...props.options
  }

  editor.value = new JSONEditor(editorContainer.value, {
    schema: props.schema,
    startval: props.modelValue,
    ...defaultOptions
  })

  editor.value.on('ready', () => {
    console.log('JSON Editor ready')
  })

  editor.value.on('change', () => {
    const value = editor.value.getValue()
    const errors = editor.value.validate()
    validationErrors.value = errors
    emit('update:modelValue', value)
    emit('change', value, errors)
  })

  editor.value.on('validate', (errors) => {
    validationErrors.value = errors
    emit('validate', errors)
  })
}

const destroyEditor = () => {
  if (editor.value) {
    editor.value.destroy()
    editor.value = null
  }
}

// 监听 schema 变化
watch(() => props.schema, (newSchema) => {
  if (editor.value) {
    destroyEditor()
    initEditor()
  }
}, { deep: true })

// 监听 value 变化（外部更新）
watch(() => props.modelValue, (newValue) => {
  if (editor.value && JSON.stringify(newValue) !== JSON.stringify(editor.value.getValue())) {
    editor.value.setValue(newValue)
  }
}, { deep: true })

onMounted(() => {
  initEditor()
})

onUnmounted(() => {
  destroyEditor()
})

// 暴露方法给父组件
defineExpose({
  getValue: () => editor.value?.getValue(),
  setValue: (value) => editor.value?.setValue(value),
  validate: () => editor.value?.validate(),
  isValid: () => editor.value?.validate().length === 0
})
</script>

<style scoped>
.json-schema-editor {
  width: 100%;
}

.editor-container {
  width: 100%;
  min-height: 500px;
  max-height: 800px;
  overflow-y: auto;
}

:deep(.je-object__container) {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
}

:deep(.je-object__title) {
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 10px;
}

:deep(.form-control) {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 10px 14px;
  min-height: 42px;
  font-size: 14px;
  width: 100%;
}

/* 表格模式样式 */
:deep(.je-table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
}

:deep(.je-table th),
:deep(.je-table td) {
  padding: 12px;
  border: 1px solid #dcdfe6;
  text-align: left;
}

:deep(.je-table th) {
  background-color: #f5f7fa;
  font-weight: bold;
}

/* Tab 模式样式 */
:deep(.je-tabs) {
  margin-bottom: 15px;
}

:deep(.je-tabs-content) {
  padding: 15px;
  border: 1px solid #dcdfe6;
  border-top: none;
  border-radius: 0 0 4px 4px;
}

:deep(.je-tab) {
  padding: 10px 20px;
  background-color: #f5f7fa;
  border: 1px solid #dcdfe6;
  border-bottom: none;
  cursor: pointer;
}

:deep(.je-tab.active) {
  background-color: white;
  border-bottom: 1px solid white;
  margin-bottom: -1px;
}

:deep(.je-header) {
  background-color: #f5f7fa;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 12px;
}

:deep(.je-btn) {
  background-color: #409EFF;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 8px;
  font-size: 14px;
}

:deep(.je-btn:hover) {
  background-color: #66b1ff;
}

:deep(.je-btn-group) {
  margin-bottom: 10px;
}
</style>
