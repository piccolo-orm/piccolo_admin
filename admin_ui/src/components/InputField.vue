<template>
    <div>
        <label>{{ title }}</label>

        <input
            step="1"
            type="number"
            v-bind:name="title.toLowerCase()"
            v-bind:value="value"
            v-if="type == 'integer'"
            v-bind:placeholder="placeholder"
        />

        <template v-if="type == 'string'">
            <input
                autocomplete="off"
                class="datetime"
                type="text"
                v-bind:name="getFieldName(title)"
                v-bind:value="value"
                v-bind:placeholder="placeholder"
                v-if="format == 'date-time'"
            />
            <input
                type="text"
                v-bind:name="getFieldName(title)"
                v-bind:value="value"
                v-bind:placeholder="placeholder"
                v-else
            />
        </template>

        <div class="checkbox_wrapper" v-if="type == 'boolean'">
            <select v-bind:name="getFieldName(title)">
                <option value="all" v-bind:selected="value == 'all'" v-if="isFilter">All</option>
                <option value="null" v-bind:selected="value == null" v-if="isNullable">Null</option>
                <option value="true" v-bind:selected="value == true">True</option>
                <option value="false" v-bind:selected="value == false">False</option>
            </select>
        </div>
    </div>
</template>

<script lang="ts">
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
    computed: {
        placeholder() {
            return this.isFilter ? 'All' : ''
        }
    },
    methods: {
        getFieldName(name: string) {
            return name.toLowerCase().replace(' ', '_')
        },
    },
    mounted() {
        flatpickr(".datetime", { enableTime: true })
    }
}
</script>

<style scoped lang='less'>
div.checkbox_wrapper {
    input {
        width: 1rem !important;
    }
}
</style>
