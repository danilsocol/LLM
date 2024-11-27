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

export const addCoinsToOrganization = async (user_id,organization_id, coins) => {
    const response = await axios.post(`${API_URL}/organizations/${organization_id}/coins`, { user_id,coins });
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

export const leaveOrganization = async (user_id, org_id) => {
    try {
        const response = await api.post(`/organizations/${org_id}/leave`, { user_id });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export async function addUserToOrganization(organization_id, admin_id, user_id) {
    try {
        const response = await axios.post(`${API_URL}/organizations/${organization_id}/users/${user_id}`, { admin_id });
        return response.data;
    } catch (error) {
        throw error;
    }
}

export async function getDocumentsByOrganization(organizationId) {
    try {
        const response = await api.get(`/organizations/${organizationId}/documents`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении документов:", error);
        throw error;
    }
}

export async function addDocumentToOrganization(organizationId, documentData) {
    try {
        console.log(documentData)
        const response = await api.post(`/organizations/${organizationId}/documents`, {
            title: documentData.title,
            content: documentData.content,
            organization_id: parseInt(organizationId), //  Обратите внимание на organization_id
            modified_by_id: documentData.modifiedById //  и modified_by_id
        });
        return response.data;
    } catch (error) {
        console.error("Ошибка при добавлении документа:", error);
        throw error;
    }
}

export async function updateDocumentInOrganization(organizationId, documentData) {
    try {
        await api.put(`/documents/${documentData.id}`, {  // Изменено: путь к API
            title: documentData.title,
            content: documentData.content,
            organization_id: parseInt(organizationId),
            modified_by_id: documentData.modifiedById
        });
    } catch (error) {
        console.error("Ошибка при обновлении документа:", error);
        throw error;
    }
}

export async function deleteDocumentFromOrganization(documentId) { // Изменено: только documentId
    try {
        await api.delete(`/documents/${documentId}`); // Изменено: путь к API
    } catch (error) {
        console.error("Ошибка при удалении документа:", error);
        throw error;
    }
}

export async function getQueriesByUserId(userId) {
    try {
        const response = await api.get(`/queries?user_id=${userId}`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении запросов пользователя:", error);
        throw error;
    }
}

export async function getQueriesByOrganizationId(organizationId) {
    try {
        const response = await api.get(`/queries?organization_id=${organizationId}`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении запросов организации:", error);
        throw error;
    }
}

export async function addQuery(queryData) {
    try {
        const response = await api.post(`/queries`, queryData);
        return response.data;
    } catch (error) {
        if (error.response?.status === 400) {
            throw new Error("Недостаточно монет для создания запроса");
        }
        throw error;
    }
}

export async function getTransactionsByOrganizationId(organizationId) {
    try {
        const response = await api.get(`/organizations/${organizationId}/transactions`);
        return response.data;
    } catch (error) {
        console.error("Ошибка при получении транзакций:", error);
        throw error;
    }
}