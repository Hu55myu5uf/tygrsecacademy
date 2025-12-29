import { useState, useEffect } from 'react';
import { Search, Filter, Users, UserCheck, UserX, Shield, GraduationCap } from 'lucide-react';
import { adminService } from '../../services/api';

export default function UserManagementPage() {
    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [roleFilter, setRoleFilter] = useState('');
    const [statusFilter, setStatusFilter] = useState<boolean | undefined>(undefined);
    const [searchQuery, setSearchQuery] = useState('');
    const [updating, setUpdating] = useState<number | null>(null);

    useEffect(() => {
        loadUsers();
    }, [roleFilter, statusFilter]);

    const loadUsers = async () => {
        setLoading(true);
        try {
            const filters: any = {};
            if (roleFilter) filters.role = roleFilter;
            if (statusFilter !== undefined) filters.is_active = statusFilter;
            if (searchQuery) filters.search = searchQuery;

            const data = await adminService.getAllUsers(filters);
            setUsers(data);
        } catch (error) {
            console.error('Failed to load users:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = () => {
        loadUsers();
    };

    const handleRoleChange = async (userId: number, newRole: 'student' | 'tutor' | 'admin') => {
        if (!window.confirm(`Are you sure you want to change this user's role to "${newRole}"?`)) {
            return;
        }

        setUpdating(userId);
        try {
            await adminService.updateUserRole(userId, newRole);
            alert('Role updated successfully!');
            await loadUsers();
        } catch (error: any) {
            alert(`Failed to update role: ${error.response?.data?.detail || error.message}`);
        } finally {
            setUpdating(null);
        }
    };

    const handleStatusToggle = async (userId: number, currentStatus: boolean) => {
        const action = currentStatus ? 'suspend' : 'activate';
        if (!window.confirm(`Are you sure you want to ${action} this user?`)) {
            return;
        }

        setUpdating(userId);
        try {
            await adminService.updateUserStatus(userId, !currentStatus);
            alert(`User ${action}d successfully!`);
            await loadUsers();
        } catch (error: any) {
            alert(`Failed to ${action} user: ${error.response?.data?.detail || error.message}`);
        } finally {
            setUpdating(null);
        }
    };

    const handleDeleteUser = async (userId: number) => {
        if (!window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
            return;
        }

        setUpdating(userId);
        try {
            await adminService.deleteUser(userId);
            alert('User deleted successfully!');
            await loadUsers();
        } catch (error: any) {
            alert(`Failed to delete user: ${error.response?.data?.detail || error.message}`);
        } finally {
            setUpdating(null);
        }
    };

    const getRoleBadge = (role: string) => {
        const config: Record<string, { color: string; icon: any }> = {
            student: { color: 'bg-blue-500/10 text-blue-400', icon: GraduationCap },
            tutor: { color: 'bg-purple-500/10 text-purple-400', icon: Users },
            admin: { color: 'bg-red-500/10 text-red-400', icon: Shield }
        };

        const { color, icon: Icon } = config[role] || config.student;

        return (
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium ${color}`}>
                <Icon className="w-4 h-4" />
                {role}
            </span>
        );
    };

    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    };

    return (
        <div className="container mx-auto px-6 max-w-7xl py-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold mb-2">User Management</h1>
                <p className="text-gray-400">Manage user accounts, roles, and permissions</p>
            </div>

            {/* Filters */}
            <div className="card p-6 mb-6">
                <div className="flex items-center gap-3 mb-4">
                    <Filter className="w-5 h-5 text-primary-400" />
                    <h2 className="font-bold">Filters & Search</h2>
                </div>

                <div className="grid md:grid-cols-4 gap-4">
                    {/* Search */}
                    <div className="md:col-span-2">
                        <label className="block text-sm font-medium mb-2">Search</label>
                        <div className="flex gap-2">
                            <input
                                type="text"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                                placeholder="Username, email, name..."
                                className="input flex-1"
                            />
                            <button onClick={handleSearch} className="btn-primary px-6">
                                <Search className="w-4 h-4" />
                            </button>
                        </div>
                    </div>

                    {/* Role Filter */}
                    <div>
                        <label className="block text-sm font-medium mb-2">Role</label>
                        <select
                            value={roleFilter}
                            onChange={(e) => setRoleFilter(e.target.value)}
                            className="input w-full"
                        >
                            <option value="">All Roles</option>
                            <option value="student">Student</option>
                            <option value="tutor">Tutor</option>
                            <option value="admin">Admin</option>
                        </select>
                    </div>

                    {/* Status Filter */}
                    <div>
                        <label className="block text-sm font-medium mb-2">Status</label>
                        <select
                            value={statusFilter === undefined ? '' : String(statusFilter)}
                            onChange={(e) => setStatusFilter(e.target.value === '' ? undefined : e.target.value === 'true')}
                            className="input w-full"
                        >
                            <option value="">All Status</option>
                            <option value="true">Active</option>
                            <option value="false">Suspended</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Users Table */}
            <div className="card overflow-hidden">
                {loading ? (
                    <div className="p-12 text-center">
                        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full">
                            <thead className="bg-gray-800/50">
                                <tr>
                                    <th className="px-6 py-4 text-left text-sm font-bold">User</th>
                                    <th className="px-6 py-4 text-left text-sm font-bold">Email</th>
                                    <th className="px-6 py-4 text-left text-sm font-bold">Role</th>
                                    <th className="px-6 py-4 text-left text-sm font-bold">Status</th>
                                    <th className="px-6 py-4 text-left text-sm font-bold">Joined</th>
                                    <th className="px-6 py-4 text-left text-sm font-bold">Actions</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-700">
                                {users.map((user) => (
                                    <tr key={user.id} className="hover:bg-gray-800/30 transition-colors">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="w-10 h-10 rounded-full bg-primary-500/10 flex items-center justify-center">
                                                    <span className="font-bold text-primary-400">
                                                        {user.username.charAt(0).toUpperCase()}
                                                    </span>
                                                </div>
                                                <div>
                                                    <div className="font-medium">{user.username}</div>
                                                    {user.first_name && user.last_name && (
                                                        <div className="text-xs text-gray-500">
                                                            {user.first_name} {user.last_name}
                                                        </div>
                                                    )}
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-400">{user.email}</td>
                                        <td className="px-6 py-4">
                                            <select
                                                value={user.role}
                                                onChange={(e) => handleRoleChange(user.id, e.target.value as any)}
                                                disabled={updating === user.id}
                                                className="input text-sm py-1"
                                            >
                                                <option value="student">Student</option>
                                                <option value="tutor">Tutor</option>
                                                <option value="admin">Admin</option>
                                            </select>
                                        </td>
                                        <td className="px-6 py-4">
                                            <button
                                                onClick={() => handleStatusToggle(user.id, user.is_active)}
                                                disabled={updating === user.id}
                                                className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium transition-colors ${user.is_active
                                                    ? 'bg-green-500/10 text-green-400 hover:bg-green-500/20'
                                                    : 'bg-red-500/10 text-red-400 hover:bg-red-500/20'
                                                    }`}
                                            >
                                                {user.is_active ? (
                                                    <>
                                                        <UserCheck className="w-4 h-4" />
                                                        Active
                                                    </>
                                                ) : (
                                                    <>
                                                        <UserX className="w-4 h-4" />
                                                        Suspended
                                                    </>
                                                )}
                                            </button>
                                        </td>
                                        <td className="px-6 py-4 text-sm text-gray-400">
                                            {formatDate(user.created_at)}
                                        </td>
                                        <td className="px-6 py-4">
                                            <button
                                                onClick={() => handleDeleteUser(user.id)}
                                                disabled={updating === user.id}
                                                className="text-sm text-red-400 hover:text-red-300 transition-colors disabled:opacity-50"
                                            >
                                                Delete
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {/* Empty State */}
                        {users.length === 0 && !loading && (
                            <div className="p-12 text-center">
                                <Users className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                                <h3 className="text-xl font-bold text-gray-400 mb-2">No Users Found</h3>
                                <p className="text-gray-500">Try adjusting your filters</p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Summary */}
            <div className="mt-6 text-sm text-gray-500 text-center">
                Showing {users.length} user{users.length !== 1 ? 's' : ''}
            </div>
        </div>
    );
}
