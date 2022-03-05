import Landing from '@/views/Landing.vue';

const landingRoute = {
    path: '/',
    name: 'Landing',
    component: Landing
}


import EmployeeIndex from '../views/employee/EmployeeIndex.vue';

const employeeRoutes = [
  {
    path: '/vacancy',
    name: 'EmployeeIndex',
    component: EmployeeIndex
  }
];


import EmployerIndex from '../views/employer/EmployerIndex.vue';

const employerRoutes = [
  {
    path: '/e/vacancy',
    name: 'EmployerIndex',
    component: EmployerIndex
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
    ...employeeRoutes,
    ...employerRoutes,
    fourOhFour
]