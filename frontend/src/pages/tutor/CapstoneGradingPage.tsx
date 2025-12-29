import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, Save, CheckCircle, XCircle, Github, Globe, Video, FileText, User } from 'lucide-react';
import { capstoneService } from '../../services/api';
import ReactMarkdown from 'react-markdown';

export default function CapstoneGradingPage() {
    const { submissionId } = useParams<{ submissionId: string }>();
    const navigate = useNavigate();

    const [submission, setSubmission] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    // Grading form
    const [feedback, setFeedback] = useState('');
    const [rubricScores, setRubricScores] = useState<Record<string, number>>({});

    useEffect(() => {
        loadSubmission();
    }, [submissionId]);

    const loadSubmission = async () => {
        try {
            const data = await capstoneService.getSubmissionForGrading(parseInt(submissionId!));
            setSubmission(data);

            // Pre-fill if already graded
            if (data.feedback) {
                setFeedback(data.feedback);
            }
            if (data.rubric_evaluation) {
                setRubricScores(data.rubric_evaluation);
            }
        } catch (error) {
            console.error('Failed to load submission:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleRubricScore = (criterionName: string, points: number) => {
        setRubricScores(prev => ({
            ...prev,
            [criterionName]: points
        }));
    };

    const calculateTotalScore = () => {
        return Object.values(rubricScores).reduce((sum, points) => sum + points, 0);
    };

    const handleSubmitGrade = async (status: 'graded' | 'approved' | 'rejected') => {
        if (!feedback.trim()) {
            alert('Please provide feedback');
            return;
        }

        const totalScore = calculateTotalScore();

        if (!window.confirm(`Submit grade of ${totalScore}/100 with status "${status}"?`)) {
            return;
        }

        setSaving(true);
        try {
            await capstoneService.gradeSubmission(parseInt(submissionId!), {
                score: totalScore,
                feedback,
                rubric_evaluation: rubricScores,
                status
            });

            alert('Grade submitted successfully!');
            navigate('/tutor/capstone/queue');
        } catch (error: any) {
            alert(`Failed to submit grade: ${error.response?.data?.detail || error.message}`);
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
            </div>
        );
    }

    if (!submission) {
        return (
            <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
                <div className="text-center">
                    <FileText className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Submission Not Found</h2>
                    <Link to="/tutor/capstone/queue" className="text-primary-400 hover:text-primary-300">
                        Back to Queue
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-cyber-darker py-8">
            <div className="container mx-auto px-6 max-w-6xl">
                {/* Header */}
                <Link
                    to="/tutor/capstone/queue"
                    className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 mb-6"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Queue
                </Link>

                <div className="mb-8">
                    <div className="flex items-center justify-between mb-4">
                        <div>
                            <h1 className="text-3xl font-bold mb-2">{submission.capstone_tier_title}</h1>
                            <div className="flex items-center gap-4 text-gray-400">
                                <div className="flex items-center gap-2">
                                    <User className="w-4 h-4" />
                                    <Link
                                        to={`/profile/${submission.user_username}`}
                                        className="text-primary-400 hover:text-primary-300"
                                    >
                                        {submission.user_username}
                                    </Link>
                                </div>
                                <span>•</span>
                                <span>Submitted: {new Date(submission.submitted_at).toLocaleDateString()}</span>
                            </div>
                        </div>

                        <div className="text-right">
                            <div className="text-sm text-gray-500 mb-1">Current Score</div>
                            <div className="text-3xl font-bold text-primary-400">
                                {calculateTotalScore()}/100
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid lg:grid-cols-2 gap-6">
                    {/* Left: Submission Details */}
                    <div className="space-y-6">
                        {/* Submission Links */}
                        <div className="card p-6">
                            <h2 className="text-xl font-bold mb-4">Submission Links</h2>

                            <div className="space-y-3">
                                {submission.github_url && (
                                    <a
                                        href={submission.github_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-3 p-3 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
                                    >
                                        <Github className="w-5 h-5 text-gray-400" />
                                        <div className="flex-1">
                                            <div className="text-sm font-medium">GitHub Repository</div>
                                            <div className="text-xs text-gray-500 truncate">{submission.github_url}</div>
                                        </div>
                                    </a>
                                )}

                                {submission.documentation_url && (
                                    <a
                                        href={submission.documentation_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-3 p-3 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
                                    >
                                        <FileText className="w-5 h-5 text-gray-400" />
                                        <div className="flex-1">
                                            <div className="text-sm font-medium">Documentation</div>
                                            <div className="text-xs text-gray-500 truncate">{submission.documentation_url}</div>
                                        </div>
                                    </a>
                                )}

                                {submission.demo_url && (
                                    <a
                                        href={submission.demo_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-3 p-3 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
                                    >
                                        <Globe className="w-5 h-5 text-gray-400" />
                                        <div className="flex-1">
                                            <div className="text-sm font-medium">Live Demo</div>
                                            <div className="text-xs text-gray-500 truncate">{submission.demo_url}</div>
                                        </div>
                                    </a>
                                )}

                                {submission.video_url && (
                                    <a
                                        href={submission.video_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex items-center gap-3 p-3 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
                                    >
                                        <Video className="w-5 h-5 text-gray-400" />
                                        <div className="flex-1">
                                            <div className="text-sm font-medium">Demo Video</div>
                                            <div className="text-xs text-gray-500 truncate">{submission.video_url}</div>
                                        </div>
                                    </a>
                                )}
                            </div>
                        </div>

                        {/* Write-up */}
                        <div className="card p-6">
                            <h2 className="text-xl font-bold mb-4">Project Write-up</h2>
                            <div className="prose prose-invert max-w-none">
                                <ReactMarkdown>{submission.write_up || '*No write-up provided*'}</ReactMarkdown>
                            </div>
                        </div>
                    </div>

                    {/* Right: Grading Form */}
                    <div className="space-y-6">
                        {/* Feedback */}
                        <div className="card p-6">
                            <h2 className="text-xl font-bold mb-4">Instructor Feedback</h2>
                            <textarea
                                value={feedback}
                                onChange={(e) => setFeedback(e.target.value)}
                                placeholder="Provide detailed feedback..."
                                className="input w-full min-h-[200px]"
                            />
                        </div>

                        {/* Actions */}
                        <div className="card p-6">
                            <h2 className="text-xl font-bold mb-4">Submit Grade</h2>

                            <div className="space-y-3">
                                <button
                                    onClick={() => handleSubmitGrade('graded')}
                                    disabled={saving}
                                    className="btn-secondary w-full flex items-center justify-center gap-2"
                                >
                                    <Save className="w-4 h-4" />
                                    Save as Graded
                                </button>

                                <button
                                    onClick={() => handleSubmitGrade('approved')}
                                    disabled={saving}
                                    className="btn-primary w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700"
                                >
                                    <CheckCircle className="w-4 h-4" />
                                    Approve Submission
                                </button>

                                <button
                                    onClick={() => handleSubmitGrade('rejected')}
                                    disabled={saving}
                                    className="w-full px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors flex items-center justify-center gap-2"
                                >
                                    <XCircle className="w-4 h-4" />
                                    Reject Submission
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
