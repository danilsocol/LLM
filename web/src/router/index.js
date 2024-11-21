import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import UserProfile from "@/views/UserProfile.vue";
import UserList from "@/views/UserList.vue";

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
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;