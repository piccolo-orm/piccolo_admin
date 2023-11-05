interface State {
    showTimezoneModal: boolean
}

export default {
    state: {
        showTimezoneModal: false
    } as State,
    mutations: {
        updateShowTimezoneModal(state: State, value: boolean) {
            state.showTimezoneModal = value
        }
    }
}
