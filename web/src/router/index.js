import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import UserProfile from "@/views/UserProfile.vue";
import OrganizationUsers from "@/views/OrganizationUsers.vue";

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/user',
        name: 'User Profile',
        component: UserProfile
    },
    {
        path: '/organization-users/:organizationId',
        name: 'OrganizationUsers',
        component: OrganizationUsers
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;