<template>
    <div class="subcontent">
      <navigation-bar
        @today="onToday"
        @prev="onPrev"
        @next="onNext"
      />

      <div class="row justify-center">
        <div style="display: flex; max-width: 100%; width: 100%; height: 100%;">
          <q-calendar-day
            ref="calendar"
            v-model="selectedDate"
            view="week"
            animated
            bordered
            transition-next="slide-left"
            transition-prev="slide-right"
            no-active-date
            :interval-start="6"
            :interval-count="18"
            :interval-height="28"
            :weekdays="[1,2,3,4,5]"
            @change="onChange"
            @moved="onMoved"
            @click-date="onClickDate"
            @click-time="onClickTime"
            @click-interval="onClickInterval"
            @click-head-intervals="onClickHeadIntervals"
            @click-head-day="onClickHeadDay">
            <template #head-day-event="{ scope: { timestamp } }">
              <!-- <div style="display: flex; justify-content: center; flex-wrap: wrap; padding-bottom: 2px; padding-top: 2px;">
                <template
                  v-for="group in getGroupsByTrainProgId[84]"
                  :key="group.id">
                  <q-badge
                    :class="badgeClasses(group, 'header')"
                    :style="badgeGroupStyles(group, 'header')"
                    style="cursor: pointer; height: 12px; font-size: 10px; margin-bottom: 1px; margin-top: 1px;"
                  >
                    <span class="title q-calendar__ellipsis">
                      {{ group.name }}
                      <q-tooltip>{{ group.name }}</q-tooltip>
                    </span>
                  </q-badge>
                </template>
                 <!- <template
                  v-for="event in eventsMap[timestamp.date]"
                  :key="event.id"
                >
                  <q-badge
                    v-if="!event.time"
                    :class="badgeClasses(event, 'header')"
                    :style="badgeStyles(event, 'header')"
                    style="width: 100%; cursor: pointer; height: 12px; font-size: 10px; margin: 1px;"
                  >
                    <span class="title q-calendar__ellipsis">
                      {{ event.title }}
                      <q-tooltip>{{ event.details }}</q-tooltip>
                    </span>
                  </q-badge>
                  <q-badge
                    v-else
                    :class="badgeClasses(event, 'header')"
                    :style="badgeStyles(event, 'header')"
                    style="margin: 1px; width: 10px; max-width: 10px; height: 10px; max-height: 10px"
                    @click="scrollToEvent(event)"
                  >
                    <q-tooltip>{{ event.time + ' - ' + event.details }}</q-tooltip>
                  </q-badge>
                </template> ->
              </div> -->
            </template>

            <template #day-body="{ scope: { timestamp, timeStartPos, timeDurationHeight } }">
              <template
                v-for="event in getScheduled(timestamp.date)"
                :key="event.id">
                <div
                  v-if="event.time !== undefined"
                  class="my-event"
                  :class="badgeClasses(event, 'body')"
                  :style="badgeStyles(event, 'body', timeStartPos, timeDurationHeight)">
                  <span class="title q-calendar__ellipsis">
                    {{ event.course.groups[0].name }}
                    <q-tooltip>{{ event.details }}</q-tooltip>
                  </span>
                </div>
              </template>
            </template>
          </q-calendar-day>
        </div>
      </div>
    </div>
  </template>

<script setup lang="ts">
import {
    QCalendarDay,
    addToDate,
    parseTimestamp,
    isBetweenDates,
    today,
    parsed,
    parseDate,
    parseTime
} from '@quasar/quasar-ui-qcalendar/src/QCalendarDay.js'
import '@quasar/quasar-ui-qcalendar/src/QCalendarVariables.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarTransitions.sass'
import '@quasar/quasar-ui-qcalendar/src/QCalendarDay.sass'
import { computed, onMounted, ref } from 'vue'
import NavigationBar from '@/components/utils/NavigationBar.vue'
import { useScheduledCourseStore } from '@/stores/scheduledCourse'
import { api } from '@/composables/api'
import { useDepartmentStore } from '@/stores/department'
import type { Group } from '@/ts/types'

