import { isLoggedIn, isNotLoggedIn, isEmployer, isEmployee } from '@/middleware';
import Landing from '@/views/Landing.vue';

const landingRoute = {
    path: '/',
    name: 'Landing',
    component: Landing
}



import LogIn from '@/views/auth/LogIn.vue';
import Reset from '@/views/auth/Reset.vue';

const authRoutes = [
    {
        path: '/login',
        name: 'LogIn',
        component: LogIn,
        meta: {
            middleware: [isNotLoggedIn]
        }
    },
    {
      path: '/reset',
      name: 'Reset',
      component: Reset,
      meta: {
        middleware: [isNotLoggedIn]
      }
    }
];



import EmployeeIndex from '../views/employee/EmployeeIndex.vue';
import EmployeeApplications from '../views/employee/EmployeeApplications.vue';
import EmployeeFavourites from '../views/employee/EmployeeFavourites.vue';
import EmployeeProfile from '../views/employee/EmployeeProfile.vue';

const employeeRoutes = [
  {
    path: '/vacancy',
    name: 'EmployeeIndex',
    component: EmployeeIndex,
    meta: {
        middleware: [isLoggedIn, isEmployee]
    }
  },
  {
    path: '/applications',
    name: 'EmployeeApplications',
    component: EmployeeApplications,
    meta: {
        middleware: [isLoggedIn, isEmployee]
    }
  },
  {
    path: '/favourites',
    name: 'EmployeeFavourites',
    component: EmployeeFavourites,
    meta: {
        middleware: [isLoggedIn, isEmployee]
    }
  },
  {
    path: '/profile',
    name: 'EmployeeProfile',
    component: EmployeeProfile,
    meta: {
        middleware: [isLoggedIn, isEmployee]
    }
  }
];



import EmployerIndex from '../views/employer/EmployerIndex.vue';
import EmployerMatch from '../views/employer/EmployerMatch.vue';
import EmployerReview from '../views/employer/EmployerReview.vue';

const employerRoutes = [
  {
    path: '/e/vacancy',
    name: 'EmployerIndex',
    component: EmployerIndex,
    meta: {
        middleware: [isLoggedIn, isEmployer]
    }
  },
  {
    path: '/e/review/:vacancyId',
    name: 'EmployerReview',
    component: EmployerReview,
    meta: {
      middleware: [isLoggedIn, isEmployer]
    }
  },
  {
    path: '/e/match',
    name: 'EmployerMatch',
    component: EmployerMatch,
    meta: {
      middleware: [isLoggedIn, isEmployer]
    }
  }
];


import PrivacyPolicy from '@/views/PrivacyPolicy.vue';

const privacyPolicyRoute = {
    path: '/privacy',
    name: 'PrivacyPolicy',
    component: PrivacyPolicy
}

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
    privacyPolicyRoute,
    fourOhFour
]
