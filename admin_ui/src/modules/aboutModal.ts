interface State {
    showAboutModal: boolean
}

export default {
    state: {
        showAboutModal: false
    } as State,
    mutations: {
        updateShowAboutModal(state: State, value: boolean) {
            state.showAboutModal = value
        }
    }
}
