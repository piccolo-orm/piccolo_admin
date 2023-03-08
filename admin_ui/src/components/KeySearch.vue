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
            @update="
                handleUpdate($event)
                $emit('update', $event)
            "
        />
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"
import KeySearchModal from "./KeySearchModal.vue"

let persistedData = undefined

export default defineComponent({
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
            persistedData = event.readable
        }
    },
    components: {
        KeySearchModal
    },
    watch: {
        readable(newValue) {
            this.selectedValue = newValue
        },
        rowID(newValue) {
            this.hiddenSelectedValue = newValue
        }
    },
    async mounted() {
        this.selectedValue = persistedData
        this.hiddenSelectedValue = this.$route.query[this.fieldName]
    }
})
</script>
