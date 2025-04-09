import { Router, RouteLocationNormalizedLoaded } from "vue-router"

import router from "@/router"

declare module "@vue/runtime-core" {
    interface ComponentCustomProperties {
        $router: router
        $route: RouteLocationNormalizedLoaded
    }
}
