<template>
    <a
        class="button"
        href="#"
        title="Update selected Rows"
        v-on:click.prevent="$emit('triggered')"
    >
        <font-awesome-icon icon="arrow-up" />
        <span>Update {{ selected }} rows</span>
    </a>
</template>

<script>
export default {
    props: {
        selected: {
            type: Number,
            default: 0
        }
    }
}
</script>