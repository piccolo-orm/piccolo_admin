import { Translation, VueI18n } from "vue-i18n"

declare module "@vue/runtime-core" {
    interface ComponentCustomProperties {
        $t: Translation
        $i18n: VueI18n
    }
}
