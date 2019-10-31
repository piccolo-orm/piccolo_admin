<template>
    <div>
        <label>{{ title }}</label>

        <input
            step="1"
            type="number"
            v-bind:name="title.toLowerCase()"
            v-bind:value="value"
            v-if="type == 'integer'"
        />

        <template v-if="type == 'string'">
            <input
                autocomplete="off"
                class="datetime"
                type="text"
                v-bind:name="title.toLowerCase()"
                v-bind:value="value"
                v-if="format == 'date-time'"
            />
            <input
                type="text"
                v-bind:name="title.toLowerCase()"
                v-bind:value="value"
                v-else
            />
        </template>

        <div class="checkbox_wrapper">
            <input
                type="checkbox"
                v-bind:checked="value"
                v-bind:name="title.toLowerCase()"
                v-bind:value="value"
                v-if="type == 'boolean'"
                v-on:change="valueChanged($event)"
            />
        </div>
    </div>
</template>

<script>
export default {
    props: {
        title: String,
        type: String,
        value: undefined,
        format: String
    },
    methods: {
        valueChanged(event) {
            event.target.value = event.target.checked
        }
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
