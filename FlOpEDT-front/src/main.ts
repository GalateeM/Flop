import { createApp, readonly, ref, Ref } from 'vue'

import { createPinia } from 'pinia'

import '@/assets/scss/styles.scss'
import './style.css'

import App from './App.vue'
import '@vuepic/vue-datepicker/dist/main.css'

import router from '@/router'
import { FlopWeek } from '@/ts/type'
import Popper from 'vue3-popper'
    

import i18n from '@/i18n'

import { Quasar } from 'quasar'
import Plugin from '@quasar/quasar-ui-qcalendar/src/QCalendarDay.js'
import '@quasar/quasar-ui-qcalendar/src/css/calendar-day.sass'
// Import icon libraries
import '@quasar/extras/material-icons/material-icons.css'

// Import Quasar css
import 'quasar/src/css/index.sass'

const app = createApp(App)
// Provide the current week and year
const now = new Date()
const startDate = new Date(now.getFullYear(), 0, 1)
const days = Math.floor((now.getTime() - startDate.getTime()) / (24 * 60 * 60 * 1000))
const week = Math.ceil(days / 7)

const currentWeek: Ref<FlopWeek> = ref({
    week: week,
    year: now.getFullYear(),
})

app.provide('currentWeek', readonly(currentWeek.value))
app.component('PopperComponent', Popper)
app.use(router).use(Quasar, {
    plugins: {}, // import Quasar plugins and add here
}).use(Plugin).use(createPinia()).use(i18n).mount('#app')

