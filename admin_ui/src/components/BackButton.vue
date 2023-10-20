<template>
    <p>
        <a href="#" v-if="showBackButton" v-on:click.prevent="$router.go(-1)">
            <font-awesome-icon icon="angle-left" />{{ $t("Back") }}
        </a>
    </p>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    computed: {
        showBackButton() {
            return window.history.length > 1
        }
    }
})
</script>

<style scoped lang="less">
a {
    text-decoration: none;
    transform: translateX(0);

    svg {
        transition: 0.5s transform;
    }

    &:hover {
        svg {
            transform: translateX(-0.2rem);
            transition: 0.5s transform;
        }
    }
}
</style>
