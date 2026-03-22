import { usePermissionStore } from '@/stores/permission'

// 权限存储实例（在应用初始化后设置）
let permissionStoreInstance = null

export function setPermissionStore(store) {
  permissionStoreInstance = store
}

function getPermissionStore() {
  // 优先使用已设置的实例，否则尝试从 Pinia 获取
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
  
  if (typeof vnode === 'string') {
    return vnode.trim()
  }
  
  if (typeof vnode.children === 'string') {
    return vnode.children.trim()
  }
  
  if (vnode.children && Array.isArray(vnode.children)) {
    return vnode.children
      .map(child => getTextContent(child))
      .filter(Boolean)
      .join('')
      .trim()
  }
  
  return ''
}

function inferPermissionName(vnode, route) {
  const routePermission = route.meta?.permission
  if (!routePermission) {
    console.log('[权限拦截] 路由没有设置 meta.permission:', route.path)
    return null
  }
  
  const buttonText = getTextContent(vnode)
  if (!buttonText) {
    console.log('[权限拦截] 按钮没有文本内容')
    return null
  }
  
  // 提取按钮文字中的核心动词（去掉括号内容和多余空格）
  const coreAction = buttonText
    .replace(/[（(].*?[）)]/g, '')  // 去掉括号内容
    .replace(/\s+/g, '')            // 去掉空格
    .trim()
  
  // 如果提取不到核心动词，返回 null
  if (!coreAction) {
    console.log('[权限拦截] 无法提取核心动词:', buttonText)
    return null
  }
  
  return `${routePermission}.${coreAction}`
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
  
  // 调试：记录所有组件
  if (componentName) {
    console.log('[权限拦截] 发现组件:', componentName)
  }
  
  if (!isButton) {
    // 递归处理子节点，但返回新的 vnode 而不是修改原 vnode
    if (vnode.children && Array.isArray(vnode.children)) {
      const processedChildren = vnode.children
        .map(child => processVNodePermission(child, component))
        .filter(Boolean)
      
      // 如果有子节点被过滤掉，创建新的 vnode
      if (processedChildren.length !== vnode.children.length) {
        return {
          ...vnode,
          children: processedChildren
        }
      }
    }
    return vnode
  }
  
  const buttonText = getTextContent(vnode)
  const permissionName = inferPermissionName(vnode, route)
  
  // 调试日志 - 记录所有按钮
  console.log('[权限拦截] 发现按钮:', {
    buttonText,
    permissionName,
    route: route.path,
    routePermission: route.meta?.permission,
    componentName,
    vnodeType: typeof vnode.type,
    vnodeTypeName: vnode.type?.name,
    children: vnode.children
  })
  
  if (!permissionName) {
    console.log('[权限拦截] 无法推断权限名，保留按钮:', buttonText)
    return vnode
  }
  
  const permissionStore = getPermissionStore()
  if (!permissionStore) {
    console.warn('[权限拦截] permission store 未初始化，默认显示按钮:', buttonText)
    return vnode
  }
  
  // 权限数据已加载，进行权限检查
  
  const hasPermission = permissionStore.hasPermission(permissionName)
  
  // 调试日志
  console.log('[权限拦截] 权限检查:', {
    buttonText,
    permissionName,
    hasPermission,
    missingPermissions: permissionStore.missingPermissions
  })
  
  if (!hasPermission) {
    console.log('[权限拦截] 隐藏按钮:', permissionName)
    return null
  }
  
  console.log('[权限拦截] 显示按钮:', permissionName)
  return vnode
}
