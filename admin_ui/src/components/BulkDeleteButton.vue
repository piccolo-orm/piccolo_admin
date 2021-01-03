<template>
    <a
        class="button"
        href="#"
        selected="selected"
        title="Delete selected Rows"
        v-on:click.prevent="$emit('triggered')"
    >
        <span>
            <font-awesome-icon icon="trash-alt" />
            Delete {{ selected }} result(s)
        </span>
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