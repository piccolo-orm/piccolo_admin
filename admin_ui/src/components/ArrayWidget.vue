<template>
    <div>
        <input
            v-for="(value, index) in internalArray"
            :key="index"
            :value="value"
            v-on:change="updateArray($event, index)"
        />
        <button v-on:click.prevent="addArrayElement">Add</button>
    </div>
</template>

<script>
export default {
    props: {
        array: {
            type: Array,
            default: () => [],
        },
    },
    data() {
        return {
            internalArray: [],
        }
    },
    methods: {
        updateArray($event, index) {
            this.$set(this.internalArray, index, $event.target.value)
            this.$emit("updateArray", this.internalArray)
        },
        addArrayElement() {
            this.internalArray = [...this.internalArray, ""]
        },
    },
    watch: {
        array() {
            this.internalArray = [...this.array]
        },
    },
    mounted() {
        this.internalArray = [...this.array]
    },
}
</script>

<style>
</style>
