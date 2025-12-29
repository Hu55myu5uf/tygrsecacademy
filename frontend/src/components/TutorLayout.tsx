import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Menu, X, GraduationCap, BookOpen, Users, LogOut, User as UserIcon } from 'lucide-react';

export default function TutorLayout() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-cyber-darker">
            {/* Header */}
            <header className="bg-cyber-dark border-b border-gray-700 sticky top-0 z-50">
                <div className="container mx-auto px-6">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo */}
                        <Link to="/tutor/dashboard" className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-700 rounded-lg flex items-center justify-center">
                                <Users className="w-6 h-6 text-white" />
                            </div>
                            <div>
                                <div className="font-bold text-lg">Tutor Panel</div>
                                <div className="text-xs text-gray-500">TygrSec Academy</div>
                            </div>
                        </Link>

                        <div className="flex items-center gap-6">
                            {/* Navigation Links (Desktop) */}
                            <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-400">
                                <Link to="/tutor/dashboard" className="hover:text-white transition-colors flex items-center gap-2">
                                    <Users className="w-4 h-4" />
                                    Dashboard
                                </Link>
                                <Link to="/tutor/capstone/queue" className="hover:text-white transition-colors flex items-center gap-2">
                                    <BookOpen className="w-4 h-4" />
                                    Capstone Queue
                                </Link>
                                <Link to="/student/dashboard" className="hover:text-white transition-colors flex items-center gap-2">
                                    <GraduationCap className="w-4 h-4" />
                                    Student View
                                </Link>
                            </nav>

                            <div className="h-6 w-px bg-gray-700 hidden md:block"></div>

                            {/* User Menu */}
                            <div className="flex items-center gap-4">
                                <div className="hidden md:block text-right">
                                    <div className="text-sm font-medium">{user?.username}</div>
                                    <div className="text-xs text-purple-400">Tutor</div>
                                </div>

                                <div className="w-10 h-10 rounded-full bg-purple-500/10 flex items-center justify-center">
                                    <UserIcon className="w-5 h-5 text-purple-400" />
                                </div>

                                <button
                                    onClick={handleLogout}
                                    className="hidden md:flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors"
                                >
                                    <LogOut className="w-4 h-4" />
                                    Logout
                                </button>
                            </div>

                            {/* Mobile Menu Button */}
                            <button
                                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                                className="md:hidden text-gray-400 hover:text-white"
                            >
                                {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                            </button>
                        </div>
                    </div>

                    {/* Mobile Menu */}
                    {mobileMenuOpen && (
                        <div className="md:hidden py-4 border-t border-gray-700">
                            <nav className="flex flex-col gap-4">
                                <Link
                                    to="/tutor/dashboard"
                                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    <Users className="w-4 h-4" />
                                    Dashboard
                                </Link>
                                <Link
                                    to="/tutor/capstone/queue"
                                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    <BookOpen className="w-4 h-4" />
                                    Capstone Queue
                                </Link>
                                <Link
                                    to="/student/dashboard"
                                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
                                    onClick={() => setMobileMenuOpen(false)}
                                >
                                    <GraduationCap className="w-4 h-4" />
                                    Student View
                                </Link>
                                <button
                                    onClick={handleLogout}
                                    className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors text-left"
                                >
                                    <LogOut className="w-4 h-4" />
                                    Logout
                                </button>
                            </nav>
                        </div>
                    )}
                </div>
            </header>

            {/* Main Content */}
            <main>
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="bg-cyber-dark border-t border-gray-700 mt-12">
                <div className="container mx-auto px-6 py-8">
                    <div className="grid md:grid-cols-3 gap-8">
                        {/* About */}
                        <div>
                            <h3 className="font-bold mb-3 flex items-center gap-2">
                                <Users className="w-5 h-5 text-purple-400" />
                                Tutor Panel
                            </h3>
                            <p className="text-sm text-gray-400">
                                Review student submissions and provide feedback.
                            </p>
                        </div>

                        {/* Quick Links */}
                        <div>
                            <h3 className="font-bold mb-3">Quick Links</h3>
                            <ul className="space-y-2 text-sm text-gray-400">
                                <li>
                                    <Link to="/tutor/dashboard" className="hover:text-primary-400 transition-colors">
                                        Dashboard
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/tutor/capstone/queue" className="hover:text-primary-400 transition-colors">
                                        Capstone Queue
                                    </Link>
                                </li>
                                <li>
                                    <Link to="/student/dashboard" className="hover:text-primary-400 transition-colors">
                                        Student View
                                    </Link>
                                </li>
                            </ul>
                        </div>

                        {/* Tutor Info */}
                        <div>
                            <h3 className="font-bold mb-3">Logged In As</h3>
                            <div className="text-sm">
                                <div className="text-white font-medium">{user?.username}</div>
                                <div className="text-purple-400 text-xs">Tutor</div>
                                <div className="text-gray-500 text-xs mt-1">{user?.email}</div>
                            </div>
                        </div>
                    </div>

                    <div className="mt-8 pt-6 border-t border-gray-700 text-center text-sm text-gray-500">
                        © {new Date().getFullYear()} TygrSec Academy. All rights reserved.
                    </div>
                </div>
            </footer>
        </div>
    );
}
