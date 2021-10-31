<template>
    <select v-bind:name="fieldName">
        <option v-bind:selected="value == 'all'" v-if="isFilter" value="all">
            All
        </option>
        <option v-bind:selected="value == null" v-if="isNullable" value="null">
            Null
        </option>
        <option
            v-for="(item, key) in choices"
            :key="key"
            :selected="value == item.value"
            :value="item.value"
        >
            {{ item.display_name }}
        </option>
    </select>
</template>

<script lang="ts">
import Vue, { PropType } from "vue"
import { Choices } from "../interfaces"

export default Vue.extend({
    props: {
        fieldName: {
            type: String,
            default: ""
        },
        value: {
            type: undefined,
            default: undefined
        },
        choices: {
            type: Object as PropType<Choices>,
            default: () => {
                return {}
            }
        },
        isNullable: {
            type: Boolean,
            default: false
        },
        isFilter: {
            type: Boolean,
            default: false
        }
    },
    mounted() {
        if (this.isFilter) {
            this.value = "all"
        }
    }
})
</script>

<style>
</style>
