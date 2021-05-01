<template>
    <BaseView>
        <PasswordModal
            v-if="showPasswordModal"
            v-on:close="showPasswordModal = false"
        />

        <div class="users_lists">
            <TitleBar title="Users"></TitleBar>
            <Table>
                <template v-slot:thead>
                    <tr>
                        <th>Username</th>
                        <th>Active</th>
                        <th>Last login</th>
                        <th>Admin</th>
                        <th>Superuser</th>
                        <th>Tools</th>
                    </tr>
                </template>

                <template v-slot:tbody>
                    <tr v-for="(user, index) in userList" :key="index">
                        <td>{{ user.username }}</td>
                        <td>Active</td>
                        <td>Last login</td>
                        <td>Admin</td>
                        <td>Superuser</td>
                        <td>
                            <span style="display: block; text-align: right">
                                <a
                                    href="#"
                                    v-on:click.prevent="
                                        showPasswordModal = true
                                    "
                                    >Change password</a
                                >
                            </span>
                        </td>
                    </tr>
                </template>
            </Table>
        </div>
    </BaseView>
</template>


<script lang="ts">
import Vue from "vue"
import BaseView from "./BaseView.vue"
import Table from "../components/Table.vue"
import TitleBar from "../components/TitleBar.vue"
import PasswordModal from "../components/PasswordModal.vue"

export default Vue.extend({
    components: {
        BaseView,
        PasswordModal,
        Table,
        TitleBar,
    },
    data() {
        return {
            showPasswordModal: false,
        }
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
