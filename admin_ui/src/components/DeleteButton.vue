<template>
    <a
        href="#"
        id="delete"
        title="Delete Row"
        data-uitest="delete_row_button"
        v-on:click.prevent="$emit('triggered')"
    >
        <font-awesome-icon icon="trash-alt" />
        <span v-if="includeTitle">{{ $t("Delete") }}</span>
    </a>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    props: {
        includeTitle: {
            type: Boolean,
            default: false
        }
    }
})
</script>

<style scoped lang="less">
@import "../vars.less";

@keyframes shake {
    0% {
        transform: rotate(0deg);
    }
    50% {
        transform: rotate(-10deg);
    }
    100% {
        transform: rotate(10deg);
    }
}

a#delete {
    text-decoration: none;

    span {
        padding-left: 0.2rem;
    }

    &:hover {
        color: @red;

        svg {
            animation: shake 0.4s;
            animation-iteration-count: infinite;
        }
    }
}
</style>
