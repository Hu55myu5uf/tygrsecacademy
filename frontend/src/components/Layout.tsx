
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Shield, LogOut, Github, Twitter, Linkedin, Heart, Settings as SettingsIcon, ArrowLeft } from 'lucide-react';

export default function Layout() {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <div className="min-h-screen bg-cyber-darker flex flex-col">
            {/* Header */}
            <header className="bg-cyber-dark border-b border-gray-700 sticky top-0 z-50">
                <div className="container mx-auto px-6 py-4 flex justify-between items-center">
                    <Link to="/" className="flex items-center gap-2 group">
                        <Shield className="w-8 h-8 text-cyber-accent group-hover:text-primary-400 transition-colors" />
                        <span className="text-xl font-bold gradient-text">TygrSecAcademy</span>
                    </Link>

                    <div className="flex items-center gap-6">
                        {/* Navigation Links (Desktop) */}
                        <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-gray-400">
                            <Link to="/student/dashboard" className="hover:text-white transition-colors">Dashboard</Link>
                            <Link to="/student/curriculum" className="hover:text-white transition-colors">Curriculum</Link>
                            <Link to="/student/labs" className="hover:text-white transition-colors">Labs</Link>
                            <Link to="/student/challenges" className="hover:text-white transition-colors">Challenges</Link>
                            <Link to="/student/capstone" className="hover:text-white transition-colors">Capstones</Link>
                            <Link to="/student/leaderboard" className="hover:text-white transition-colors">Leaderboard</Link>
                            <Link to="/student/progress" className="hover:text-white transition-colors">Progress</Link>
                        </nav>

                        <div className="h-6 w-px bg-gray-700 hidden md:block"></div>

                        <div className="flex items-center gap-4">
                            {/* Back to Admin/Tutor Button - Only for admins and tutors */}
                            {user?.role === 'admin' && (
                                <Link
                                    to="/admin/dashboard"
                                    className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-red-500/10 text-red-400 hover:bg-red-500/20 rounded-lg transition-colors text-sm font-medium"
                                >
                                    <ArrowLeft className="w-4 h-4" />
                                    Back to Admin Panel
                                </Link>
                            )}
                            {user?.role === 'tutor' && (
                                <Link
                                    to="/tutor/dashboard"
                                    className="hidden md:flex items-center gap-2 px-3 py-1.5 bg-purple-500/10 text-purple-400 hover:bg-purple-500/20 rounded-lg transition-colors text-sm font-medium"
                                >
                                    <ArrowLeft className="w-4 h-4" />
                                    Back to Tutor Panel
                                </Link>
                            )}

                            <div className="text-right hidden sm:block">
                                <p className="font-medium text-white">{user?.username}</p>
                                <p className="text-xs text-gray-400">{user?.role}</p>
                            </div>
                            <Link
                                to="/student/settings"
                                className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-400 hover:text-white"
                                title="Settings"
                            >
                                <SettingsIcon className="w-5 h-5" />
                            </Link>
                            <button
                                onClick={handleLogout}
                                className="p-2 hover:bg-gray-800 rounded-lg transition-colors text-gray-400 hover:text-white"
                                title="Sign Out"
                            >
                                <LogOut className="w-5 h-5" />
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-grow">
                <Outlet />
            </main>

            {/* Footer */}
            <footer className="bg-cyber-dark/50 border-t border-gray-800 mt-auto">
                <div className="container mx-auto px-6 py-8">
                    <div className="grid md:grid-cols-4 gap-8 mb-8">
                        <div className="col-span-1 md:col-span-2">
                            <Link to="/" className="flex items-center gap-2 mb-4">
                                <Shield className="w-6 h-6 text-gray-500" />
                                <span className="font-bold text-gray-300">TygrSecAcademy</span>
                            </Link>
                            <p className="text-gray-500 text-sm max-w-xs">
                                Empowering the next generation of cybersecurity professionals with hands-on labs and real-world scenarios.
                            </p>
                        </div>

                        <div>
                            <h4 className="font-bold text-gray-300 mb-4">Platform</h4>
                            <ul className="space-y-2 text-sm text-gray-500">
                                <li><Link to="/student/curriculum" className="hover:text-primary-400">Curriculum</Link></li>
                                <li><Link to="/student/labs" className="hover:text-primary-400">Labs</Link></li>
                                <li><Link to="/challenges" className="hover:text-primary-400">Capture The Flag</Link></li>
                            </ul>
                        </div>

                        <div>
                            <h4 className="font-bold text-gray-300 mb-4">Community</h4>
                            <div className="flex gap-4">
                                <a href="#" className="text-gray-500 hover:text-white transition-colors"><Github className="w-5 h-5" /></a>
                                <a href="#" className="text-gray-500 hover:text-blue-400 transition-colors"><Twitter className="w-5 h-5" /></a>
                                <a href="#" className="text-gray-500 hover:text-blue-600 transition-colors"><Linkedin className="w-5 h-5" /></a>
                            </div>
                        </div>
                    </div>

                    <div className="border-t border-gray-800 pt-8 flex flex-col md:flex-row justify-between items-center gap-4 text-xs text-gray-600">
                        <p>© 2025 TygrSecAcademy. All rights reserved.</p>
                        <p className="flex items-center gap-1">
                            Made with <Heart className="w-3 h-3 text-red-500 fill-red-500" /> for the security community
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}
