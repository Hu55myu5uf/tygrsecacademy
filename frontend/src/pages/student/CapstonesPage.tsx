import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Trophy, FileText, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import { capstoneService } from '../../services/api';

interface CapstoneTier {
    id: number;
    tier_id: number;
    title: string;
    description: string;
    max_score: number;
    passing_score: number;
    time_limit_hours: number | null;
    is_active: boolean;
}

interface CapstoneSubmission {
    id: number;
    capstone_tier_id: number;
    status: string;
    score: number | null;
    submitted_at: string | null;
}

export default function CapstonesPage() {
    const [tiers, setTiers] = useState<CapstoneTier[]>([]);
    const [submissions, setSubmissions] = useState<CapstoneSubmission[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [tiersData, submissionsData] = await Promise.all([
                capstoneService.getTiers(),
                capstoneService.getMySubmissions()
            ]);
            setTiers(tiersData);
            setSubmissions(submissionsData);
        } catch (error) {
            console.error('Failed to load capstone data:', error);
        } finally {
            setLoading(false);
        }
    };

    const getSubmissionForTier = (capstoneTierId: number) => {
        return submissions.find(sub => sub.capstone_tier_id === capstoneTierId);
    };

    const getStatusBadge = (status: string) => {
        const statusConfig: Record<string, { icon: any; color: string; text: string }> = {
            draft: { icon: FileText, color: 'bg-gray-500/10 text-gray-400', text: 'Draft' },
            submitted: { icon: Clock, color: 'bg-blue-500/10 text-blue-400', text: 'Submitted' },
            under_review: { icon: AlertCircle, color: 'bg-yellow-500/10 text-yellow-400', text: 'Under Review' },
            graded: { icon: CheckCircle, color: 'bg-green-500/10 text-green-400', text: 'Graded' },
            approved: { icon: CheckCircle, color: 'bg-green-500/10 text-green-400', text: 'Approved' },
            rejected: { icon: XCircle, color: 'bg-red-500/10 text-red-400', text: 'Rejected' }
        };

        const config = statusConfig[status] || statusConfig.draft;
        const Icon = config.icon;

        return (
            <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium ${config.color}`}>
                <Icon className="w-4 h-4" />
                {config.text}
            </span>
        );
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cyber-darker py-8">
            <div className="container mx-auto px-6 max-w-6xl">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center gap-3 mb-2">
                        <Trophy className="w-8 h-8 text-primary-400" />
                        <h1 className="text-3xl font-bold">Capstone Projects</h1>
                    </div>
                    <p className="text-gray-400">
                        Demonstrate your mastery with comprehensive real-world projects
                    </p>
                </div>

                {/* Capstone Tiers Grid */}
                <div className="grid gap-6 mb-8">
                    {tiers.map((tier) => {
                        const submission = getSubmissionForTier(tier.id);
                        const hasSubmission = !!submission;

                        return (
                            <div
                                key={tier.id}
                                className="card p-6 hover:border-primary-500/30 transition-all"
                            >
                                <div className="flex items-start justify-between mb-4">
                                    <div className="flex-1">
                                        <div className="flex items-center gap-3 mb-2">
                                            <h2 className="text-2xl font-bold">{tier.title}</h2>
                                            {hasSubmission && getStatusBadge(submission.status)}
                                        </div>
                                        <p className="text-gray-400 mb-4">{tier.description}</p>

                                        {/* Project Info */}
                                        <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                                            <div className="flex items-center gap-2">
                                                <Trophy className="w-4 h-4" />
                                                <span>Tier {tier.tier_id}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <FileText className="w-4 h-4" />
                                                <span>Max Score: {tier.max_score}</span>
                                            </div>
                                            <div className="flex items-center gap-2">
                                                <CheckCircle className="w-4 h-4" />
                                                <span>Passing: {tier.passing_score}</span>
                                            </div>
                                            {tier.time_limit_hours && (
                                                <div className="flex items-center gap-2">
                                                    <Clock className="w-4 h-4" />
                                                    <span>{tier.time_limit_hours}h limit</span>
                                                </div>
                                            )}
                                        </div>

                                        {/* Score Display */}
                                        {submission?.score !== null && submission?.score !== undefined && (
                                            <div className="mt-4 p-3 bg-gray-800/50 rounded-lg border border-gray-700">
                                                <div className="flex items-center justify-between">
                                                    <span className="text-gray-400">Your Score:</span>
                                                    <span className={`text-2xl font-bold ${submission.score >= tier.passing_score
                                                        ? 'text-green-400'
                                                        : 'text-red-400'
                                                        }`}>
                                                        {submission.score} / {tier.max_score}
                                                    </span>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>

                                {/* Actions */}
                                <div className="flex gap-3">
                                    <Link
                                        to={`/student/capstone/${tier.id}`}
                                        className="btn-primary flex-1 text-center"
                                    >
                                        {hasSubmission ? 'View Submission' : 'Start Project'}
                                    </Link>
                                    <Link
                                        to={`/student/capstone/${tier.id}/requirements`}
                                        className="btn-secondary"
                                    >
                                        View Requirements
                                    </Link>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* My Submissions Link */}
                {submissions.length > 0 && (
                    <div className="text-center">
                        <Link
                            to="/student/capstone/my-submissions"
                            className="text-primary-400 hover:text-primary-300 underline"
                        >
                            View All My Submissions ({submissions.length})
                        </Link>
                    </div>
                )}

                {/* Empty State */}
                {tiers.length === 0 && (
                    <div className="card p-12 text-center">
                        <Trophy className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                        <h3 className="text-xl font-bold text-gray-400 mb-2">No Capstone Projects Available</h3>
                        <p className="text-gray-500">Check back later for capstone project opportunities</p>
                    </div>
                )}
            </div>
        </div>
    );
}
