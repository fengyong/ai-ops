import { usePermissionStore } from '@/stores/permission'

let permissionStoreInstance = null

export function setPermissionStore(store) {
  permissionStoreInstance = store
}

function getPermissionStore() {
  if (permissionStoreInstance) {
    return permissionStoreInstance
  }
  try {
    return usePermissionStore()
  } catch (e) {
    console.warn('[权限拦截] 无法获取 permission store:', e)
    return null
  }
}

function getTextContent(vnode) {
  if (!vnode) return ''
  if (typeof vnode === 'string') return vnode.trim()
  if (typeof vnode.children === 'string') return vnode.children.trim()
  if (Array.isArray(vnode.children)) {
    return vnode.children.map(getTextContent).filter(Boolean).join('').trim()
  }
  // 处理 slot 对象形式：{ default: () => [...] }
  if (vnode.children && typeof vnode.children === 'object') {
    const defaultSlot = vnode.children.default?.()
    if (Array.isArray(defaultSlot)) {
      return defaultSlot.map(getTextContent).filter(Boolean).join('').trim()
    }
  }
  return ''
}

function inferPermissionName(vnode, route) {
  const routePermission = route.meta?.permission
  if (!routePermission) return null

  const buttonText = getTextContent(vnode)
  if (!buttonText) return null

  // 去掉括号内容和空格，提取核心动词
  const coreAction = buttonText
    .replace(/[（(].*?[）)]/g, '')
    .replace(/\s+/g, '')
    .trim()

  return coreAction ? `${routePermission}.${coreAction}` : null
}

function processChildren(vnode, component) {
  if (!vnode.children) return vnode

  // 数组形式
  if (Array.isArray(vnode.children)) {
    const processed = vnode.children
      .map(child => processVNodePermission(child, component))
      .filter(Boolean)
    if (processed.length !== vnode.children.length) {
      return { ...vnode, children: processed }
    }
    return vnode
  }

  // slot 对象形式：{ default: () => [...] }
  if (typeof vnode.children === 'object') {
    const originalDefault = vnode.children.default
    if (typeof originalDefault === 'function') {
      return {
        ...vnode,
        children: {
          ...vnode.children,
          default: (...args) => {
            const nodes = originalDefault(...args)
            if (!Array.isArray(nodes)) return nodes
            return nodes
              .map(child => processVNodePermission(child, component))
              .filter(Boolean)
          }
        }
      }
    }
  }

  return vnode
}

export function processVNodePermission(vnode, component) {
  if (!vnode) return vnode

  const route = component.$route
  if (!route) return vnode

  const componentName = vnode.type?.name || vnode.type?.__name
  const isButton = componentName === 'ElButton' ||
                   componentName === 'el-button' ||
                   componentName === 'Button' ||
                   vnode.type === 'button'

  if (!isButton) {
    return processChildren(vnode, component)
  }

  const permissionName = inferPermissionName(vnode, route)
  if (!permissionName) return vnode

  const permissionStore = getPermissionStore()
  if (!permissionStore) {
    console.warn('[权限拦截] permission store 未初始化，默认显示按钮')
    return vnode
  }

  return permissionStore.hasPermission(permissionName) ? vnode : null
}
