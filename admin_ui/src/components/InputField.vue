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

        <input
            type="text"
            v-bind:name="title.toLowerCase()"
            v-bind:value="value"
            v-if="type == 'string'"
        />

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

        <input
            type="text"
            v-bind:name="title.toLowerCase()"
            v-bind:value="value"
            v-if="type == 'date-time'"
        />
    </div>
</template>

<script>
export default {
    props: {
        title: String,
        type: String,
        value: undefined
    },
    methods: {
        valueChanged(event) {
            event.target.value = event.target.checked
        }
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
