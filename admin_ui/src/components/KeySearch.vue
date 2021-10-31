<template>
    <div class="key_search">
        <input
            autocomplete="off"
            :placeholder="isFilter ? 'All' : 'None'"
            type="text"
            v-model="selectedValue"
            v-on:focus="showModal = true"
            v-on:keydown.enter.prevent
            v-bind:name="fieldName"
        />

        <input
            :value="hiddenSelectedValue"
            type="hidden"
            v-bind:name="fieldName"
        />

        <KeySearchModal
            v-show="showModal"
            :tableName="tableName"
            @close="showModal = false"
        />
    </div>
</template>

<script lang="ts">
import KeySearchModal from "./KeySearchModal.vue"

export default {
    props: {
        fieldName: String,
        tableName: String,
        rowID: undefined,
        readable: undefined,
        isFilter: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            ids: [],
            selectedValue: undefined,
            hiddenSelectedValue: undefined,
            showModal: false
        }
    },
    components: {
        KeySearchModal
    },
    async mounted() {
        this.selectedValue = this.readable
        this.hiddenSelectedValue = this.rowID
    }
}
</script>
