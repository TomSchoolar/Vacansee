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
import EmployeeApplications from '../views/employee/EmployeeApplications.vue';

const employeeRoutes = [
  {
    path: '/vacancy',
    name: 'EmployeeIndex',
    component: EmployeeIndex
  },
  {
    path: '/applications',
    name: 'EmployeeApplications',
    component: EmployeeApplications
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
    ...authRoutes,
    ...employeeRoutes,
    ...employerRoutes,
    fourOhFour
]
