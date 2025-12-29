import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FileText, User, Trophy, Clock, Filter } from 'lucide-react';
import { capstoneService } from '../../services/api';

export default function CapstoneGradingQueue() {
    const [submissions, setSubmissions] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [statusFilter, setStatusFilter] = useState('submitted');
    const [tierFilter, setTierFilter] = useState<number | null>(null);

    useEffect(() => {
        loadSubmissions();
    }, [statusFilter, tierFilter]);

    const loadSubmissions = async () => {
        setLoading(true);
        try {
            const filters: any = {};
            if (statusFilter && statusFilter !== 'all') {
                filters.status_filter = statusFilter;
            }
            if (tierFilter) {
                filters.tier_id = tierFilter;
            }

            const data = await capstoneService.getAllSubmissions(filters);
            setSubmissions(data);
        } catch (error) {
            console.error('Failed to load submissions:', error);
        } finally {
            setLoading(false);
        }
    };

    const getStatusBadge = (status: string) => {
        const config: Record<string, { color: string; text: string }> = {
            draft: { color: 'bg-gray-500/10 text-gray-400', text: 'Draft' },
            submitted: { color: 'bg-blue-500/10 text-blue-400', text: 'Submitted' },
            under_review: { color: 'bg-yellow-500/10 text-yellow-400', text: 'Under Review' },
            graded: { color: 'bg-green-500/10 text-green-400', text: 'Graded' },
            approved: { color: 'bg-green-500/10 text-green-400', text: 'Approved' },
            rejected: { color: 'bg-red-500/10 text-red-400', text: 'Rejected' }
        };

        const { color, text } = config[status] || config.draft;

        return (
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${color}`}>
                {text}
            </span>
        );
    };

    const formatDate = (dateString: string) => {
        if (!dateString) return 'N/A';
        return new Date(dateString).toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    return (
        <div className="container mx-auto px-6 max-w-7xl py-8">
            {/* Header */}
            <div className="mb-8">
                <h1 className="text-3xl font-bold mb-2">Capstone Grading Queue</h1>
                <p className="text-gray-400">Review and grade student capstone submissions</p>
            </div>

            {/* Filters */}
            <div className="card p-6 mb-6">
                <div className="flex items-center gap-3 mb-4">
                    <Filter className="w-5 h-5 text-primary-400" />
                    <h2 className="font-bold">Filters</h2>
                </div>

                <div className="flex gap-4">
                    <div>
                        <label className="block text-sm font-medium mb-2">Status</label>
                        <select
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                            className="input"
                        >
                            <option value="all">All</option>
                            <option value="submitted">Submitted</option>
                            <option value="under_review">Under Review</option>
                            <option value="graded">Graded</option>
                            <option value="approved">Approved</option>
                            <option value="rejected">Rejected</option>
                        </select>
                    </div>

                    <div>
                        <label className="block text-sm font-medium mb-2">Tier</label>
                        <select
                            value={tierFilter || ''}
                            onChange={(e) => setTierFilter(e.target.value ? parseInt(e.target.value) : null)}
                            className="input"
                        >
                            <option value="">All Tiers</option>
                            <option value="1">Tier 1</option>
                            <option value="2">Tier 2</option>
                            <option value="3">Tier 3</option>
                        </select>
                    </div>
                </div>
            </div>

            {/* Submissions Table */}
            <div className="card overflow-hidden mb-6">
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead className="bg-gray-800/50">
                            <tr>
                                <th className="px-6 py-4 text-left text-sm font-bold">Student</th>
                                <th className="px-6 py-4 text-left text-sm font-bold">Project</th>
                                <th className="px-6 py-4 text-left text-sm font-bold">Status</th>
                                <th className="px-6 py-4 text-left text-sm font-bold">Submitted</th>
                                <th className="px-6 py-4 text-left text-sm font-bold">Score</th>
                                <th className="px-6 py-4 text-left text-sm font-bold">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-gray-700">
                            {submissions.map((submission) => (
                                <tr key={submission.id} className="hover:bg-gray-800/30 transition-colors">
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2">
                                            <User className="w-4 h-4 text-gray-500" />
                                            <Link
                                                to={`/profile/${submission.user_username}`}
                                                className="text-primary-400 hover:text-primary-300"
                                            >
                                                {submission.user_username}
                                            </Link>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        <div className="flex items-center gap-2">
                                            <Trophy className="w-4 h-4 text-primary-400" />
                                            <span className="font-medium">{submission.capstone_tier_title}</span>
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        {getStatusBadge(submission.status)}
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-400">
                                        <div className="flex items-center gap-2">
                                            <Clock className="w-4 h-4" />
                                            {formatDate(submission.submitted_at)}
                                        </div>
                                    </td>
                                    <td className="px-6 py-4">
                                        {submission.score !== null ? (
                                            <span className="font-bold text-green-400">
                                                {submission.score}/100
                                            </span>
                                        ) : (
                                            <span className="text-gray-500">-</span>
                                        )}
                                    </td>
                                    <td className="px-6 py-4">
                                        <Link
                                            to={`/tutor/capstone/grade/${submission.id}`}
                                            className="btn-primary text-sm px-4 py-2"
                                        >
                                            {submission.status === 'submitted' ? 'Grade' : 'View/Edit'}
                                        </Link>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>

                    {/* Empty State */}
                    {submissions.length === 0 && (
                        <div className="p-12 text-center">
                            <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                            <h3 className="text-xl font-bold text-gray-400 mb-2">No Submissions Found</h3>
                            <p className="text-gray-500">Try adjusting your filters</p>
                        </div>
                    )}
                </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-4">
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-blue-400">
                        {submissions.filter(s => s.status === 'submitted').length}
                    </div>
                    <div className="text-sm text-gray-500">Awaiting Review</div>
                </div>
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-yellow-400">
                        {submissions.filter(s => s.status === 'under_review').length}
                    </div>
                    <div className="text-sm text-gray-500">Under Review</div>
                </div>
                <div className="card p-4 text-center">
                    <div className="text-2xl font-bold text-green-400">
                        {submissions.filter(s => s.status === 'graded' || s.status === 'approved').length}
                    </div>
                    <div className="text-sm text-gray-500">Graded</div>
                </div>
            </div>
        </div>
    );
}
