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

/* 应用类似 audio_ops 项目的样式 */
:deep(.je-object__container) {
  border: 1px solid #3883fa;
  border-radius: 4px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fff;
  box-shadow: 2px 2px 12px rgba(128, 128, 128, 0.3);
}

:deep(.je-object__title) {
  font-weight: bold;
  color: #3883fa;
  margin-bottom: 10px;
  font-size: 11pt;
  font-family: arial, sans-serif;
}

:deep(.form-control) {
  border: 1px solid #d3d3d3;
  border-radius: 3px;
  padding: 4px;
  min-height: 32px;
  font-size: 10pt;
  width: 100%;
  box-sizing: border-box;
  font-family: "dejavu sans mono", "droid sans mono", consolas, monaco, "lucida console", "courier new", courier, monospace, sans-serif;
  color: #1A1A1A;
  background-color: #fff;
}

:deep(.form-control:focus) {
  outline: none;
  border-color: #3883fa;
  box-shadow: 0 0 5px rgba(56, 131, 250, 0.3);
}

/* 表格模式样式 */
:deep(.je-table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 15px;
  border: 1px solid #d3d3d3;
}

:deep(.je-table th),
:deep(.je-table td) {
  padding: 5px 10px;
  border: 1px solid #d3d3d3;
  text-align: left;
  box-sizing: border-box;
  font-size: 10pt;
}

:deep(.je-table th) {
  background-color: #f5f5f5;
  font-weight: bold;
  color: #4d4d4d;
}

:deep(.je-table tr:hover td) {
  background-color: #f5f5f5;
}

/* Tab 模式样式 */
:deep(.je-tabs) {
  margin-bottom: 15px;
}

:deep(.je-tabs-content) {
  padding: 15px;
  border: 1px solid #d3d3d3;
  border-top: none;
  border-radius: 0 0 4px 4px;
  background-color: #fff;
}

:deep(.je-tab) {
  padding: 4px 10px;
  background-color: #f5f5f5;
  border: 1px solid #d3d3d3;
  border-bottom: none;
  cursor: pointer;
  color: #4d4d4d;
  font-size: 10pt;
  font-family: arial, sans-serif;
}

:deep(.je-tab.active) {
  background-color: white;
  border-bottom: 1px solid white;
  margin-bottom: -1px;
  color: #3883fa;
  font-weight: bold;
}

:deep(.je-header) {
  background-color: #3883fa;
  padding: 0 10px;
  border-radius: 4px 4px 0 0;
  margin-bottom: 0;
  color: white;
  font-family: arial, sans-serif;
  font-size: 11pt;
  line-height: 30px;
}

:deep(.je-btn) {
  background-color: #f5f5f5;
  color: #4d4d4d;
  border: 1px solid #d3d3d3;
  padding: 4px 20px;
  border-radius: 3px;
  cursor: pointer;
  margin-right: 8px;
  font-size: 10pt;
  font-family: arial, sans-serif;
  transition: all 0.3s ease;
}

:deep(.je-btn:hover) {
  background-color: #e5e5e5;
}

:deep(.je-btn-group) {
  margin-bottom: 10px;
}

/* 修复 theme management 中的表格样式 */
:deep(.je-table-container) {
  overflow-x: auto;
}

:deep(.je-object-properties) {
  margin-top: 10px;
}

:deep(.je-property-key) {
  font-weight: normal;
  color: #4d4d4d;
  margin-bottom: 5px;
  font-size: 10pt;
}

:deep(.je-property-value) {
  margin-bottom: 15px;
}

/* 修复日期选择器样式 */
:deep(.je-datetime) {
  width: 100%;
}

:deep(.je-datetime input) {
  width: 100%;
  border: 1px solid #d3d3d3;
  border-radius: 3px;
  padding: 4px;
  font-size: 10pt;
  background-color: #fff;
  color: #4d4d4d;
}

:deep(.je-datetime input:focus) {
  outline: none;
  border-color: #3883fa;
  box-shadow: 0 0 5px rgba(56, 131, 250, 0.3);
}

/* 高亮样式 */
:deep(.je-highlight) {
  background-color: #FFFFAB;
  border: 1px solid yellow;
  border-radius: 2px;
}

/* 字符串值样式 */
:deep(.jsoneditor-value.jsoneditor-string) {
  color: #008000;
}

/* 数字值样式 */
:deep(.jsoneditor-value.jsoneditor-number) {
  color: #ee422e;
}

/* 布尔值样式 */
:deep(.jsoneditor-value.jsoneditor-boolean) {
  color: #ff8c00;
}

/* null值样式 */
:deep(.jsoneditor-value.jsoneditor-null) {
  color: #004ED0;
}

/* 选中的行 */
:deep(tr.jsoneditor-highlight),
:deep(tr.jsoneditor-selected) {
  background-color: #d3d3d3;
}

/* 错误提示样式 */
:deep(.jsoneditor-schema-error) {
  cursor: default;
  display: inline-block;
  height: 24px;
  line-height: 24px;
  position: relative;
  text-align: center;
  width: 24px;
  color: #ee422e;
}
</style>
