<template>
    <a
        class="button"
        href="#"
        title="Delete selected Rows"
        v-on:click.prevent="$emit('triggered')"
    >
        <font-awesome-icon icon="trash-alt" />
        <span>Delete {{ selected }} selected</span>
    </a>
</template>

<script>
export default {
    props: {
        selected: {
            type: Number,
            default: 0,
        },
    },
}
</script>