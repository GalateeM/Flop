import { apiKey, currentWeekKey } from '@/assets/js/keys'
import type { FlopWeek } from '@/assets/js/types'
// Import Bootstrap CSS
import '@/assets/scss/styles.scss'
import router from '@/router'
import '@vuepic/vue-datepicker/dist/main.css'
import { createPinia } from 'pinia'
import type { Ref } from 'vue'
import { createApp, readonly, ref } from 'vue'
import { useRoute } from 'vue-router'
import Popper from 'vue3-popper'
import App from './App.vue'
import { api } from './composables/api'

const app = createApp(App)

app.use(router)

// Provide the current week and year
const now = new Date()
const startDate = new Date(now.getFullYear(), 0, 1)
const days = Math.floor((now.getTime() - startDate.getTime()) / (24 * 60 * 60 * 1000))
const week = Math.ceil(days / 7)

const currentWeek: Ref<FlopWeek> = ref({
    week: week,
    year: now.getFullYear(),
})
app.provide(currentWeekKey, readonly(currentWeek.value))
app.provide(apiKey, readonly(api))
const pinia = createPinia()
app.use(pinia)

export function getDepartment(): string | null {
    const dept = useRoute().params.dept
    if (dept instanceof Array) {
        if (dept.length === 0) {
            return null
        }
        return dept[0]
    }
    return dept
}

app.component('PopperComponent', Popper)
app.mount('#app')
