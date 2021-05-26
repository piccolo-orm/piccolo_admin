import Modal from "../Modal.vue"
import '!style-loader!css-loader!less-loader!../../main.less';

export default {
    title: "Components/Modal",
    component: Modal,
    args: {
        mode: "dark_mode",
    },
    argTypes: {
        mode: {
            options: ["light_mode", "dark_mode"],
            control: { type: 'select' }
        }
    }
}

export const Primary = (args, { argTypes }) => {
    return {
        props: Object.keys(argTypes),
        components: { Modal },
        template: '<Modal :class="mode" v-bind="$props" v-on="$props">Content</Modal>',
        data: {
            mode: args.mode
        }
    }
}
