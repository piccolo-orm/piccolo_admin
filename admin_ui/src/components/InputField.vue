<template>
    <div>
        <label>{{ title }}</label>

        <template v-if="type == 'integer'">
            <OperatorField :fieldName="title.toLowerCase()" />
            <input
                step="1"
                type="number"
                v-bind:name="title.toLowerCase()"
                v-bind:placeholder="placeholder"
                v-bind:value="value"
            />
        </template>

        <template v-if="type == 'string'">
            <template v-if="format == 'date-time'">
                <OperatorField :fieldName="title.toLowerCase()" />
                <input
                    autocomplete="off"
                    class="datetime"
                    type="text"
                    v-bind:name="getFieldName(title)"
                    v-bind:placeholder="placeholder"
                    v-bind:value="value"
                />
            </template>

            <input
                type="text"
                v-bind:name="getFieldName(title)"
                v-bind:placeholder="placeholder"
                v-bind:value="value"
                v-else
            />
        </template>

        <template v-if="type == 'boolean'">
            <select v-bind:name="getFieldName(title)">
                <option
                    v-bind:selected="value == 'all'"
                    v-if="isFilter"
                    value="all"
                >All</option>
                <option
                    v-bind:selected="value == null"
                    v-if="isNullable"
                    value="null"
                >Null</option>
                <option
                    v-bind:selected="value == true"
                    value="true"
                >True</option>
                <option
                    v-bind:selected="value == false"
                    value="false"
                >False</option>
            </select>
        </template>
    </div>
</template>

<script lang="ts">
import OperatorField from "./OperatorField.vue"
import flatpickr from "flatpickr"

export default {
    props: {
        title: String,
        type: String,
        value: undefined,
        format: String,
        isFilter: {
            type: Boolean,
            default: true
        },
        isNullable: {
            type: Boolean,
            default: false
        }
    },
    components: {
        OperatorField
    },
    computed: {
        placeholder() {
            return this.isFilter ? "All" : ""
        }
    },
    methods: {
        getFieldName(name: string) {
            return name.toLowerCase().replace(" ", "_")
        }
    },
    mounted() {
        flatpickr(".datetime", { enableTime: true })
    }
}
</script>
