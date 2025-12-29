import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ProfilePictureProvider } from './context/ProfilePictureContext';
import Login from './pages/Login.tsx';
import Register from './pages/Register.tsx';
import StudentDashboard from './pages/student/Dashboard';
import TutorDashboard from './pages/tutor/Dashboard';
import AdminDashboard from './pages/admin/Dashboard';
import Landing from './pages/Landing';
import Curriculum from './pages/student/Curriculum';
import ModuleDetail from './pages/student/ModuleDetail';
import LessonView from './pages/student/LessonView';
import LabEnvironment from './pages/student/LabEnvironment';
import Labs from './pages/student/Labs';
import Challenges from './pages/student/Challenges';
import ChallengeDetail from './pages/student/ChallengeDetail';
import Leaderboard from './pages/student/Leaderboard';
import ProgressDashboard from './pages/student/ProgressDashboard';
import UserManagement from './pages/admin/UserManagement';
import CapstoneReview from './pages/tutor/CapstoneReview';
import TierLanding from './pages/TierLanding';
import Settings from './pages/student/Settings';
import PublicProfile from './pages/PublicProfile';
import CapstonesPage from './pages/student/CapstonesPage';
import CapstoneSubmissionPage from './pages/student/CapstoneSubmissionPage';
import CapstoneRequirementsPage from './pages/student/CapstoneRequirementsPage';
import CapstoneGradingQueue from './pages/tutor/CapstoneGradingQueue';
import CapstoneGradingPage from './pages/tutor/CapstoneGradingPage';
import Layout from './components/Layout';
import AdminLayout from './components/AdminLayout';
import TutorLayout from './components/TutorLayout';

function App() {
    return (
        <AuthProvider>
            <ProfilePictureProvider>
                <Router>
                    <Routes>
                        {/* Public Routes */}
                        <Route path="/" element={<Landing />} />
                        <Route path="/login" element={<Login />} />
                        <Route path="/register" element={<Register />} />
                        <Route path="/profile/:username" element={<PublicProfile />} />

                        {/* Protected Routes */}
                        <Route path="/dashboard" element={<ProtectedRoute><RoleDashboard /></ProtectedRoute>} />

                        {/* Student Routes - Also accessible by tutors and admins */}
                        <Route path="/student" element={<ProtectedRoute roles={['student', 'tutor', 'admin']}><Layout /></ProtectedRoute>}>
                            <Route path="dashboard" element={<StudentDashboard />} />
                            <Route path="curriculum" element={<Curriculum />} />
                            <Route path="modules/:moduleId" element={<ModuleDetail />} />
                            <Route path="lessons/:lessonId" element={<LessonView />} />
                            <Route path="labs" element={<Labs />} />
                            <Route path="labs/:labId" element={<LabEnvironment />} />
                            <Route path="challenges" element={<Challenges />} />
                            <Route path="challenges/:challengeId" element={<ChallengeDetail />} />
                            <Route path="leaderboard" element={<Leaderboard />} />
                            <Route path="progress" element={<ProgressDashboard />} />
                            <Route path="capstone" element={<CapstonesPage />} />
                            <Route path="capstone/:capstoneTierId" element={<CapstoneSubmissionPage />} />
                            <Route path="capstone/:capstoneTierId/requirements" element={<CapstoneRequirementsPage />} />
                            <Route path="tiers/:tierNumber" element={<TierLanding />} />
                            <Route path="settings" element={<Settings />} />
                        </Route>

                        {/* Tutor Routes */}
                        <Route path="/tutor/*" element={<ProtectedRoute roles={['tutor', 'admin']}><TutorRoutes /></ProtectedRoute>} />

                        {/* Admin Routes */}
                        <Route path="/admin/*" element={<ProtectedRoute roles={['admin']}><AdminRoutes /></ProtectedRoute>} />

                        {/* Catch all */}
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </Routes>
                </Router>
            </ProfilePictureProvider>
        </AuthProvider >
    );
}

// Protected Route Component
function ProtectedRoute({ children, roles }: { children: React.ReactNode; roles?: string[] }) {
    const { user, isAuthenticated, loading } = useAuth();

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-gray-900">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-cyan-500"></div>
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    if (roles && user && !roles.includes(user.role)) {
        return <Navigate to="/dashboard" replace />;
    }

    return <>{children}</>;
}

// Role-based Dashboard Router
function RoleDashboard() {
    const { user } = useAuth();

    if (user?.role === 'admin') {
        return <Navigate to="/admin/dashboard" replace />;
    } else if (user?.role === 'tutor') {
        return <Navigate to="/tutor/dashboard" replace />;
    } else {
        return <Navigate to="/student/dashboard" replace />;
    }
}

// Tutor route component
function TutorRoutes() {
    return (
        <Routes>
            <Route element={<TutorLayout />}>
                <Route path="dashboard" element={<TutorDashboard />} />
                <Route path="review" element={<CapstoneReview />} />
                <Route path="capstone/queue" element={<CapstoneGradingQueue />} />
                <Route path="capstone/grade/:submissionId" element={<CapstoneGradingPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/tutor/dashboard" replace />} />
        </Routes>
    );
}

// Admin route component
function AdminRoutes() {
    return (
        <Routes>
            <Route element={<AdminLayout />}>
                <Route path="dashboard" element={<AdminDashboard />} />
                <Route path="users" element={<UserManagement />} />
                <Route path="capstone/queue" element={<CapstoneGradingQueue />} />
                <Route path="capstone/grade/:submissionId" element={<CapstoneGradingPage />} />
            </Route>
            <Route path="*" element={<Navigate to="/admin/dashboard" replace />} />
        </Routes>
    );
}

export default App;
