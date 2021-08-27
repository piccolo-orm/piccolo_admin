import Store from './store'

declare module '@vue/runtime-core' {
    interface ComponentCustomProperties {
        $store: typeof Store
    }
}