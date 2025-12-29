import { useState, useEffect } from 'react';
import { Trophy, Medal, Award, Search, Users } from 'lucide-react';
import { Link } from 'react-router-dom';
import { challengeService } from '../../services/api';

interface LeaderboardEntry {
    rank: number;
    username: string;
    total_points: number;
    challenge_points: number;
    challenges_solved: number;
    lesson_points: number;
    lessons_completed: number;
    module_points: number;
    modules_completed: number;
    last_solve_at?: string;
}

export default function Leaderboard() {
    const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
    const [filteredLeaderboard, setFilteredLeaderboard] = useState<LeaderboardEntry[]>([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');

    useEffect(() => {
        loadLeaderboard();
    }, []);

    useEffect(() => {
        // Filter leaderboard based on search query
        if (searchQuery.trim() === '') {
            setFilteredLeaderboard(leaderboard);
        } else {
            const filtered = leaderboard.filter(entry =>
                entry.username.toLowerCase().includes(searchQuery.toLowerCase())
            );
            setFilteredLeaderboard(filtered);
        }
    }, [searchQuery, leaderboard]);

    const loadLeaderboard = async () => {
        try {
            const data = await challengeService.getLeaderboard();
            // Sort by points descending
            const sorted = data.sort((a: LeaderboardEntry, b: LeaderboardEntry) =>
                b.total_points - a.total_points
            );
            // Assign ranks
            const ranked = sorted.map((entry: LeaderboardEntry, index: number) => ({
                ...entry,
                rank: index + 1
            }));
            setLeaderboard(ranked);
            setFilteredLeaderboard(ranked);
        } catch (error) {
            console.error('Failed to load leaderboard:', error);
        } finally {
            setLoading(false);
        }
    };

    const getRankIcon = (rank: number) => {
        if (rank === 1) return <Trophy className="w-6 h-6 text-yellow-400" />;
        if (rank === 2) return <Medal className="w-6 h-6 text-gray-400" />;
        if (rank === 3) return <Medal className="w-6 h-6 text-orange-400" />;
        return null;
    };

    const getRankColor = (rank: number) => {
        if (rank === 1) return 'bg-yellow-500/10 border-yellow-500/30';
        if (rank === 2) return 'bg-gray-500/10 border-gray-500/30';
        if (rank === 3) return 'bg-orange-500/10 border-orange-500/30';
        return 'bg-gray-800/50 border-gray-700';
    };

    if (loading) {
        return <div className="flex items-center justify-center h-96">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        </div>;
    }

    return (
        <div className="container mx-auto px-6 py-12 max-w-4xl">
            {/* Header */}
            <div className="text-center mb-8">
                <div className="flex items-center justify-center gap-3 mb-4">
                    <Trophy className="w-12 h-12 text-primary-400" />
                    <h1 className="text-4xl font-bold">Leaderboard</h1>
                </div>
                <p className="text-gray-400">Top performers in CTF challenges</p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-primary-400">{leaderboard.length}</div>
                    <div className="text-sm text-gray-500">Total Users</div>
                </div>
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-yellow-400">
                        {leaderboard[0]?.total_points || 0}
                    </div>
                    <div className="text-sm text-gray-500">Top Score</div>
                </div>
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-green-400">
                        {leaderboard.reduce((sum, entry) => sum + entry.challenges_solved, 0)}
                    </div>
                    <div className="text-sm text-gray-500">Total Solves</div>
                </div>
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-blue-400">
                        {Math.round(leaderboard.reduce((sum, entry) => sum + entry.total_points, 0) / leaderboard.length) || 0}
                    </div>
                    <div className="text-sm text-gray-500">Avg Score</div>
                </div>
            </div>

            {/* Search Bar */}
            <div className="card p-4 mb-6">
                <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-500" />
                    <input
                        type="text"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        placeholder="Search for a user..."
                        className="input w-full pl-10"
                    />
                </div>
                {searchQuery && (
                    <div className="mt-2 text-sm text-gray-400">
                        Found {filteredLeaderboard.length} result{filteredLeaderboard.length !== 1 ? 's' : ''}
                    </div>
                )}
            </div>

            {/* Leaderboard */}
            <div className="space-y-3">
                {filteredLeaderboard.length > 0 ? (
                    filteredLeaderboard.map((entry) => (
                        <div
                            key={entry.rank}
                            className={`card p-6 border ${getRankColor(entry.rank)} transition-all hover:scale-[1.02]`}
                        >
                            <div className="flex items-center gap-4">
                                {/* Rank */}
                                <div className="flex items-center justify-center w-12 shrink-0">
                                    {getRankIcon(entry.rank) || (
                                        <span className="text-2xl font-bold text-gray-500">#{entry.rank}</span>
                                    )}
                                </div>

                                {/* User Info */}
                                <div className="flex-1">
                                    <Link
                                        to={`/profile/${entry.username}`}
                                        className="font-bold text-lg hover:text-primary-400 transition-colors"
                                    >
                                        {entry.username}
                                    </Link>
                                    <div className="flex items-center gap-4 mt-1 text-sm text-gray-400">
                                        <span title="Challenges">{entry.challenges_solved || 0} challenges</span>
                                        <span title="Lessons">{entry.lessons_completed || 0} lessons</span>
                                        <span title="Modules">{entry.modules_completed || 0} modules</span>
                                        {entry.last_solve_at && (
                                            <span>
                                                Last activity: {new Date(entry.last_solve_at).toLocaleDateString()}
                                            </span>
                                        )}
                                    </div>
                                </div>

                                {/* Points Breakdown */}
                                <div className="text-right">
                                    <div className="text-2xl font-bold text-primary-400">
                                        {entry.total_points}
                                    </div>
                                    <div className="text-sm text-gray-500">total points</div>
                                    <div className="flex gap-2 mt-2 text-xs justify-end">
                                        {entry.challenge_points > 0 && (
                                            <span className="px-2 py-1 bg-yellow-500/10 text-yellow-400 rounded" title="Challenge Points">
                                                🏆 {entry.challenge_points}
                                            </span>
                                        )}
                                        {entry.lesson_points > 0 && (
                                            <span className="px-2 py-1 bg-blue-500/10 text-blue-400 rounded" title="Lesson Points (10pts each)">
                                                📖 {entry.lesson_points}
                                            </span>
                                        )}
                                        {entry.module_points > 0 && (
                                            <span className="px-2 py-1 bg-green-500/10 text-green-400 rounded" title="Module Points (50pts each)">
                                                📚 {entry.module_points}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))
                ) : (
                    <div className="card p-12 text-center">
                        <Users className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                        <h3 className="text-xl font-bold text-gray-400 mb-2">No Users Found</h3>
                        <p className="text-gray-500">
                            {searchQuery ? `No results for "${searchQuery}"` : 'No users on the leaderboard yet'}
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
