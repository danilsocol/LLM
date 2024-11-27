import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Register from '../views/Register.vue';
import UserProfile from "@/views/UserProfile.vue";
import OrganizationUsers from "@/views/OrganizationUsers.vue";
import OrganizationDocuments from "@/views/OrganizationDocuments.vue";
import DocumentForm from "@/components/DocumentForm.vue";
import MyQueries from "@/views/MyQueries.vue";
import OrganizationQueries from "@/views/OrganizationQueries.vue";
import AddQuery from "@/components/AddQuery.vue";

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
    {
        path: '/organization/:organizationId/documents',
        name: 'OrganizationDocuments',
        component: OrganizationDocuments,
        children: [
            {
                path: 'add',
                name: 'AddDocument',
                component: DocumentForm,
            },
            {
                path: 'edit/:documentId',
                name: 'EditDocument',
                component: DocumentForm,
            }
        ]
    },
    {
        path: '/my-queries',
        name: 'MyQueries',
        component: MyQueries
    },
    {
        path: '/organization/:organizationId/queries',
        name: 'OrganizationQueries',
        component: OrganizationQueries
    },
    {
        path: '/add-query/:organizationId', // Добавляем параметр organizationId
        name: 'AddQuery',
        component: AddQuery
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;