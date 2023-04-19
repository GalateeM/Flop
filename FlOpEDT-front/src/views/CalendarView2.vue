<template>
    
    <div style="max-width: 800px; width: 100%;">
        <div class="row justify-center items-center">
            <q-btn flat label="Prev" @click="calendarPrev" ></q-btn>
            <q-separator vertical ></q-separator>
            <q-btn flat label="Next" @click="calendarNext" ></q-btn>
        </div>
        <q-separator ></q-separator>
        <q-calendar
        ref="calendar"
        v-model="selectedDate"
        view="day"
        locale="en-us"
        animated
        transition-prev="slide-right"
        transition-next="slide-left"
        style="height: 400px;"
        ></q-calendar>
        <div> tgada</div>
        <div>{{ selectedDate }}</div>
    </div>
    
    <!-- <div class="row justify-center">
        <div style="display: flex; max-width: 800px; width: 100%; height: 400px;">
            <q-calendar-day
            ref="calendar"
            v-model="selectedDate"
            view="week"
            :interval-minutes="30"
            :interval-count="48"
            animated
            bordered
            @change="onChange"
            @moved="onMoved"
            @click-date="onClickDate"
            @click-time="onClickTime"
            @click-interval="onClickInterval"
            @click-head-intervals="onClickHeadIntervals"
            @click-head-day="onClickHeadDay">
            <template #day-body="{ scope: { timestamp, timeStartPos, timeDurationHeight } }">
                <template
                v-for="event in getEvents(timestamp.date)"
                :key="event.id"
                >
                <div
                v-if="event.time !== undefined"
                class="my-event"
                :class="badgeClasses(event, 'body')"
                :style="badgeStyles(event, 'body', timeStartPos, timeDurationHeight)"
                >
                <div class="title q-calendar__ellipsis">
                    {{ event.title }}
                    <q-tooltip>{{ event.time + ' - ' + event.details }}</q-tooltip>
                </div>
            </div>
        </template>
    </template>
</q-calendar-day>
</div> -->
</template>

<script setup lang="ts">
import {QCalendar, today} from '@quasar/quasar-ui-qcalendar/src/index.js'

import { ref, Ref } from 'vue';

const selectedDate = ref(today())

const calendar: Ref<QCalendar> = ref(null)

function calendarNext () {
    calendar.value.next()
}   
function calendarPrev () {
    calendar.value.prev()
}
</script>