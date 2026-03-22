import { usePermissionStore } from '@/stores/permission'

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
  if (!routePermission) return null
  
  const buttonText = getTextContent(vnode)
  if (!buttonText) return null
  
  return `${routePermission}.${buttonText}`
}

export function processVNodePermission(vnode, component) {
  if (!vnode) return vnode
  
  const route = component.$route
  if (!route) return vnode
  
  const componentName = vnode.type?.name || vnode.type?.__name
  const isButton = componentName === 'ElButton' || 
                   componentName === 'el-button' ||
                   vnode.type === 'button'
  
  if (!isButton) {
    if (vnode.children && Array.isArray(vnode.children)) {
      vnode.children = vnode.children
        .map(child => processVNodePermission(child, component))
        .filter(Boolean)
    }
    return vnode
  }
  
  const permissionName = inferPermissionName(vnode, route)
  
  if (!permissionName) {
    return vnode
  }
  
  const permissionStore = usePermissionStore()
  const hasPermission = permissionStore.hasPermission(permissionName)
  
  if (!hasPermission) {
    return null
  }
  
  return vnode
}
