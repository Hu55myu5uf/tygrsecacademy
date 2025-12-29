/**
 * Progress Tracking Service
 * API client for progress tracking endpoints
 */

const API_URL = 'http://localhost:8000/api/progress';

// Helper to get auth headers
const getAuthHeaders = () => {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
    };
};

export const progressService = {
    // Lesson Progress
    startLesson: async (lessonId: number) => {
        const response = await fetch(`${API_URL}/lessons/${lessonId}/start`, {
            method: 'POST',
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to start lesson');
        return response.json();
    },

    completeLesson: async (lessonId: number, timeSpent: number = 0) => {
        const response = await fetch(`${API_URL}/lessons/${lessonId}/complete?time_spent=${timeSpent}`, {
            method: 'POST',
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to complete lesson');
        return response.json();
    },

    getLessonProgress: async (lessonId: number) => {
        const response = await fetch(`${API_URL}/lessons/${lessonId}`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get lesson progress');
        return response.json();
    },

    // Module Progress
    getModuleProgress: async (moduleId: number) => {
        const response = await fetch(`${API_URL}/modules/${moduleId}`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get module progress');
        return response.json();
    },

    getAllModuleProgress: async () => {
        const response = await fetch(`${API_URL}/modules`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get all module progress');
        return response.json();
    },

    // Tier Progress
    getTierProgress: async (tierNumber: number) => {
        const response = await fetch(`${API_URL}/tiers/${tierNumber}`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get tier progress');
        return response.json();
    },

    getAllTierProgress: async () => {
        const response = await fetch(`${API_URL}/tiers`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get all tier progress');
        return response.json();
    },

    // Dashboard Stats
    getStats: async () => {
        const response = await fetch(`${API_URL}/stats`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get progress stats');
        return response.json();
    },

    getMyProgress: async () => {
        const response = await fetch(`${API_URL}/me`, {
            headers: getAuthHeaders(),
            credentials: 'include',
        });
        if (!response.ok) throw new Error('Failed to get my progress');
        return response.json();
    },
};
