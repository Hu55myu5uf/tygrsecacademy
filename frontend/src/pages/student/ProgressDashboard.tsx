import { useState, useEffect } from 'react';
import { TrendingUp, BookOpen, Target, Trophy, Award, Clock, ArrowLeft } from 'lucide-react';
import { progressService } from '../../services/api';
import { useNavigate } from 'react-router-dom';
import StudentProfileHeader from '../../components/StudentProfileHeader';

interface ProgressData {
    overall: {
        current_tier: number;
        modules_completed: number;
        labs_completed: number;
        challenges_solved: number;
        total_points: number;
        total_achievements: number;
        total_time_minutes: number;
    };
    modules: Array<{
        module_id: number;
        title: string;
        completion_percent: number;
        is_completed: boolean;
        lessons_completed: number;
        time_spent_minutes: number;
    }>;
    achievements: Array<{
        name: string;
        description: string;
        icon_url?: string;
        earned_at: string;
    }>;
}

export default function ProgressDashboard() {
    const [progress, setProgress] = useState<ProgressData | null>(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        loadProgress();
    }, []);

    const loadProgress = async () => {
        try {
            const data = await progressService.getMyProgress();
            setProgress(data);
        } catch (error) {
            console.error('Failed to load progress:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        </div>;
    }

    if (!progress) {
        return <div className="container mx-auto px-6 py-12 text-center">
            <h2 className="text-2xl font-bold">Failed to load progress</h2>
        </div>;
    }

    return (
        <div className="container mx-auto px-6 py-12">
            {/* Header */}
            <div className="mb-8">
                <button
                    onClick={() => navigate('/student/dashboard')}
                    className="btn btn-secondary mb-4 flex items-center gap-2"
                >
                    <ArrowLeft className="w-4 h-4" />
                </button>
                <StudentProfileHeader
                    showTierProgress={true}
                    currentTier={progress.overall.current_tier}
                    totalPoints={progress.overall.total_points}
                />
                <div className="flex items-center gap-3 mb-3">
                    <TrendingUp className="w-10 h-10 text-primary-400" />
                    <h1 className="text-4xl font-bold">My Progress</h1>
                </div>
                <p className="text-gray-400">Track your learning journey</p>
            </div>


            {/* Stats Cards */}
            <div className="grid md:grid-cols-4 gap-6 mb-12">
                <div className="card p-6">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="bg-blue-500 w-12 h-12 rounded-lg flex items-center justify-center">
                            <BookOpen className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-gray-400 text-sm">Current Tier</p>
                            <p className="text-3xl font-bold">Tier {progress.overall.current_tier}</p>
                        </div>
                    </div>
                </div>

                <div className="card p-6">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="bg-green-500 w-12 h-12 rounded-lg flex items-center justify-center">
                            <Target className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-gray-400 text-sm">Modules</p>
                            <p className="text-3xl font-bold">{progress.overall.modules_completed}</p>
                        </div>
                    </div>
                </div>

                <div className="card p-6">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="bg-purple-500 w-12 h-12 rounded-lg flex items-center justify-center">
                            <Trophy className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-gray-400 text-sm">Challenges</p>
                            <p className="text-3xl font-bold">{progress.overall.challenges_solved}</p>
                        </div>
                    </div>
                </div>

                <div className="card p-6">
                    <div className="flex items-center gap-3 mb-3">
                        <div className="bg-yellow-500 w-12 h-12 rounded-lg flex items-center justify-center">
                            <Award className="w-6 h-6" />
                        </div>
                        <div>
                            <p className="text-gray-400 text-sm">Total Points</p>
                            <p className="text-3xl font-bold">{progress.overall.total_points}</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Module Progress */}
            <div className="card p-8 mb-8">
                <h2 className="text-2xl font-bold mb-6">Module Progress</h2>
                <div className="space-y-4">
                    {progress.modules.map((module) => (
                        <div key={module.module_id} className="bg-gray-800/30 rounded-lg p-4">
                            <div className="flex items-center justify-between mb-3">
                                <div className="flex flex-col">
                                    <span className="text-sm text-gray-400">Module {module.module_id}</span>
                                    <span className="font-bold text-lg">{module.title}</span>
                                </div>
                                <span className="text-primary-400 font-bold">{module.completion_percent.toFixed(0)}%</span>
                            </div>
                            <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                                <div
                                    className="bg-gradient-to-r from-primary-500 to-primary-400 h-full transition-all"
                                    style={{ width: `${module.completion_percent}%` }}
                                />
                            </div>
                            <div className="flex items-center gap-4 mt-3 text-sm text-gray-400">
                                <span>{module.lessons_completed} lessons completed</span>
                                <span className="flex items-center gap-1">
                                    <Clock className="w-4 h-4" />
                                    {module.time_spent_minutes} minutes
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Achievements */}
            <div className="card p-8">
                <h2 className="text-2xl font-bold mb-6">Achievements</h2>
                {progress.achievements.length > 0 ? (
                    <div className="grid md:grid-cols-3 gap-4">
                        {progress.achievements.map((achievement, idx) => (
                            <div key={idx} className="bg-gray-800/30 rounded-lg p-4 border border-yellow-500/20">
                                <div className="flex items-center gap-3 mb-2">
                                    <Award className="w-8 h-8 text-yellow-400" />
                                    <div>
                                        <h3 className="font-bold">{achievement.name}</h3>
                                        <p className="text-xs text-gray-400">
                                            {new Date(achievement.earned_at).toLocaleDateString()}
                                        </p>
                                    </div>
                                </div>
                                <p className="text-sm text-gray-400">{achievement.description}</p>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="text-center py-8 text-gray-500">
                        <Award className="w-12 h-12 mx-auto mb-3 opacity-20" />
                        <p>No achievements yet. Keep learning!</p>
                    </div>
                )}
            </div>
        </div >
    );
}
