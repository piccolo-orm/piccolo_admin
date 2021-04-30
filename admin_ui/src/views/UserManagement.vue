<template>
    <BaseView>
        <div class="users_lists">
            <TitleBar title="Users"></TitleBar>
            <ul>
                <li v-for="(user, index) in userList" :key="index">
                    {{ user }}
                </li>
            </ul>
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
    computed: {
        userList(): any[] {
            return this.$store.state.userManagement.userList
        },
    },
    async mounted() {
        this.$store.commit("updateCurrentTablename", "")

        await this.$store.dispatch("userManagement/fetchUserList")
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
