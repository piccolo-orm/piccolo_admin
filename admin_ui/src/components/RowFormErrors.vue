<template>
    <div class="errors">
        <font-awesome-icon icon="exclamation-triangle" />
        <span>
            <b> {{ errors }}</b>
        </span>
    </div>
</template>

<script lang="ts">
import Vue from "vue"

export default Vue.extend({
    props: { errors: String }
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