//Test on scheduledCourses data
const scheduledCourseStore = useScheduledCourseStore()
const departmentStore = useDepartmentStore()
const selectedDate = ref(today())
const calendar = ref<QCalendarDay>(null)
const CURRENT_DAY = new Date()
const groups = ref([])
const events = ref([
    {
        id: 1,
        title: '1st of the Month',
        details: 'Everything is funny as long as it is happening to someone else',
        date: getCurrentDay(1),
        bgcolor: 'orange'
    },
    {
        id: 2,
        title: 'Sisters Birthday',
        details: 'Buy a nice present',
        date: getCurrentDay(4),
        bgcolor: 'green',
        icon: 'fas fa-birthday-cake'
    },
    {
        id: 3,
        title: 'Meeting',
        details: 'Time to pitch my idea to the company',
        date: getCurrentDay(10),
        time: '10:00',
        duration: 120,
        bgcolor: 'red',
        icon: 'fas fa-handshake'
    },
    {
        id: 4,
        title: 'Lunch',
        details: 'Company is paying!',
        date: getCurrentDay(10),
        time: '11:30',
        duration: 90,
        bgcolor: 'teal',
        icon: 'fas fa-hamburger'
    },
    {
        id: 5,
        title: 'Visit mom',
        details: 'Always a nice chat with mom',
        date: getCurrentDay(20),
        time: '17:00',
        duration: 90,
        bgcolor: 'grey',
        icon: 'fas fa-car'
    },
    {
        id: 6,
        title: 'Conference',
        details: 'Teaching Javascript 101',
        date: getCurrentDay(22),
        time: '08:00',
        duration: 540,
        bgcolor: 'blue',
        icon: 'fas fa-chalkboard-teacher'
    },
    {
        id: 7,
        title: 'Girlfriend',
        details: 'Meet GF for dinner at Swanky Restaurant',
        date: getCurrentDay(22),
        time: '19:00',
        duration: 180,
        bgcolor: 'teal',
        icon: 'fas fa-utensils'
    },
    {
        id: 8,
        title: 'Fishing',
        details: 'Time for some weekend R&R',
        date: getCurrentDay(27),
        bgcolor: 'purple',
        icon: 'fas fa-fish',
        days: 2
    },
    {
        id: 9,
        title: 'Vacation',
        details: 'Trails and hikes, going camping! Don\'t forget to bring bear spray!',
        date: getCurrentDay(29),
        bgcolor: 'purple',
        icon: 'fas fa-plane',
        days: 5
    }
])

function scheduledCoursesToCalendarSlot(scheduledCourse: any): any {
    let slot = scheduledCourse
    slot.title = scheduledCourse.course.module.abbrev
    slot.details = scheduledCourse.tutor + " is teaching " + scheduledCourse.course.module.name
    slot.date = parseDate(scheduledCourse.start_time).date
    slot.time = scheduledCourse.start_time.toLocaleTimeString()
    console.log("XXTime", slot.date)
    slot.bgcolor = 'purple'
    slot.icon ='fas fa-plane'
    slot.side = "right"
    return slot
}

const scheduledMap = computed(() => {
    const map = {}
    scheduledCourseStore.scheduledCourses.forEach(scheduledCourse => {
      let slot = scheduledCoursesToCalendarSlot(scheduledCourse)
      if(!map[slot.date]) {
        map[slot.date] = []
      }
      map[slot.date].push(slot)
      // let hasBasicGroup = false
      // let group : Group
      // scheduledCourse.course.groups.forEach(gp => {

      //   if(gp.id in getGroupsById.value) {
      //     hasBasicGroup = true
      //     group = gp
      //   }
      // })
      // if(hasBasicGroup) {
      //   let slot = scheduledCoursesToCalendarSlot(scheduledCourse)
      //   slot.group = group
      //   slot.index = getIndexById.value[group.id]
      //   if(!map[slot.date]) {
      //       map[slot.date] = []
      //   }
      //   map[slot.date].push(slot)
      //   if(slot.days) {
      //       let timestamp = parseTimestamp(slot.date)
      //       let days = slot.days
      //       do {
      //           timestamp = addToDate(timestamp, { day: 1 })
      //           if (!map[ timestamp.date ]) {
      //               map[ timestamp.date ] = []
      //           }
      //           map[ timestamp.date ].push(slot)
      //       } while (--days > 0)
      //   }
      // }
    })
    return map
})

const getGroupsById = computed(() => {
  return Object.fromEntries(groups.value.map((group: any) => [group.id, group]))
})

const getIndexById = computed(() => {
  let map = {}
  let i = 0
  map = groups.value.map((group: Group) => {[i++, group]})
  console.log("MAP", map)
  return map
})

const getGroupsByTrainProgId = computed(() => {
  let map = {}
  groups.value.forEach((group: any) => {
    if(!map[group.train_prog]) {
      map[group.train_prog] = []
    }
    map[group.train_prog].push(group)
  })
  console.log("GROUPS", map)
  return map
})

