import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Trophy, Target, Clock, Award, Filter, ArrowLeft } from 'lucide-react';
import { challengeService } from '../../services/api';
import StudentProfileHeader from '../../components/StudentProfileHeader';

interface Challenge {
    id: number;
    title: string;
    description: string;
    category: string;
    difficulty: string;
    base_points: number;
    solved: boolean;
    solvers_count: number;
    tags?: string[];
}

export default function Challenges() {
    const [challenges, setChallenges] = useState<Challenge[]>([]);
    const [loading, setLoading] = useState(true);
    const [categoryFilter, setCategoryFilter] = useState('');
    const [difficultyFilter, setDifficultyFilter] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        loadChallenges();
    }, [categoryFilter, difficultyFilter]);

    const loadChallenges = async () => {
        try {
            const data = await challengeService.getChallenges(categoryFilter, difficultyFilter);
            setChallenges(data);
        } catch (error) {
            console.error('Failed to load challenges:', error);
        } finally {
            setLoading(false);
        }
    };

    const getDifficultyColor = (difficulty: string) => {
        const colors: Record<string, string> = {
            easy: 'bg-green-500/10 text-green-400 border-green-500/30',
            medium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
            hard: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
            insane: 'bg-red-500/10 text-red-400 border-red-500/30'
        };
        return colors[difficulty.toLowerCase()] || 'bg-gray-500/10 text-gray-400 border-gray-500/30';
    };

    if (loading) {
        return <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
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
                <StudentProfileHeader />
                <div className="flex items-center gap-3 mb-3">
                    <Trophy className="w-10 h-10 text-primary-400" />
                    <h1 className="text-4xl font-bold">CTF Challenges</h1>
                </div>
                <p className="text-gray-400">Test your skills with capture-the-flag challenges</p>
            </div>

            {/* Filters */}
            <div className="card p-6 mb-8">
                <div className="flex items-center gap-4 flex-wrap">
                    <Filter className="w-5 h-5 text-gray-400" />
                    <select
                        value={difficultyFilter}
                        onChange={(e) => setDifficultyFilter(e.target.value)}
                        className="input"
                    >
                        <option value="">All Difficulties</option>
                        <option value="easy">Easy</option>
                        <option value="medium">Medium</option>
                        <option value="hard">Hard</option>
                        <option value="insane">Insane</option>
                    </select>
                    <select
                        value={categoryFilter}
                        onChange={(e) => setCategoryFilter(e.target.value)}
                        className="input"
                    >
                        <option value="">All Categories</option>
                        <option value="web_security">Web Security</option>
                        <option value="cryptography">Cryptography</option>
                        <option value="forensics">Forensics</option>
                        <option value="reverse_engineering">Reverse Engineering</option>
                        <option value="osint">OSINT</option>
                    </select>
                </div>
            </div>

            {/* Challenges Grid */}
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {challenges.map((challenge) => (
                    <div
                        key={challenge.id}
                        onClick={() => navigate(`/student/challenges/${challenge.id}`)}
                        className="card card-hover p-6 cursor-pointer group"
                    >
                        {/* Header */}
                        <div className="flex items-start justify-between mb-4">
                            <div className="flex-1">
                                <h3 className="text-xl font-bold mb-2 group-hover:text-primary-400 transition-colors">
                                    {challenge.title}
                                </h3>
                                <div className="flex items-center gap-2 mb-3">
                                    <span className={`text-xs px-2 py-1 rounded border ${getDifficultyColor(challenge.difficulty)}`}>
                                        {challenge.difficulty}
                                    </span>
                                    <span className="text-xs text-gray-500 uppercase">{challenge.category.replace('_', ' ')}</span>
                                </div>
                            </div>
                            {challenge.solved && (
                                <div className="bg-green-500/10 p-2 rounded-lg">
                                    <Award className="w-5 h-5 text-green-400" />
                                </div>
                            )}
                        </div>

                        {/* Description */}
                        <p className="text-gray-400 text-sm mb-4 line-clamp-2">{challenge.description}</p>

                        {/* Footer */}
                        <div className="flex items-center justify-between text-sm">
                            <div className="flex items-center gap-2 text-primary-400">
                                <Target className="w-4 h-4" />
                                <span className="font-bold">{challenge.base_points} pts</span>
                            </div>
                            <div className="flex items-center gap-2 text-gray-500">
                                <Clock className="w-4 h-4" />
                                <span>{challenge.solvers_count} solved</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {challenges.length === 0 && (
                <div className="text-center py-12">
                    <Trophy className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <h3 className="text-xl font-bold mb-2">No challenges found</h3>
                    <p className="text-gray-400">Try adjusting your filters</p>
                </div>
            )}

            {/* Quick Link to Leaderboard */}
            <div className="mt-12 text-center">
                <button
                    onClick={() => navigate('/student/leaderboard')}
                    className="btn btn-outline"
                >
                    View Leaderboard
                </button>
            </div>
        </div>
    );
}
