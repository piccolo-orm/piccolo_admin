<template>
    <div class="errors">
        <span>
            <font-awesome-icon icon="exclamation-triangle" />Error
            <ul>
                <li v-for="error in errors" :key="error">{{ error }}</li>
            </ul>
        </span>
    </div>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    props: {
        errors: {
            type: Array,
            default: () => []
        }
    }
})
</script>

<style lang="less" scoped>
@import "../vars.less";

div.errors {
    color: @red;
    border: 0.15em solid;
    padding: 1em;
}
</style>
