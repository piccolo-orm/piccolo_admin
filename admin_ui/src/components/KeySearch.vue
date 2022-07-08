<template>
    <div class="key_search">
        <input
            autocomplete="off"
            :placeholder="isFilter ? 'All' : 'None'"
            type="text"
            v-model="selectedValue"
            v-on:focus="showModal = true"
            v-on:keydown.enter.prevent
        />

        <input
            :value="hiddenSelectedValue"
            type="hidden"
            v-bind:name="fieldName"
        />

        <KeySearchModal
            v-show="showModal"
            :isFilter="isFilter"
            :tableName="tableName"
            @close="showModal = false"
            @update="handleUpdate($event)"
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
        },
        isNullable: {
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
    methods: {
        handleUpdate(event) {
            this.selectedValue = event.readable
            this.hiddenSelectedValue = event.id
            this.showModal = false
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
