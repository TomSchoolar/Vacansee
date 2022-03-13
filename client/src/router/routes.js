import Landing from '@/views/Landing.vue';

const landingRoute = {
    path: '/',
    name: 'Landing',
    component: Landing
}



import LogIn from '@/views/auth/LogIn.vue';

const authRoutes = [
    {
        path: '/login',
        name: 'LogIn',
        component: LogIn
    }
];



import EmployeeIndex from '../views/employee/EmployeeIndex.vue';

const employeeRoutes = [
  {
    path: '/vacancy',
    name: 'EmployeeIndex',
    component: EmployeeIndex
  }
];



import EmployerIndex from '../views/employer/EmployerIndex.vue';

import EmployerReview from '../views/employer/EmployerReview.vue';

const employerRoutes = [
  {
    path: '/e/vacancy',
    name: 'EmployerIndex',
    component: EmployerIndex
  },

  {
    path: '/e/review/:vacancyId',
    name: 'EmployerReview',
    component: EmployerReview
  }
];



import Error from '@/views/auth/Error.vue';

const fourOhFour = {
    path: '/:catchAll(.*)',
    name: 'NotFound',
    component: Error
}



export default [
    landingRoute,
    ...authRoutes,
    ...employeeRoutes,
    ...employerRoutes,
    fourOhFour
]
