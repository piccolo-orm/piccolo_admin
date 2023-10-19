<template>
    <div class="errors">
        <p><font-awesome-icon icon="exclamation-triangle" />Error</p>
        <ul>
            <li v-for="error in errors" :key="error">{{ error }}</li>
        </ul>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from "vue"

export default defineComponent({
    props: {
        errors: {
            type: Array as PropType<string[]>,
            default: () => []
        }
    }
})
</script>

<style lang="less" scoped>
@import "../vars.less";

div.errors {
    @darkRed: darken(@red, 10%);
    background-color: fade(@red, 20%);
    color: @darkRed;
    border: 2px solid @darkRed;
    padding: 1rem;

    p {
        font-weight: bold;
        margin: 0 0 0.2rem;

        svg {
            margin-right: 0.1rem;
        }
    }

    ul {
        margin: 0;
        padding-left: 1.5rem;

        li {
            font-weight: bold;
        }
    }
}

.dark_mode {
    @lightRed: lighten(@red, 5%);
    div.errors {
        color: @lightRed;
        background: none;
        border-color: @lightRed;
    }
}
</style>
