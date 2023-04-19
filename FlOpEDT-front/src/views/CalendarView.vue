<template>
    <div class="subcontent">
      <navigation-bar
        @today="onToday"
        @prev="onPrev"
        @next="onNext"
      />
  
      <div class="row justify-center">
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
        </div>
      </div>
    </div>
  </template>

<script setup lang="ts">
import { addToDate, isBetweenDates, parsed, parseTime, QCalendarDay, today, parseTimestamp } from '@quasar/quasar-ui-qcalendar/src/index.js'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarDay.sass'
import NavigationBar from '@/components/utils/NavigationBar.vue'
import { computed, ref } from 'vue'

const selectedDate = ref(today())
const calendar = ref<QCalendarDay>(null)
const eventsMap= computed(() => {
      const map: any = {}
      // this.events.forEach(event => (map[ event.date ] = map[ event.date ] || []).push(event))
      events.forEach(event => {
        if (!map[ event.date ]) {
          map[ event.date ] = []
        }
        map[ event.date ].push(event)
        if (event.days) {
          let timestamp = parseTimestamp(event.date)
          let days = event.days
          do {
            timestamp = addToDate(timestamp, { day: 1 })
            if (!map[ timestamp.date ]) {
              map[ timestamp.date ] = []
            }
            map[ timestamp.date ].push(event)
          } while (--days > 0)
        }
      })
      return map
    })
const resourceWidth = 100
const resourceHeight = 70
const resourceMinHeight = 20
const resources = ref([
    { id: '1', name: 'John' },
    {
        id: '2',
        name: 'Board Room',
        expanded: false,
        children: [
        { id: '2.1', name: 'Room-1' },
        {
            id: '2.2',
            name: 'Room-2',
            expanded: false,
            children: [
            { id: '2.2.1', name: 'Partition-A' },
            { id: '2.2.2', name: 'Partition-B' },
            { id: '2.2.3', name: 'Partition-C' }
            ]
        }
        ]
    },
    { id: '3', name: 'Mary' },
    { id: '4', name: 'Susan' },
    { id: '5', name: 'Olivia' }
])
const events = [
    {
        id: 1,
        title: 'Meeting',
        details: 'Time to pitch my idea to the company',
        date: today(),
        time: '09:00',
        duration: 120,
        bgcolor: 'red',
        icon: 'fas fa-handshake'
    },
    {
        id: 2,
        title: 'Lunch',
        details: 'Company is paying!',
        date: today(),
        time: '12:00',
        duration: 60,
        bgcolor: 'teal',
        icon: 'fas fa-hamburger'
    },
    {
        id: 3,
        title: 'Conference',
        details: 'Teaching Javascript 101',
        date: today(),
        time: '13:00',
        duration: 240,
        bgcolor: 'blue',
        icon: 'fas fa-chalkboard-teacher'
    },
    {
        id: 4,
        title: 'Girlfriend',
        details: 'Meet GF for dinner at Swanky Restaurant',
        date: today(),
        time: '19:00',
        duration: 180,
        bgcolor: 'teal-2',
        icon: 'fas fa-utensils'
    }
]
function onToday () {
    calendar.moveToToday()
}
function onPrev () {
    calendar.prev()
}
function onNext () {
    calendar.next()
}
function onMoved (data: any) {
    console.log('onMoved', data)
}
function onChange (data: any) {
    console.log('onChange', data)
}
function onClickDate (data: any) {
    console.log('onClickDate', data)
}
function onClickTime (data: any) {
    console.log('onClickTime', data)
}
function onClickInterval (data: any) {
    console.log('onClickInterval', data)
}
function onClickHeadIntervals (data: any) {
    console.log('onClickHeadIntervals', data)
}
function onClickHeadDay (data: any) {
    console.log('onClickHeadDay', data)
}

function getEvents (dt: any) {
    // get all events for the specified date
    const events = eventsMap[ dt ] || []
    if (events.length === 1) {
    events[ 0 ].side = 'full'
    }
    else if (events.length === 2) {
    // this example does no more than 2 events per day
    // check if the two events overlap and if so, select
    // left or right side alignment to prevent overlap
    const startTime = addToDate(parsed(events[ 0 ].date), { minute: parseTime(events[ 0 ].time) })
    const endTime = addToDate(startTime, { minute: events[ 0 ].duration })
    const startTime2 = addToDate(parsed(events[ 1 ].date), { minute: parseTime(events[ 1 ].time) })
    const endTime2 = addToDate(startTime2, { minute: events[ 1 ].duration })
    if (isBetweenDates(startTime2, startTime, endTime, true) || isBetweenDates(endTime2, startTime, endTime, true)) {
        events[ 0 ].side = 'left'
        events[ 1 ].side = 'right'
    }
    else {
        events[ 0 ].side = 'full'
        events[ 1 ].side = 'full'
    }
    }
    return events
}
function getStyle (event: any) {
    return {
        position: 'absolute',
        background: 'white',
        left: event.left,
        width: event.width
    }
}
function getLeft (scope: any, event: any) {
    const left = event.dow * parseFloat(scope.cellWidth)
    const val = left + (scope.cellWidth.endsWith('%') ? '%' : 'px')
    return val
}
function getWidth (scope: any, event: any) {
    const width = (event.range ? event.range : 1) * parseFloat(scope.cellWidth)
    const val = width + (scope.cellWidth.endsWith('%') ? '%' : 'px')
    return val
}
</script>