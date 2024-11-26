import axios from 'axios';
import {User} from "@/models/models.js";

const API_URL = 'http://localhost:8080/api';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const login = async (email, password) => {
    try {
        const response = await api.post('/users/login/', { email, password });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const register = async (email, password) => {
    try {
        const response = await api.post('/users/register/', { email, password });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getOrganizationByOrgId  = async (orgId) => {
    try {
        const response = await api.get(`/organizations/${orgId}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const createOrganization = async (organization,user_id) => {
    try {
        const response = await api.post('/organizations/', {organization,user_id});
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const addCoinsToOrganization = async (organization_id, coins) => {
    const response = await axios.post(`${API_URL}/organizations/${organization_id}/coins`, { coins });
    return response.data;
};

export const getUsersByOrganization = async (organizationId) => {
    const response = await axios.get(`${API_URL}/organizations/${organizationId}/users`);
    return response.data;
};

export const getDocumentationByOrganization = async (organizationId) => {
    const response = await axios.get(`${API_URL}/organizations/${organizationId}/documentation`);
    return response.data;
};

export const deleteOrganization = async (orgId) => {
    try {
        const response = await api.delete(`/organizations/${orgId}`);
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const leaveOrganization = async (userId, orgId) => {
    try {
        const response = await api.post(`/organizations/${orgId}/leave`, { userId });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export async function addUserToOrganization(organizationId, adminId, userId) {
    const response = await axios.post(`/organizations/${organizationId}/users/${userId}`, {
        admin_id: adminId,
        user_id: userId
    });
    return response.data;
}