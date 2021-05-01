<template>
    <Modal v-on:close="$emit('close')">
        <h1>Change password</h1>

        <form>
            <input type="password" placeholder="Password"></input>
            <input type="password" placeholder="Confirm password"></input>
            <button>Submit</button>
        </form>
    </Modal>
</template>

<script lang="ts">
import Modal from "./Modal.vue"
import AddRowForm from "./AddRowForm.vue"

export default {
    props: {},
    components: {
        Modal,
    },
}
</script>

<style scoped lang="less">
</style>
