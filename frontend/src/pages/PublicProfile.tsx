import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { User, Github, Linkedin, Trophy, Award, Target, Calendar, Star, Zap, Medal } from 'lucide-react';
import { userService } from '../services/api';

interface PublicProfile {
    username: string;
    first_name?: string;
    last_name?: string;
    bio?: string;
    avatar_url?: string;
    linkedin_url?: string;
    github_url?: string;
    role: string;
    created_at: string;
    current_tier: number;
    total_points: number;
    achievements: Array<{
        name: string;
        description: string;
        icon: string;
        earned_at: string;
    }>;
}

export default function PublicProfile() {
    const { username } = useParams<{ username: string }>();
    const [profile, setProfile] = useState<PublicProfile | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        loadProfile();
    }, [username]);

    const loadProfile = async () => {
        if (!username) return;

        try {
            const data = await userService.getPublicProfile(username);
            setProfile(data);
        } catch (err: any) {
            setError(err.response?.status === 404 ? 'User not found' : 'Failed to load profile');
        } finally {
            setLoading(false);
        }
    };

    // Map icon names to Lucide components
    const getIconComponent = (iconName: string | null) => {
        const iconMap: Record<string, any> = {
            'Trophy': Trophy,
            'Award': Award,
            'Star': Star,
            'Medal': Medal,
            'Zap': Zap,
            'Target': Target,
        };

        const IconComponent = iconName ? iconMap[iconName] : Award;
        return IconComponent || Award; // Default to Award if not found
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (error || !profile) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="text-center">
                    <User className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold mb-2">{error || 'Profile not found'}</h2>
                    <Link to="/" className="text-primary-400 hover:text-primary-300">
                        Return to Home
                    </Link>
                </div>
            </div>
        );
    }

    const displayName = profile.first_name && profile.last_name
        ? `${profile.first_name} ${profile.last_name}`
        : profile.username;

    return (
        <div className="min-h-screen bg-cyber-darker py-12">
            <div className="container mx-auto px-6 max-w-4xl">
                {/* Header Card */}
                <div className="card p-8 mb-6">
                    <div className="flex items-start gap-6">
                        {/* Avatar */}
                        <div className="relative">
                            <div className="w-32 h-32 rounded-xl overflow-hidden border-4 border-primary-500/30 bg-gray-800">
                                {profile.avatar_url ? (
                                    <img
                                        src={profile.avatar_url}
                                        alt={displayName}
                                        className="w-full h-full object-cover"
                                    />
                                ) : (
                                    <div className="w-full h-full bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
                                        <User className="w-16 h-16 text-gray-600" />
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Info */}
                        <div className="flex-1">
                            <h1 className="text-3xl font-bold mb-1">{displayName}</h1>
                            <p className="text-gray-400 mb-3">@{profile.username}</p>

                            {profile.bio && (
                                <p className="text-gray-300 mb-4">{profile.bio}</p>
                            )}

                            {/* Social Links */}
                            <div className="flex gap-4 mb-4">
                                {profile.github_url && (
                                    <a
                                        href={profile.github_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors"
                                    >
                                        <Github className="w-4 h-4" />
                                        <span className="text-sm">GitHub</span>
                                    </a>
                                )}
                                {profile.linkedin_url && (
                                    <a
                                        href={profile.linkedin_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-2 px-4 py-2 bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 rounded-lg transition-colors"
                                    >
                                        <Linkedin className="w-4 h-4" />
                                        <span className="text-sm">LinkedIn</span>
                                    </a>
                                )}
                            </div>

                            {/* Metadata */}
                            <div className="flex items-center gap-4 text-sm text-gray-500">
                                <div className="flex items-center gap-1.5">
                                    <Calendar className="w-4 h-4" />
                                    <span>Joined {new Date(profile.created_at).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}</span>
                                </div>
                                <span className="px-2 py-1 bg-purple-500/10 text-purple-400 rounded text-xs uppercase font-bold">
                                    {profile.role}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Stats Grid */}
                <div className="grid grid-cols-2 gap-6 mb-6">
                    <div className="card p-6">
                        <div className="flex items-center gap-3 mb-2">
                            <Target className="w-6 h-6 text-primary-400" />
                            <h3 className="font-bold text-gray-400">Current Tier</h3>
                        </div>
                        <p className="text-3xl font-bold">Tier {profile.current_tier}</p>
                    </div>

                    <div className="card p-6">
                        <div className="flex items-center gap-3 mb-2">
                            <Trophy className="w-6 h-6 text-yellow-400" />
                            <h3 className="font-bold text-gray-400">Total Points</h3>
                        </div>
                        <p className="text-3xl font-bold text-yellow-400">{profile.total_points}</p>
                    </div>
                </div>

                {/* Achievements */}
                <div className="card p-8">
                    <div className="flex items-center gap-3 mb-6">
                        <Award className="w-6 h-6 text-primary-400" />
                        <h2 className="text-2xl font-bold">Achievements</h2>
                        <span className="ml-auto text-sm text-gray-500">{profile.achievements.length} earned</span>
                    </div>

                    {profile.achievements.length > 0 ? (
                        <div className="grid md:grid-cols-2 gap-4">
                            {profile.achievements.map((achievement, idx) => {
                                const IconComponent = getIconComponent(achievement.icon);
                                return (
                                    <div
                                        key={idx}
                                        className="p-4 bg-gray-800/50 border border-gray-700 rounded-lg hover:border-primary-500/30 transition-colors"
                                    >
                                        <div className="flex items-start gap-3">
                                            <IconComponent className="w-8 h-8 text-primary-400" />
                                            <div className="flex-1">
                                                <h3 className="font-bold mb-1">{achievement.name}</h3>
                                                <p className="text-sm text-gray-400 mb-2">{achievement.description}</p>
                                                <p className="text-xs text-gray-600">
                                                    Earned {new Date(achievement.earned_at).toLocaleDateString()}
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="text-center py-12">
                            <Award className="w-12 h-12 text-gray-600 mx-auto mb-3" />
                            <p className="text-gray-500">No achievements earned yet</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
