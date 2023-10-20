// We're currently using Vuex, which isn't the best for TypeScript support.
// These interfaces are used for now, to stop TypeScript from complaining.

export interface Context {
    commit: (mutation: string, value: any) => void
    dispatch: (actionName: string, arg?: any) => Promise<void>
}