// convert the events into a map of lists keyed by date
const eventsMap= computed(() => {
    const map = {}
    // this.events.forEach(event => (map[ event.date ] = map[ event.date ] || []).push(event))
    events.value.forEach(event => {
        console.log("XXTime2", event.date)
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

const widthPercentGroup = computed(() => {
  return 20
  //return 100/getGroupsByTrainProgId.value[84].length
})

function getCurrentDay (day: any) {
    console.log("XX", CURRENT_DAY)
    const newDay = new Date(CURRENT_DAY)
    newDay.setDate(day)
    const tm = parseDate(newDay)
    console.log("XXY", tm)
    return tm.date
}
function badgeClasses (event: any, type: any) {
    const isHeader = type === 'header'
    return {
        [ `text-white bg-${ event.bgcolor }` ]: true,
        'full-width': !isHeader && (!event.side || event.side === 'full'),
        'left-side': !isHeader && event.side === 'left',
        'right-side': !isHeader && event.side === 'right',
        'rounded-border': true
    }
}
function badgeStyles (event: any, type: any, timeStartPos : any = undefined, timeDurationHeight: any = undefined) {
    const s = {left: "10%", width: widthPercentGroup.value + "%" }
    if (timeStartPos && timeDurationHeight) {
        s.top = timeStartPos(event.time) + 'px'
        s.height = timeDurationHeight(event.duration) + 'px'
    }
    s[ 'align-items' ] = 'flex-start'
    return s
}
function badgeGroupStyles (event: any, type: any, timeStartPos : any = undefined, timeDurationHeight: any = undefined) {
    const s = { top: "", height: "", width: widthPercentGroup.value + "%" }
    if (timeStartPos && timeDurationHeight) {
        s.top = timeStartPos(event.time) + 'px'
        s.height = timeDurationHeight(event.duration) + 'px'
    }
    s[ 'align-items' ] = 'flex-start'
    return s
  }

function getScheduled (dt : any) {
    // get all events for the specified date
    const events: any = scheduledMap.value[ dt ] || []
    // if (events.length === 1) {
    //     events[ 0 ].side = 'full'
    // }
    // else if (events.length === 2) {
    //     // this example does no more than 2 events per day
    //     // check if the two events overlap and if so, select
    //     // left or right side alignment to prevent overlap
    //     const startTime = addToDate(parsed(events[ 0 ].date), { minute: parseTime(events[ 0 ].time) })
    //     const endTime = addToDate(startTime, { minute: events[ 0 ].duration })
    //     const startTime2 = addToDate(parsed(events[ 1 ].date), { minute: parseTime(events[ 1 ].time) })
    //     const endTime2 = addToDate(startTime2, { minute: events[ 1 ].duration })
    //     if (isBetweenDates(startTime2, startTime, endTime, true) || isBetweenDates(endTime2, startTime, endTime, true)) {
    //         events[ 0 ].side = 'left'
    //         events[ 1 ].side = 'right'
    //     }
    //     else {
    //         events[ 0 ].side = 'full'
    //         events[ 1 ].side = 'full'
    //     }
    // }
    return events
}

function getEvents (dt: any) {
    // get all events for the specified date
    const events: any = eventsMap.value[ dt ] || []
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

function scrollToEvent (event: any) {
    calendar.value.scrollToTime(event.time, 350)
}
function onToday () {
    calendar.value.moveToToday()
}
function onPrev () {
    calendar.value.prev()
}
function onNext () {
    calendar.value.next()
}
function onMoved (data : any) {
    console.log('onMoved', data)
}
function onChange (data : any) {
    console.log('onChange', data)
}
function onClickDate (data : any) {
    console.log('onClickDate', data)
}
function onClickTime (data : any) {
    console.log('onClickTime', data)
}
function onClickInterval (data : any) {
    console.log('onClickInterval', data)
}
function onClickHeadIntervals (data : any) {
    console.log('onClickHeadIntervals', data)
}
function onClickHeadDay (data : any) {
    console.log('onClickHeadDay', data)
}

onMounted(() => {
    scheduledCourseStore.fetchScheduledCourses({week : 16, year: 2023}).then(() => {
        console.log(scheduledMap.value)
    })
    api.getGroups(departmentStore.getCurrentDepartment).then(
      (groupsFetched : any) => {
        groups.value = groupsFetched.filter((group: Group) => group.basic === true)
      }
    )
})
</script>

<style lang="sass" scoped>
.my-event
  position: absolute
  font-size: 12px
  justify-content: center
  margin: 0 1px
  text-overflow: ellipsis
  overflow: hidden
  cursor: pointer
.title
  position: relative
  display: flex
  justify-content: center
  align-items: center
  height: 100%
.text-white
  color: white
.bg-blue
  background: blue
.bg-green
  background: green
.bg-orange
  background: orange
.bg-red
  background: red
.bg-teal
  background: teal
.bg-grey
  background: grey
.bg-purple
  background: purple
  .full-width
   left: 0
   width: calc(100% - 2px)
  .left-side
   left: 0
   width: calc(50% - 3px)
  .right-side
   left: 50%
   width: calc(50% - 3px)
  .rounded-border
  border-radius: 2px
</style>
