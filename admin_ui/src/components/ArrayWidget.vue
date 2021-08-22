<template>
    <div>
        <ul class="array_items">
            <li
                :key="index"
                v-for="(value, index) in internalArray"
            >
                <input
                    :type="inputType"
                    :value="value"
                    id="choice"
                    v-on:change="updateArray($event, index)"
                />
                <a
                    href="#"
                    v-if="value !== ''"
                    v-on:click.prevent="removeArrayElement(index)"
                >
                    <font-awesome-icon icon="times" />
                </a>
                <a
                    href="#"
                    v-else
                    v-on:click.prevent="removeArrayField(index)"
                >
                    <font-awesome-icon icon="times" />
                </a>
            </li>
            <li>
                <a
                    href="#"
                    v-on:click.prevent="addArrayElement"
                >
                    <font-awesome-icon icon="plus" />Add
                </a>
            </li>
        </ul>
    </div>
</template>

<script>
export default {
    props: {
        array: {
            type: Array,
            default: () => [],
        },
        inputType: {
            type: String,
            default: "text",
        },
    },
    data() {
        return {
            internalArray: [],
        }
    },
    methods: {
        updateArray($event, index) {
            Reflect.set(this.internalArray, index, $event.target.value)
            this.$emit("updateArray", this.internalArray)
        },
        addArrayElement() {
            this.internalArray = [...this.internalArray, ""]
            this.$emit("updateArray", this.internalArray)
        },
        removeArrayElement(index) {
            Reflect.deleteProperty(this.internalArray, index)
            this.$emit("updateArray", this.internalArray)
        },
        removeArrayField(index) {
            this.internalArray.splice(index, 1)
            this.$emit("updateArray", this.internalArray)
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

<style scoped lang="less">
ul.array_items {
    padding: 0;
    width: 100%;

    li {
        display: flex;
        flex-direction: row;
        list-style: none;
        margin-bottom: 0.8rem;
        align-items: center;

        a {
            text-decoration: none;
        }

        input {
            flex-grow: 1;
            margin-right: 0.5rem;
            margin-bottom: 0 !important;
        }
    }
}
</style>
