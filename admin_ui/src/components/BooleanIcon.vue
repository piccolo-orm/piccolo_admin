<template>
    <span class="boolean">
        <font-awesome-icon
            class="correct"
            icon="check"
            v-if="boolean === true"
        />
        <font-awesome-icon class="incorrect" icon="times" v-else />
    </span>
</template>

<script>
export default {
    props: {
        boolean: {
            type: Boolean,
            default: undefined,
        },
    },
}
</script>

<style lang="less">
@import "../vars.less";

svg.correct {
    color: @green;
}

svg.incorrect {
    color: @red;
}
</style>
