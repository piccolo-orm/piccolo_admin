<template>
    <select v-bind:name="fieldName" v-model="localValue">
        <option
            v-bind:selected="value == 'all'"
            v-if="isFilter && !isArray"
            value="all"
        >
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
import { type PropType, defineComponent } from "vue"
import type { Choices } from "../interfaces"

export default defineComponent({
    props: {
        fieldName: {
            type: String as PropType<string>,
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
            type: Boolean as PropType<boolean>,
            default: false
        },
        isFilter: {
            type: Boolean as PropType<boolean>,
            default: false
        },
        isArray: {
            type: Boolean as PropType<boolean>,
            default: false
        }
    },
    data() {
        return {
            localValue: undefined as string | number | undefined
        }
    },
    emits: ["updated"],
    mounted() {
        if (this.isFilter) {
            this.localValue = "all"
        } else if (this.value !== undefined) {
            this.localValue = this.value
        }
    },
    watch: {
        value(newValue) {
            this.localValue = newValue
        },
        localValue(newValue) {
            this.$emit("updated", newValue)
        }
    }
})
</script>

<style></style>
