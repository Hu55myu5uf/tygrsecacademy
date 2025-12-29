import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Users, BookOpen, Trophy, Activity, UserCheck, UserX, GraduationCap } from 'lucide-react';
import { adminService } from '../../services/api';

export default function AdminDashboardHome() {
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadStats();
    }, []);

    const loadStats = async () => {
        try {
            const data = await adminService.getPlatformStats();
            setStats(data);
        } catch (error) {
            console.error('Failed to load stats:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-6 max-w-7xl py-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold mb-2">Admin Dashboard</h1>
                <p className="text-gray-400">Platform overview and management</p>
            </div>

            {/* Stats Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                {/* Total Users */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="p-3 bg-primary-500/10 rounded-lg">
                            <Users className="w-6 h-6 text-primary-400" />
                        </div>
                        <span className="text-xs text-gray-500">Total</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stats?.users?.total || 0}</div>
                    <div className="text-sm text-gray-400">Total Users</div>
                    <div className="mt-2 text-xs text-green-400">
                        +{stats?.users?.new_30d || 0} this month
                    </div>
                </div>

                {/* Active Users */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="p-3 bg-green-500/10 rounded-lg">
                            <UserCheck className="w-6 h-6 text-green-400" />
                        </div>
                        <span className="text-xs text-gray-500">Active</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stats?.users?.active || 0}</div>
                    <div className="text-sm text-gray-400">Active Users</div>
                    <div className="mt-2 text-xs text-gray-500">
                        {stats?.users?.total - stats?.users?.active || 0} suspended
                    </div>
                </div>

                {/* Students */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="p-3 bg-blue-500/10 rounded-lg">
                            <GraduationCap className="w-6 h-6 text-blue-400" />
                        </div>
                        <span className="text-xs text-gray-500">Students</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stats?.users?.students || 0}</div>
                    <div className="text-sm text-gray-400">Students</div>
                    <div className="mt-2 text-xs text-gray-500">
                        {stats?.users?.tutors || 0} tutors, {stats?.users?.admins || 0} admins
                    </div>
                </div>

                {/* Engagement */}
                <div className="card p-6">
                    <div className="flex items-center justify-between mb-4">
                        <div className="p-3 bg-yellow-500/10 rounded-lg">
                            <Activity className="w-6 h-6 text-yellow-400" />
                        </div>
                        <span className="text-xs text-gray-500">Engagement</span>
                    </div>
                    <div className="text-3xl font-bold mb-1">{stats?.engagement?.lessons_completed || 0}</div>
                    <div className="text-sm text-gray-400">Lessons Completed</div>
                    <div className="mt-2 text-xs text-gray-500">
                        {stats?.engagement?.challenges_completed || 0} challenges solved
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid md:grid-cols-4 gap-6 mb-8">
                <Link
                    to="/admin/users"
                    className="card p-6 hover:border-primary-500/30 transition-all group"
                >
                    <Users className="w-8 h-8 text-primary-400 mb-4" />
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">
                        User Management
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Manage user accounts, roles, and permissions
                    </p>
                </Link>

                <Link
                    to="/admin/capstone/queue"
                    className="card p-6 hover:border-primary-500/30 transition-all group"
                >
                    <Trophy className="w-8 h-8 text-primary-400 mb-4" />
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">
                        Capstone Grading
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Review and grade student capstone projects
                    </p>
                    {stats?.capstones?.pending_review > 0 && (
                        <div className="mt-3 inline-block px-3 py-1 bg-yellow-500/10 text-yellow-400 rounded-full text-sm">
                            {stats.capstones.pending_review} pending
                        </div>
                    )}
                </Link>

                <Link
                    to="/student/dashboard"
                    className="card p-6 hover:border-primary-500/30 transition-all group"
                >
                    <GraduationCap className="w-8 h-8 text-blue-400 mb-4" />
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">
                        Student View
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Access the platform as a student
                    </p>
                </Link>

                <div className="card p-6 opacity-60">
                    <BookOpen className="w-8 h-8 text-gray-500 mb-4" />
                    <h3 className="text-xl font-bold mb-2 text-gray-500">
                        Content Management
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Coming soon...
                    </p>
                </div>
            </div>

            {/* Recent Activity */}
            <div className="card p-6">
                <h2 className="text-xl font-bold mb-4">Platform Statistics</h2>

                <div className="grid md:grid-cols-3 gap-6">
                    <div className="p-4 bg-gray-800/50 rounded-lg">
                        <div className="text-sm text-gray-400 mb-1">Capstone Submissions</div>
                        <div className="text-2xl font-bold">{stats?.capstones?.total_submissions || 0}</div>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg">
                        <div className="text-sm text-gray-400 mb-1">Challenges Completed</div>
                        <div className="text-2xl font-bold">{stats?.engagement?.challenges_completed || 0}</div>
                    </div>

                    <div className="p-4 bg-gray-800/50 rounded-lg">
                        <div className="text-sm text-gray-400 mb-1">Lessons Completed</div>
                        <div className="text-2xl font-bold">{stats?.engagement?.lessons_completed || 0}</div>
                    </div>
                </div>
            </div>
        </div>
    );
}
