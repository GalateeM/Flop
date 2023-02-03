import { createRouter, createWebHistory } from 'vue-router'

export const routeNames = {
    home: Symbol('Home'),
    roomReservation: Symbol('room-reservation'),
    departmentSelection: Symbol('department-selection'),
    notFound: Symbol('notFound'),
}

const routes = [
    {
        path: '/',
        name: routeNames.departmentSelection,
        component: () => import('@/views/DepartmentSelectionView.vue'),
        meta: {
            title: 'Ca floppe !',
        },
    },
    {
        path: '/home',
        name: routeNames.home,
        component: () => import('@/views/HomeView.vue'),
        meta: {
            title: 'Ca floppe !',
        },
    },
    {
        path: '/roomreservation/',
        name: routeNames.roomReservation,
        component: () => import('@/views/RoomReservationView.vue'),
        meta: {
            title: 'Réservation de salles',
        },
    },
    {
        path: '/:pathMatch(.*)',
        name: routeNames.notFound,
        component: () => import('@/views/NotFoundView.vue'),
        meta: {
            title: '404 Not Found',
        },
    },
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: routes,
})

router.afterEach((to) => {
    document.title = to.meta.title as string
})

export default router