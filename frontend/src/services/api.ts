import axios, { AxiosInstance } from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Create axios instance
const api: AxiosInstance = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add auth token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor - simplified for 24-hour tokens
// Just clear tokens on 401 and let user login again
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        // If 401, clear tokens - don't try to refresh since it causes loops
        if (error.response?.status === 401) {
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            // Don't redirect here - let the app handle it
        }
        return Promise.reject(error);
    }
);

// Types
export interface User {
    id: number;
    email: string;
    username: string;
    first_name?: string;
    last_name?: string;
    role: 'student' | 'tutor' | 'admin';
    is_active: boolean;
    bio?: string;
    avatar_url?: string;
    created_at: string;
}

export interface LoginResponse {
    access_token: string;
    refresh_token: string;
    token_type: string;
    user: User;
}

// Auth Service
export const authService = {
    async login(email: string, password: string): Promise<LoginResponse> {
        const response = await api.post('/api/auth/login', { email, password });
        return response.data;
    },

    async register(email: string, username: string, password: string): Promise<User> {
        const response = await api.post('/api/auth/register', { email, username, password });
        return response.data;
    },

    async logout(refreshToken: string): Promise<void> {
        await api.post('/api/auth/logout', { refresh_token: refreshToken });
    },

    async getCurrentUser(): Promise<User> {
        const response = await api.get('/api/users/me');
        return response.data;
    },

    async updateProfile(data: Partial<User>): Promise<User> {
        const response = await api.put('/api/users/me', data);
        return response.data;
    },

    async changePassword(currentPassword: string, newPassword: string): Promise<void> {
        await api.post('/api/auth/change-password', {
            current_password: currentPassword,
            new_password: newPassword,
        });
    },
};

// User Service
export const userService = {
    async getUser(userId: number): Promise<User> {
        const response = await api.get(`/api/users/${userId}`);
        return response.data;
    },

    async listUsers(skip = 0, limit = 100): Promise<User[]> {
        const response = await api.get('/api/users', { params: { skip, limit } });
        return response.data;
    },

    async deleteUser(userId: number): Promise<void> {
        await api.delete(`/api/users/${userId}`);
    },

    async getPublicProfile(username: string): Promise<any> { // Typing as any for now or define interface
        const response = await api.get(`/api/users/profile/${username}`);
        return response.data;
    },
};

// Curriculum Service
export const curriculumService = {
    async getTiers() {
        const response = await api.get('/api/curriculum/tiers');
        return response.data;
    },

    async getModules(tierId: number) {
        const response = await api.get(`/api/curriculum/tiers/${tierId}/modules`);
        return response.data;
    },

    async getModule(moduleId: number) {
        const response = await api.get(`/api/curriculum/modules/${moduleId}`);
        return response.data;
    },

    async getLesson(lessonId: number) {
        const response = await api.get(`/api/curriculum/lessons/${lessonId}`);
        return response.data;
    },
};

// Lab Service
export const labService = {
    async getLabs() {
        const response = await api.get('/api/labs/');
        return response.data;
    },

    async getLab(labId: number) {
        const response = await api.get(`/api/labs/${labId}`);
        return response.data;
    },

    async startLab(labId: number) {
        const response = await api.post(`/api/labs/${labId}/start`);
        return response.data;
    },

    async stopLab(instanceId: number) {
        const response = await api.post(`/api/labs/instances/${instanceId}/stop`);
        return response.data;
    },

    async submitAction(instanceId: number, action: any) {
        const response = await api.post(`/api/labs/instances/${instanceId}/actions`, action);
        return response.data;
    },

    async requestHint(instanceId: number) {
        const response = await api.post(`/api/labs/instances/${instanceId}/hint`);
        return response.data;
    },

    async completeLab(instanceId: number) {
        const response = await api.post(`/api/labs/instances/${instanceId}/complete`);
        return response.data;
    },
};

// Challenge Service

export const challengeService = {
    async getChallenges(category?: string, difficulty?: string) {
        const params = new URLSearchParams();
        if (category) params.append('category', category);
        if (difficulty) params.append('difficulty', difficulty);
        const response = await api.get(`/api/challenges/?${params.toString()}`);
        return response.data;
    },

    async getChallenge(challengeId: number) {
        const response = await api.get(`/api/challenges/${challengeId}`);
        return response.data;
    },

    async submitFlag(challengeId: number, flag: string) {
        const response = await api.post(`/api/challenges/${challengeId}/submit`, null, {
            params: { flag }
        });
        return response.data;
    },

    async getLeaderboard() {
        const response = await api.get('/api/challenges/leaderboard/global');
        return response.data;
    },
};

// Progress Service
export const progressService = {
    async getMyProgress() {
        const response = await api.get('/api/progress/me');
        return response.data;
    },

    async getUserProgress(userId: number) {
        const response = await api.get(`/api/progress/users/${userId}`);
        return response.data;
    },

    async getAnalytics() {
        const response = await api.get('/api/progress/analytics');
        return response.data;
    },

    async startLesson(lessonId: number) {
        const response = await api.post(`/api/progress/lessons/${lessonId}/start`);
        return response.data;
    },

    async completeLesson(lessonId: number, timeSpent: number = 0) {
        const response = await api.post(`/api/progress/lessons/${lessonId}/complete`, null, {
            params: { time_spent: timeSpent }
        });
        return response.data;
    },

    // Alias for compatibility
    async markLessonComplete(lessonId: number) {
        return this.completeLesson(lessonId);
    },

    async getLessonProgress(lessonId: number) {
        const response = await api.get(`/api/progress/lessons/${lessonId}`);
        return response.data;
    },

    async getModuleProgress(moduleId: number) {
        const response = await api.get(`/api/progress/modules/${moduleId}`);
        return response.data;
    },

    async getAllModuleProgress() {
        const response = await api.get('/api/progress/modules');
        return response.data;
    },

    async getTierProgress(tierNumber: number) {
        const response = await api.get(`/api/progress/tiers/${tierNumber}`);
        return response.data;
    },

    async getAllTierProgress() {
        const response = await api.get('/api/progress/tiers');
        return response.data;
    },

    async getStats() {
        const response = await api.get('/api/progress/stats');
        return response.data;
    },
};

