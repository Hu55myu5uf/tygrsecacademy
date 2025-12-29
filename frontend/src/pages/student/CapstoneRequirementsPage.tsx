import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, FileText, Trophy, Clock, CheckCircle, Target } from 'lucide-react';
import { capstoneService } from '../../services/api';
import ReactMarkdown from 'react-markdown';

export default function CapstoneRequirementsPage() {
    const { capstoneTierId } = useParams<{ capstoneTierId: string }>();
    const [tier, setTier] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadTier();
    }, [capstoneTierId]);

    const loadTier = async () => {
        try {
            const tierData = await capstoneService.getTier(parseInt(capstoneTierId!));
            setTier(tierData);
        } catch (error) {
            console.error('Failed to load capstone tier:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (!tier) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="text-center">
                    <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Capstone Not Found</h2>
                    <Link to="/student/capstone" className="text-primary-400 hover:text-primary-300">
                        Back to Capstones
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cyber-darker py-8">
            <div className="container mx-auto px-6 max-w-4xl">
                {/* Header */}
                <Link
                    to="/student/capstone"
                    className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 mb-6"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Capstones
                </Link>

                <div className="mb-8">
                    <div className="flex items-center gap-3 mb-2">
                        <Trophy className="w-8 h-8 text-primary-400" />
                        <h1 className="text-3xl font-bold">{tier.title}</h1>
                    </div>
                    <p className="text-gray-400 text-lg">{tier.description}</p>
                </div>

                {/* Requirements */}
                <div className="card p-6 mb-6">
                    <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                        <FileText className="w-6 h-6 text-primary-400" />
                        Project Requirements
                    </h2>
                    <div className="prose prose-invert max-w-none">
                        <ReactMarkdown>{tier.requirements}</ReactMarkdown>
                    </div>
                </div>

                {/* Deliverables */}
                <div className="card p-6 mb-6">
                    <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                        <Target className="w-6 h-6 text-primary-400" />
                        Required Deliverables
                    </h2>
                    <ul className="space-y-2">
                        {tier.deliverables.map((deliverable: string, idx: number) => (
                            <li key={idx} className="flex items-start gap-3">
                                <CheckCircle className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                                <span className="text-gray-300">{deliverable}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                {/* Grading Rubric */}
                <div className="card p-6 mb-6">
                    <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                        <Trophy className="w-6 h-6 text-primary-400" />
                        Grading Rubric
                    </h2>

                    <div className="space-y-4">
                        {tier.rubric.criteria.map((criterion: any, idx: number) => (
                            <div key={idx} className="p-4 bg-gray-800/50 border border-gray-700 rounded-lg">
                                <div className="flex items-start justify-between mb-2">
                                    <h3 className="font-bold text-lg">{criterion.name}</h3>
                                    <span className="text-primary-400 font-bold">{criterion.max_points} pts</span>
                                </div>
                                <p className="text-gray-400 text-sm">{criterion.description}</p>
                            </div>
                        ))}
                    </div>

                    <div className="mt-6 p-4 bg-primary-500/10 border border-primary-500/30 rounded-lg">
                        <div className="flex items-center justify-between">
                            <span className="font-bold">Total Points</span>
                            <span className="text-2xl font-bold text-primary-400">{tier.max_score}</span>
                        </div>
                        <div className="flex items-center justify-between mt-2 text-sm">
                            <span className="text-gray-400">Passing Score</span>
                            <span className="text-green-400 font-bold">{tier.passing_score}+</span>
                        </div>
                    </div>
                </div>

                {/* Time Limit */}
                {tier.time_limit_hours && (
                    <div className="card p-6 mb-6 border-yellow-500/30">
                        <div className="flex items-center gap-3">
                            <Clock className="w-6 h-6 text-yellow-400" />
                            <div>
                                <h3 className="font-bold">Time Limit</h3>
                                <p className="text-gray-400">
                                    You have {tier.time_limit_hours} hours to complete this project after starting
                                </p>
                            </div>
                        </div>
                    </div>
                )}

                {/* Action Button */}
                <div className="text-center">
                    <Link
                        to={`/student/capstone/${tier.id}`}
                        className="btn-primary inline-block"
                    >
                        Start Project
                    </Link>
                </div>
            </div>
        </div>
    );
}
