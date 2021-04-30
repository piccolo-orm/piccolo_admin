<template>
    <BaseView>
        <div class="users_lists">
            <TitleBar title="Users"></TitleBar>
            <div>Stuff</div>
        </div>
    </BaseView>
</template>


<script lang="ts">
import Vue from "vue"
import BaseView from "./BaseView.vue"
import TitleBar from "../components/TitleBar.vue"

export default Vue.extend({
    components: {
        BaseView,
        TitleBar,
    },
})
</script>


<style scoped lang="less">
div.users_lists {
    box-sizing: border-box;
    width: 100%;
    padding: 0.5rem 0.8rem;
}
</style>
