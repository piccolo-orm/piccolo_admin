<template>
    <a
        class="button"
        href="#"
        title="Delete selected Rows"
        v-on:click.prevent="$emit('triggered')"
    >
        <font-awesome-icon icon="trash-alt" />
        <span>{{ $t("Delete") }} {{ selected }} {{ $t("rows") }}</span>
    </a>
</template>

<script lang="ts">
import { defineComponent } from "vue"

export default defineComponent({
    props: {
        selected: {
            type: Number,
            default: 0
        }
    }
})
</script>
