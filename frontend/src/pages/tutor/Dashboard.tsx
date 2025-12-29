import { Link } from 'react-router-dom';
import { Users, FileCheck, TrendingUp, GraduationCap, BookOpen } from 'lucide-react';

export default function TutorDashboard() {
    return (
        <div className="container mx-auto px-6 max-w-7xl py-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold mb-2">Tutor Dashboard</h1>
                <p className="text-gray-400">Review submissions and help students succeed</p>
            </div>

            {/* Stats Grid */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
                <div className="card p-6">
                    <Users className="w-8 h-8 text-blue-500 mb-3" />
                    <p className="text-gray-400 mb-1">Students Supervised</p>
                    <p className="text-2xl font-bold">0</p>
                </div>
                <div className="card p-6">
                    <FileCheck className="w-8 h-8 text-green-500 mb-3" />
                    <p className="text-gray-400 mb-1">Pending Reviews</p>
                    <p className="text-2xl font-bold">0</p>
                </div>
                <div className="card p-6">
                    <TrendingUp className="w-8 h-8 text-purple-500 mb-3" />
                    <p className="text-gray-400 mb-1">Reviews Completed</p>
                    <p className="text-2xl font-bold">0</p>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid md:grid-cols-3 gap-6 mb-8">
                <Link
                    to="/tutor/capstone/queue"
                    className="card p-6 hover:border-primary-500/30 transition-all group"
                >
                    <BookOpen className="w-8 h-8 text-primary-400 mb-4" />
                    <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">
                        Capstone Queue
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Review and grade student capstone projects
                    </p>
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
                    <Users className="w-8 h-8 text-gray-500 mb-4" />
                    <h3 className="text-xl font-bold mb-2 text-gray-500">
                        Student Management
                    </h3>
                    <p className="text-gray-400 text-sm">
                        Coming soon...
                    </p>
                </div>
            </div>

            {/* Additional Info */}
            <div className="card p-8">
                <h3 className="text-xl font-bold mb-3">Tutor Features</h3>
                <p className="text-gray-400">
                    As a tutor, you can review student capstone submissions, provide feedback, and help students succeed in their learning journey.
                </p>
            </div>
        </div>
    );
}
