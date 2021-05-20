<template>
    <Modal v-on:close="$emit('close')">
        <h1>Add User</h1>

        <form v-if="schema" v-on:submit.prevent="submitForm($event)">
            <RowFormSelect v-bind:row="{}" v-bind:schema="schema" />
            <button>Create</button>
        </form>
    </Modal>
</template>

<script>
import RowFormSelect from "./RowFormSelect.vue"
import Modal from "./Modal.vue"

export default {
    components: {
        RowFormSelect,
        Modal,
    },
    computed: {
        schema() {
            return this.$store.state.userManagement.userSchema
        },
    },
    methods: {
        async submitForm(event) {},
    },
    async mounted() {
        if (!this.schema) {
            await this.$store.dispatch("userManagement/fetchUserSchema")
        }
    },
}
</script>

<style>
</style>