// Publishing Service
export const publishingService = {
    async submitCapstone(data: any) {
        const response = await api.post('/api/publish/capstone', data);
        return response.data;
    },

    async getCapstones() {
        const response = await api.get('/api/publish/capstones');
        return response.data;
    },

    async reviewCapstone(capstoneId: number, feedback: string, score: number) {
        const response = await api.put(`/api/publish/capstones/${capstoneId}/review`, {
            feedback,
            score,
            approved: score >= 70
        });
        return response.data;
    },

    async getBlogPosts() {
        const response = await api.get('/api/publish/blog');
        return response.data;
    },

    async publishBlog(data: any) {
        const response = await api.post('/api/publish/blog', data);
        return response.data;
    },
};

// Capstone Service
export const capstoneService = {
    // Student endpoints
    async getTiers() {
        const response = await api.get('/api/capstone/tiers');
        return response.data;
    },

    async getTier(tierId: number) {
        const response = await api.get(`/api/capstone/tier/${tierId}`);
        return response.data;
    },

    async getMySubmissions() {
        const response = await api.get('/api/capstone/my-submissions');
        return response.data;
    },

    async getSubmission(submissionId: number) {
        const response = await api.get(`/api/capstone/submission/${submissionId}`);
        return response.data;
    },

    async createSubmission(capstoneTierId: number, data: any) {
        const response = await api.post(`/api/capstone/tier/${capstoneTierId}/submit`, data);
        return response.data;
    },

    async updateSubmission(submissionId: number, data: any) {
        const response = await api.put(`/api/capstone/submission/${submissionId}`, data);
        return response.data;
    },

    async submitFinal(submissionId: number) {
        const response = await api.post(`/api/capstone/submission/${submissionId}/submit`);
        return response.data;
    },

    // Instructor endpoints
    async getAllSubmissions(filters?: {
        tier_id?: number;
        status_filter?: string;
        user_id?: number;
        skip?: number;
        limit?: number;
    }) {
        const response = await api.get('/api/capstone/admin/submissions', { params: filters });
        return response.data;
    },

    async getSubmissionForGrading(submissionId: number) {
        const response = await api.get(`/api/capstone/admin/submission/${submissionId}`);
        return response.data;
    },

    async gradeSubmission(submissionId: number, data: {
        score: number;
        feedback: string;
        rubric_evaluation?: any;
        status: 'graded' | 'approved' | 'rejected';
    }) {
        const response = await api.put(`/api/capstone/admin/submission/${submissionId}/grade`, data);
        return response.data;
    },

    async toggleFeature(submissionId: number, isFeatured: boolean) {
        const response = await api.put(`/api/capstone/admin/submission/${submissionId}/feature`, {
            is_featured: isFeatured
        });
        return response.data;
    },

    // Public endpoints
    async getShowcase(filters?: { tier_id?: number; limit?: number }) {
        const response = await api.get('/api/capstone/showcase', { params: filters });
        return response.data;
    },
};

// Admin Service
export const adminService = {
    // User management
    async getAllUsers(filters?: {
        role?: string;
        search?: string;
        is_active?: boolean;
        skip?: number;
        limit?: number;
    }) {
        const response = await api.get('/api/admin/users', { params: filters });
        return response.data;
    },

    async getUserDetails(userId: number) {
        const response = await api.get(`/api/admin/users/${userId}`);
        return response.data;
    },

    async updateUserRole(userId: number, role: 'student' | 'tutor' | 'admin') {
        const response = await api.put(`/api/admin/users/${userId}/role`, { role });
        return response.data;
    },

    async updateUserStatus(userId: number, isActive: boolean) {
        const response = await api.put(`/api/admin/users/${userId}/status`, { is_active: isActive });
        return response.data;
    },

    async deleteUser(userId: number) {
        const response = await api.delete(`/api/admin/users/${userId}`);
        return response.data;
    },

    // Platform stats
    async getPlatformStats() {
        const response = await api.get('/api/admin/stats');
        return response.data;
    },
};

// AI Tutor Service
export const aiService = {
    async sendMessage(message: string, contextType: 'lesson' | 'lab' | 'challenge', contextId: number) {
        const response = await api.post('/api/ai/chat', {
            message,
            context_type: contextType,
            context_id: contextId
        });
        return response.data;
    },

    async getHint(contextType: 'lab' | 'challenge', contextId: number, hintLevel: number = 1) {
        const response = await api.post('/api/ai/hint', {
            context_type: contextType,
            context_id: contextId,
            hint_level: hintLevel
        });
        return response.data;
    },

    async getHistory(contextType: string, contextId: number, limit: number = 20) {
        const response = await api.get(`/api/ai/history/${contextType}/${contextId}`, {
            params: { limit }
        });
        return response.data;
    },

    async clearHistory(contextType: string, contextId: number) {
        const response = await api.delete(`/api/ai/history/${contextType}/${contextId}`);
        return response.data;
    },
};

export default api;
