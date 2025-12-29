import { useParams, useNavigate, Link } from 'react-router-dom';
import { BookOpen, CheckCircle, Lock, ArrowLeft } from 'lucide-react';
import { useState, useEffect } from 'react';

// Tier display data (colors and topics only)
const tierDisplayData = {
    '0': {
        color: 'bg-blue-500',
        borderColor: 'border-blue-500',
        topics: ['Linux Fundamentals', 'Networking Basics', 'Python Scripting', 'AI Introduction', 'Security Concepts']
    },
    '1': {
        color: 'bg-purple-500',
        borderColor: 'border-purple-500',
        topics: ['ML for Network Security', 'LLMs in SOC', 'AI for Secure Coding', 'Threat Detection']
    },
    '2': {
        color: 'bg-cyan-500',
        borderColor: 'border-cyan-500',
        topics: ['Incident Response', 'Threat Intelligence', 'Web Security', 'Penetration Testing']
    },
    '3': {
        color: 'bg-green-500',
        borderColor: 'border-green-500',
        topics: ['OSINT', 'Malware Analysis', 'Adversarial ML', 'Leaderboards', 'Competitions']
    },
    '4': {
        color: 'bg-yellow-500',
        borderColor: 'border-yellow-500',
        topics: ['Capstone Projects', 'Tutor Mentorship', 'Blog Publishing', 'Portfolio Building']
    }
} as const;

interface Module {
    id: number;
    title: string;
    description: string;
    order: number;
    estimated_hours: number;
    is_published: boolean;
    lessons?: any[];
}

interface Tier {
    id: number;
    tier_number: number;
    name: string;
    description: string;
    order: number;
    is_active: boolean;
    modules: Module[];
}

export default function TierLanding() {
    const { tierNumber } = useParams();
    const navigate = useNavigate();
    const [tier, setTier] = useState<Tier | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchTierData = async () => {
            try {
                setLoading(true);
                // Fetch all tiers to find the one we need
                const response = await fetch('http://localhost:8000/api/curriculum/tiers');
                if (!response.ok) throw new Error('Failed to fetch tier data');

                const tiers = await response.json();
                const foundTier = tiers.find((t: Tier) => t.tier_number === parseInt(tierNumber || '0'));

                if (foundTier) {
                    setTier(foundTier);
                } else {
                    setError('Tier not found');
                }
            } catch (err) {
                setError('Failed to load tier data');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchTierData();
        window.scrollTo(0, 0);
    }, [tierNumber]);

    const displayData = tierDisplayData[tierNumber as keyof typeof tierDisplayData];

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-400 mx-auto mb-4"></div>
                    <p className="text-gray-400">Loading tier data...</p>
                </div>
            </div>
        );
    }

    if (error || !tier || !displayData) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="text-center">
                    <h2 className="text-3xl font-bold mb-4">Tier Not Found</h2>
                    <p className="text-gray-400 mb-6">The tier you're looking for doesn't exist.</p>
                    <button
                        onClick={() => navigate('/student/dashboard')}
                        className="btn btn-primary"
                    >
                        Back to Dashboard
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-cyber-darker via-cyber-dark to-cyber-darker">
            {/* Tier Hero */}
            <section className="py-20 px-6">
                <div className="container mx-auto max-w-5xl">
                    {/* Back to Dashboard Button */}
                    <button
                        onClick={() => navigate('/student/dashboard')}
                        className="btn btn-secondary mb-8 flex items-center gap-2"
                    >
                        <ArrowLeft className="w-4 h-4" />
                        Back to Dashboard
                    </button>

                    <div className={`${displayData.color} w-24 h-24 rounded-2xl flex items-center justify-center text-4xl font-bold mb-6`}>
                        {tierNumber}
                    </div>

                    <h1 className="text-5xl font-bold mb-4">
                        Tier {tierNumber}: <span className="gradient-text">{tier.name}</span>
                    </h1>
                    <p className="text-xl text-gray-300 mb-8 max-w-3xl">
                        {tier.description}
                    </p>

                    {/* Topics */}
                    <div className="flex flex-wrap gap-3 mb-12">
                        {displayData.topics.map((topic, idx) => (
                            <span key={idx} className={`badge text-black border-2 ${displayData.borderColor} ${displayData.color} font-bold`}>
                                {topic}
                            </span>
                        ))}
                    </div>

                    {/* CTA */}
                    <div className="flex gap-4">
                        <Link to="/student/curriculum" className="btn btn-primary btn-lg glow-primary">
                            Browse All Modules
                        </Link>
                        <button
                            onClick={() => navigate('/student/dashboard')}
                            className="btn btn-secondary btn-lg"
                        >
                            Back to Dashboard
                        </button>
                    </div>
                </div>
            </section>

            {/* Modules */}
            <section className="py-16 px-6 bg-cyber-dark/30">
                <div className="container mx-auto max-w-5xl">
                    <h2 className="text-3xl font-bold mb-8 flex items-center gap-3">
                        <BookOpen className="w-8 h-8 text-primary-400" />
                        Course Modules
                    </h2>
                    <div className="grid md:grid-cols-2 gap-6">
                        {tier.modules && tier.modules.length > 0 ? (
                            tier.modules.map((module) => (
                                <Link
                                    key={module.id}
                                    to={`/student/modules/${module.id}`}
                                    state={{ fromTier: tierNumber }}
                                    className="card p-6 hover:bg-gray-800/50 transition-all block"
                                >
                                    <div className="flex items-start justify-between mb-3">
                                        <h3 className="text-xl font-bold">{module.title}</h3>
                                        {module.is_published ? (
                                            <CheckCircle className="w-6 h-6 text-green-400" />
                                        ) : (
                                            <Lock className="w-5 h-5 text-gray-600" />
                                        )}
                                    </div>
                                    <p className="text-gray-400 text-sm mb-2">
                                        {module.lessons ? `${module.lessons.length} lessons` : 'Loading lessons...'}
                                    </p>
                                    {module.description && (
                                        <p className="text-gray-500 text-sm line-clamp-2">{module.description}</p>
                                    )}
                                </Link>
                            ))
                        ) : (
                            <div className="col-span-2 text-center py-12">
                                <p className="text-gray-400">No modules available for this tier yet.</p>
                            </div>
                        )}
                    </div>
                </div>
            </section>

            {/* Footer */}
            <footer className="bg-cyber-dark/50 border-t border-gray-800 py-8">
                <div className="container mx-auto px-6 text-center">
                    <p className="text-gray-500 text-sm">
                        Ready to continue? <Link to="/student/curriculum" className="text-primary-400 hover:text-primary-300 font-bold">View all curriculum</Link>
                    </p>
                </div>
            </footer>
        </div>
    );
}
