import { useState, useEffect } from 'react';
import { BookOpen, Target, Trophy, TrendingUp } from 'lucide-react';
import { useNavigate, Link } from 'react-router-dom';
import StudentProfileHeader from '../../components/StudentProfileHeader';
import { progressService } from '../../services/progressService';

interface ProgressStats {
    total_lessons_completed: number;
    total_lessons: number;
    total_modules_completed: number;
    current_tier: number;
    total_time_minutes: number;
    completion_percentage: number;
}

export default function StudentDashboard() {
    const navigate = useNavigate();
    const [stats, setStats] = useState<ProgressStats | null>(null);

    useEffect(() => {
        loadStats();
    }, []);

    const loadStats = async () => {
        try {
            const data = await progressService.getStats();
            setStats(data);
        } catch (error) {
            console.error('Failed to load progress stats:', error);
        }
    };

    return (
        <div className="min-h-screen bg-cyber-darker">
            {/* Main Content */}
            <div className="container mx-auto px-6 py-12">
                {/* Header with Profile Picture */}
                <StudentProfileHeader />

                {/* Quick Stats */}
                <div className="grid md:grid-cols-4 gap-6 mb-12">
                    <StatCard
                        icon={<BookOpen />}
                        label="Current Tier"
                        value={`Tier ${stats?.current_tier ?? 0}`}
                        color="bg-blue-500"
                    />
                    <StatCard
                        icon={<Target />}
                        label="Lessons Completed"
                        value={`${stats?.total_lessons_completed ?? 0}/${stats?.total_lessons ?? 130}`}
                        color="bg-purple-500"
                    />
                    <StatCard
                        icon={<Trophy />}
                        label="Modules Completed"
                        value={`${stats?.total_modules_completed ?? 0}/17`}
                        color="bg-green-500"
                    />
                    <StatCard
                        icon={<TrendingUp />}
                        label="Progress"
                        value={`${Math.round(stats?.completion_percentage ?? 0)}%`}
                        color="bg-yellow-500"
                    />
                </div>

                {/* Next Steps */}
                <div className="grid md:grid-cols-2 gap-6">
                    <div className="card p-8">
                        <h3 className="text-2xl font-bold mb-4">Continue Learning</h3>
                        <p className="text-gray-400 mb-6">
                            Start with Tier 0: Foundations to build your cybersecurity knowledge.
                        </p>
                        <button
                            onClick={() => navigate('/student/curriculum')}
                            className="btn btn-primary"
                        >
                            Browse Curriculum
                        </button>
                    </div>

                    <div className="card p-8">
                        <h3 className="text-2xl font-bold mb-4">Practice Labs</h3>
                        <p className="text-gray-400 mb-6">
                            Get hands-on experience with AI-assisted cybersecurity labs.
                        </p>
                        <button
                            onClick={() => navigate('/student/challenges')}
                            className="btn btn-primary"
                        >
                            View Labs
                        </button>
                    </div>
                </div>

                {/* 5-Tier Learning Path */}
                <div className="mt-12">
                    <h3 className="text-3xl font-bold text-center mb-8">
                        <span className="gradient-text">Your Learning Path</span>
                    </h3>
                    <div className="space-y-4 max-w-4xl mx-auto">
                        <TierCard
                            tier="0"
                            title="Foundations"
                            topics={['Linux Basics', 'Networking', 'Python', 'AI Fundamentals']}
                            color="bg-blue-500"
                        />
                        <TierCard
                            tier="1"
                            title="AI in Cybersecurity"
                            topics={['ML for Network Security', 'LLMs for SOC', 'AI for Secure Coding']}
                            color="bg-purple-500"
                        />
                        <TierCard
                            tier="2"
                            title="Hands-on Labs"
                            topics={['Incident Response', 'Threat Intelligence', 'Web Security Labs']}
                            color="bg-cyan-500"
                        />
                        <TierCard
                            tier="3"
                            title="CTF Challenges"
                            topics={['OSINT', 'Malware Analysis', 'Adversarial ML', 'Leaderboards']}
                            color="bg-green-500"
                        />
                        <TierCard
                            tier="4"
                            title="Mastery & Publishing"
                            topics={['Capstone Projects', 'Tutor Supervision', 'Blog Publishing']}
                            color="bg-yellow-500"
                        />
                    </div>
                </div>
            </div>
        </div>
    );
}

function StatCard({ icon, label, value, color }: any) {
    return (
        <div className="card card-hover p-6">
            <div className={`${color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                {icon}
            </div>
            <p className="text-gray-400 text-sm mb-1">{label}</p>
            <p className="text-2xl font-bold">{value}</p>
        </div>
    );
}

function TierCard({ tier, title, topics, color }: { tier: string; title: string; topics: string[]; color: string }) {
    return (
        <Link to={`/student/tiers/${tier}`} className="card card-hover p-6 flex items-center gap-6 group transition-all">
            <div className={`${color} w-16 h-16 rounded-lg flex items-center justify-center text-2xl font-bold shrink-0 group-hover:scale-110 transition-transform`}>
                {tier}
            </div>
            <div className="flex-1">
                <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">Tier {tier}: {title}</h3>
                <div className="flex flex-wrap gap-2">
                    {topics.map((topic, idx) => (
                        <span key={idx} className="badge badge-primary">{topic}</span>
                    ))}
                </div>
            </div>
        </Link>
    );
}
