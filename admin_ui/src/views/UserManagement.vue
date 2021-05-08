<template>
    <BaseView>
        <template v-if="activeUser && userList">
            <PasswordModal
                v-if="showPasswordModal"
                v-on:close="showPasswordModal = false"
                v-bind:username="activeUser.username"
            />

            <Modal v-if="showHelpModal" v-on:close="showHelpModal = false">
                <h1>Help</h1>

                <h2><font-awesome-icon icon="check" />Active</h2>
                <p>
                    A user's account must be active in order to login, even if
                    they are an admin or superuser.
                </p>

                <h2><font-awesome-icon icon="key" />Admin</h2>
                <p>Is able to login to the admin.</p>

                <h2><font-awesome-icon icon="star" />Superuser</h2>
                <p>Is able to change any other user's password.</p>
            </Modal>

            <div class="users_lists">
                <TitleBar title="Users">
                    <template v-slot:buttons
                        ><a
                            class="button"
                            v-on:click.prevent="showHelpModal = true"
                            ><font-awesome-icon icon="question-circle" />
                            Help</a
                        ></template
                    >
                </TitleBar>
                <Table>
                    <template v-slot:thead>
                        <tr>
                            <th><font-awesome-icon icon="user" />Username</th>
                            <th><font-awesome-icon icon="check" />Active</th>
                            <th><font-awesome-icon icon="key" /> Admin</th>
                            <th><font-awesome-icon icon="star" />Superuser</th>
                            <th>Tools</th>
                        </tr>
                    </template>

                    <template v-slot:tbody>
                        <tr v-for="(user, index) in userList" :key="index">
                            <td>{{ user.username }}</td>
                            <td>
                                <BooleanIcon v-bind:boolean="user.active" />
                            </td>
                            <td><BooleanIcon v-bind:boolean="user.admin" /></td>
                            <td>
                                <BooleanIcon v-bind:boolean="user.superuser" />
                            </td>
                            <td>
                                <span
                                    style="display: block; text-align: right"
                                    v-if="
                                        activeUser.superuser ||
                                        activeUser.username == user.username
                                    "
                                >
                                    <a
                                        href="#"
                                        v-on:click.prevent="
                                            activeUser = user
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
        </template>
        <p v-else>Loading ...</p>
    </BaseView>
</template>


<script lang="ts">
import Vue from "vue"

import BaseView from "./BaseView.vue"
import BooleanIcon from "../components/BooleanIcon.vue"
import Table from "../components/Table.vue"
import TitleBar from "../components/TitleBar.vue"
import PasswordModal from "../components/PasswordModal.vue"
import Modal from "../components/Modal.vue"
import { User } from "../interfaces"

export default Vue.extend({
    components: {
        BaseView,
        BooleanIcon,
        Modal,
        PasswordModal,
        Table,
        TitleBar,
    },
    data() {
        return {
            showHelpModal: false,
            showPasswordModal: false,
        }
    },
    computed: {
        activeUser(): User {
            return this.$store.state.user
        },
        userList(): User[] {
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
