<template>
  <div class="code-editor-wrapper">
    <div ref="editorContainer" class="editor-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import { EditorView, basicSetup } from 'codemirror'
import { EditorState } from '@codemirror/state'
import { json } from '@codemirror/lang-json'
import { javascript } from '@codemirror/lang-javascript'
import { oneDark } from '@codemirror/theme-one-dark'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'json', // json, toml, yaml
    validator: (value) => ['json', 'toml', 'yaml', 'javascript'].includes(value)
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'change'])

const editorContainer = ref(null)
const editorView = ref(null)

// 根据语言获取扩展
const getLanguageExtension = (lang) => {
  switch (lang) {
    case 'json':
      return json()
    case 'toml':
    case 'yaml':
    case 'javascript':
    default:
      return javascript()
  }
}

// 自动检测语言
const detectLanguage = (content) => {
  if (!content) return 'json'
  const trimmed = content.trim()
  
  // 检测 TOML
  if (trimmed.includes('=') && trimmed.includes('[') && !trimmed.startsWith('{')) {
    return 'toml'
  }
  
  // 检测 JSON
  if (trimmed.startsWith('{') || trimmed.startsWith('[')) {
    return 'json'
  }
  
  return 'json'
}

const currentLanguage = computed(() => {
  return props.language === 'auto' ? detectLanguage(props.modelValue) : props.language
})

const createEditorState = (content) => {
  return EditorState.create({
    doc: content,
    extensions: [
      basicSetup,
      getLanguageExtension(currentLanguage.value),
      oneDark,
      EditorView.theme({
        '&': {
          fontSize: '14px',
          minHeight: '500px',
          maxHeight: '800px'
        },
        '.cm-content': {
          fontFamily: '"Consolas", "Monaco", "Courier New", monospace',
          minHeight: '500px'
        },
        '.cm-gutters': {
          backgroundColor: '#1e1e1e',
          borderRight: '1px solid #333'
        }
      }),
      EditorView.updateListener.of((update) => {
        if (update.docChanged) {
          const newValue = update.state.doc.toString()
          emit('update:modelValue', newValue)
          emit('change', newValue)
        }
      }),
      EditorView.editable.of(!props.readonly)
    ]
  })
}

const initEditor = () => {
  if (!editorContainer.value) return

  editorView.value = new EditorView({
    state: createEditorState(props.modelValue),
    parent: editorContainer.value
  })
}

const destroyEditor = () => {
  if (editorView.value) {
    editorView.value.destroy()
    editorView.value = null
  }
}

// 监听内容变化（外部更新）
watch(() => props.modelValue, (newValue) => {
  if (editorView.value) {
    const currentContent = editorView.value.state.doc.toString()
    if (newValue !== currentContent) {
      editorView.value.dispatch({
        changes: {
          from: 0,
          to: currentContent.length,
          insert: newValue
        }
      })
    }
  }
})

// 监听语言变化
watch(() => props.language, () => {
  if (editorView.value) {
    const currentContent = editorView.value.state.doc.toString()
    destroyEditor()
    initEditor()
    // 恢复内容
    editorView.value.dispatch({
      changes: {
        from: 0,
        to: editorView.value.state.doc.length,
        insert: currentContent
      }
    })
  }
})

onMounted(() => {
  initEditor()
})

onUnmounted(() => {
  destroyEditor()
})

// 暴露方法
defineExpose({
  getValue: () => editorView.value?.state.doc.toString(),
  setValue: (value) => {
    if (editorView.value) {
      editorView.value.dispatch({
        changes: {
          from: 0,
          to: editorView.value.state.doc.length,
          insert: value
        }
      })
    }
  },
  getLanguage: () => currentLanguage.value
})
</script>

<style scoped>
.code-editor-wrapper {
  width: 100%;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.editor-container {
  width: 100%;
  min-height: 500px;
  max-height: 800px;
}

.editor-container :deep(.cm-editor) {
  min-height: 500px;
}

.editor-container :deep(.cm-scroller) {
  min-height: 500px;
}
</style>
