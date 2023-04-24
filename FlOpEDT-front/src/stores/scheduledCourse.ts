import { api } from '@/composables/api'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ScheduledCourse, FlopWeek, Department, WeekDay } from '@/ts/type'


export const useScheduledCourseStore = defineStore('scheduledCourse', () => {
    const scheduledCourses = ref<Array<ScheduledCourse>>([])
    const isAllScheduledFetched = ref<boolean>(false)

    async function fetchScheduledCourses(week : FlopWeek) : Promise<void> {
        await api.fetch
            .scheduledCourses({ week: week.week, year: week.year })
            .then((value: ScheduledCourse[]) => {
                console.log(week.week, week.year)
                console.log(value)
                value.forEach(sc => {
                    sc.start_time = new Date(sc.start_time)
                    sc.end_time = new Date(sc.end_time)
                    let diffInMilliSec : number = sc.end_time - sc.start_time 
                    sc.duration = Math.floor(diffInMilliSec / 1000/60)
                })
                scheduledCourses.value = value
                isAllScheduledFetched.value = true
            })
    }

    function clearScheduledCourses() : void {
        scheduledCourses.value = []
        isAllScheduledFetched.value = false
    }

    function getScheduledCoursesPerDepartment(department : Department) : Array<ScheduledCourse> {
        if(isAllScheduledFetched.value)
            return scheduledCourses.value.filter(sc => sc.course.type.department.abbrev === department.abbrev)
        else
            return []
    }

    function getScheduledCoursesForDay(weekday : WeekDay) : Array<ScheduledCourse> {
        if(isAllScheduledFetched) {
            return scheduledCourses.value.filter(sc => sc.start_time.getDay() === weekday.num)
        }
        else
            return []
    }

    return { 
        scheduledCourses,
        fetchScheduledCourses,
        getScheduledCoursesPerDepartment,
        isAllScheduledFetched,
        clearScheduledCourses,
        getScheduledCoursesForDay
    }
})