<template>
    <li class="group">
        <a
            href="#"
            class="subtle"
            @click.prevent="$emit('toggled')"
            title="Click to toggle children."
        >
            <font-awesome-icon icon="layer-group" />
            <span class="name">{{ name }}</span>
            <span class="ellipsis" v-if="collapsed">...</span>
        </a>
    </li>
</template>

<script setup lang="ts">
import type { PropType } from "vue"

defineProps({
    name: {
        type: String as PropType<string>,
        required: true
    },
    collapsed: {
        type: Boolean as PropType<boolean>,
        required: true
    }
})

defineEmits(["toggled"])
</script>

<style scoped lang="less">
li.group {
    font-size: 0.7em;

    a {
        text-transform: uppercase;

        span {
            &.name {
                padding-left: 0;
            }

            &.ellipsis {
                flex-grow: 1;
                text-align: right;
            }
        }
    }
}
</style>
