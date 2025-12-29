import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Save, Send, ArrowLeft, Github, FileText, Video, Globe, AlertCircle } from 'lucide-react';
import { capstoneService } from '../../services/api';
import ReactMarkdown from 'react-markdown';

export default function CapstoneSubmissionPage() {
    const { capstoneTierId } = useParams<{ capstoneTierId: string }>();
    const navigate = useNavigate();

    const [tier, setTier] = useState<any>(null);
    const [submission, setSubmission] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [submitting, setSubmitting] = useState(false);

    // Form fields
    const [githubUrl, setGithubUrl] = useState('');
    const [documentationUrl, setDocumentationUrl] = useState('');
    const [demoUrl, setDemoUrl] = useState('');
    const [videoUrl, setVideoUrl] = useState('');
    const [writeUp, setWriteUp] = useState('');
    const [previewMode, setPreviewMode] = useState(false);

    useEffect(() => {
        loadData();
    }, [capstoneTierId]);

    const loadData = async () => {
        try {
            // Load tier details
            const tierData = await capstoneService.getTier(parseInt(capstoneTierId!));
            setTier(tierData);

            // Try to load existing submission
            try {
                const submissions = await capstoneService.getMySubmissions();
                const existing = submissions.find((s: any) => s.capstone_tier_id === tierData.id);

                if (existing) {
                    setSubmission(existing);
                    setGithubUrl(existing.github_url || '');
                    setDocumentationUrl(existing.documentation_url || '');
                    setDemoUrl(existing.demo_url || '');
                    setVideoUrl(existing.video_url || '');
                    setWriteUp(existing.write_up || '');
                }
            } catch (err) {
                // No existing submission
            }
        } catch (error) {
            console.error('Failed to load capstone data:', error);
        } finally {
            setLoading(false);
        }
    };

    const canEdit = () => {
        if (!submission) return true;
        return submission.status === 'draft' || submission.status === 'rejected';
    };

    const handleSaveDraft = async () => {
        setSaving(true);
        try {
            const data = {
                github_url: githubUrl || null,
                documentation_url: documentationUrl || null,
                demo_url: demoUrl || null,
                video_url: videoUrl || null,
                write_up: writeUp || null,
            };

            if (submission) {
                await capstoneService.updateSubmission(submission.id, data);
                alert('Draft saved successfully!');
            } else {
                const newSubmission = await capstoneService.createSubmission(tier.id, data);
                setSubmission(newSubmission);
                alert('Draft created successfully!');
            }

            await loadData();
        } catch (error: any) {
            alert(`Failed to save draft: ${error.response?.data?.detail || error.message}`);
        } finally {
            setSaving(false);
        }
    };

    const handleSubmitFinal = async () => {
        if (!window.confirm('Are you sure you want to submit? You won\'t be able to edit after submission.')) {
            return;
        }

        setSubmitting(true);
        try {
            // First save as draft
            await handleSaveDraft();

            // Then submit
            if (submission?.id) {
                await capstoneService.submitFinal(submission.id);
                alert('Submission successful! Your project is now under review.');
                navigate('/student/capstone');
            }
        } catch (error: any) {
            alert(`Failed to submit: ${error.response?.data?.detail || error.message}`);
        } finally {
            setSubmitting(false);
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
                    <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
                    <h2 className="text-2xl font-bold mb-2">Capstone Not Found</h2>
                    <Link to="/student/capstone" className="text-primary-400 hover:text-primary-300">
                        Back to Capstones
                    </Link>
                </div>
            </div>
        );
    }

    const isReadOnly = !canEdit();

    return (
        <div className="min-h-screen bg-cyber-darker py-8">
            <div className="container mx-auto px-6 max-w-5xl">
                {/* Header */}
                <Link
                    to="/student/capstone"
                    className="inline-flex items-center gap-2 text-primary-400 hover:text-primary-300 mb-6"
                >
                    <ArrowLeft className="w-4 h-4" />
                    Back to Capstones
                </Link>

                <div className="mb-8">
                    <h1 className="text-3xl font-bold mb-2">{tier.title}</h1>
                    <p className="text-gray-400">{tier.description}</p>

                    {submission && (
                        <div className="mt-4">
                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${submission.status === 'approved' ? 'bg-green-500/10 text-green-400' :
                                    submission.status === 'graded' ? 'bg-blue-500/10 text-blue-400' :
                                        submission.status === 'rejected' ? 'bg-red-500/10 text-red-400' :
                                            'bg-gray-500/10 text-gray-400'
                                }`}>
                                Status: {submission.status}
                            </span>

                            {submission.score !== null && submission.score !== undefined && (
                                <span className="ml-4 text-lg font-bold">
                                    Score: <span className={
                                        submission.score >= tier.passing_score ? 'text-green-400' : 'text-red-400'
                                    }>
                                        {submission.score}/{tier.max_score}
                                    </span>
                                </span>
                            )}
                        </div>
                    )}
                </div>

                {/* Feedback (if graded) */}
                {submission?.feedback && (
                    <div className="card p-6 mb-6 border-blue-500/30">
                        <h3 className="text-lg font-bold mb-3 flex items-center gap-2">
                            <AlertCircle className="w-5 h-5 text-blue-400" />
                            Instructor Feedback
                        </h3>
                        <div className="prose prose-invert max-w-none">
                            <ReactMarkdown>{submission.feedback}</ReactMarkdown>
                        </div>
                    </div>
                )}

                {/* Submission Form */}
                <div className="card p-6 mb-6">
                    <h2 className="text-xl font-bold mb-6">Project Submission</h2>

                    <div className="space-y-6">
                        {/* GitHub URL */}
                        <div>
                            <label className="block text-sm font-medium mb-2">
                                <Github className="w-4 h-4 inline mr-2" />
                                GitHub Repository URL
                            </label>
                            <input
                                type="url"
                                value={githubUrl}
                                onChange={(e) => setGithubUrl(e.target.value)}
                                placeholder="https://github.com/username/repo"
                                className="input w-full"
                                disabled={isReadOnly}
                            />
                        </div>

                        {/* Documentation URL */}
                        <div>
                            <label className="block text-sm font-medium mb-2">
                                <FileText className="w-4 h-4 inline mr-2" />
                                Documentation URL (Optional)
                            </label>
                            <input
                                type="url"
                                value={documentationUrl}
                                onChange={(e) => setDocumentationUrl(e.target.value)}
                                placeholder="https://..."
                                className="input w-full"
                                disabled={isReadOnly}
                            />
                        </div>

                        {/* Demo URL */}
                        <div>
                            <label className="block text-sm font-medium mb-2">
                                <Globe className="w-4 h-4 inline mr-2" />
                                Live Demo URL (Optional)
                            </label>
                            <input
                                type="url"
                                value={demoUrl}
                                onChange={(e) => setDemoUrl(e.target.value)}
                                placeholder="https://..."
                                className="input w-full"
                                disabled={isReadOnly}
                            />
                        </div>

                        {/* Video URL */}
                        <div>
                            <label className="block text-sm font-medium mb-2">
                                <Video className="w-4 h-4 inline mr-2" />
                                Demo Video URL (YouTube, Vimeo, etc.)
                            </label>
                            <input
                                type="url"
                                value={videoUrl}
                                onChange={(e) => setVideoUrl(e.target.value)}
                                placeholder="https://youtube.com/watch?v=..."
                                className="input w-full"
                                disabled={isReadOnly}
                            />
                        </div>

                        {/* Write-up */}
                        <div>
                            <div className="flex items-center justify-between mb-2">
                                <label className="block text-sm font-medium">
                                    Project Write-up (Markdown supported)
                                </label>
                                <button
                                    onClick={() => setPreviewMode(!previewMode)}
                                    className="text-sm text-primary-400 hover:text-primary-300"
                                >
                                    {previewMode ? 'Edit' : 'Preview'}
                                </button>
                            </div>

                            {previewMode ? (
                                <div className="p-4 border border-gray-700 rounded-lg bg-gray-800/30 prose prose-invert max-w-none min-h-[300px]">
                                    <ReactMarkdown>{writeUp || '*No content*'}</ReactMarkdown>
                                </div>
                            ) : (
                                <textarea
                                    value={writeUp}
                                    onChange={(e) => setWriteUp(e.target.value)}
                                    placeholder="Describe your project, implementation, challenges faced, and solutions..."
                                    className="input w-full min-h-[300px] font-mono text-sm"
                                    disabled={isReadOnly}
                                />
                            )}
                        </div>
                    </div>
                </div>

                {/* Actions */}
                {!isReadOnly && (
                    <div className="flex gap-4">
                        <button
                            onClick={handleSaveDraft}
                            disabled={saving}
                            className="btn-secondary flex items-center gap-2"
                        >
                            <Save className="w-4 h-4" />
                            {saving ? 'Saving...' : 'Save Draft'}
                        </button>

                        <button
                            onClick={handleSubmitFinal}
                            disabled={submitting || !submission}
                            className="btn-primary flex items-center gap-2"
                        >
                            <Send className="w-4 h-4" />
                            {submitting ? 'Submitting...' : 'Submit for Review'}
                        </button>
                    </div>
                )}

                {isReadOnly && (
                    <div className="p-4 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                        <p className="text-yellow-400">
                            This submission cannot be edited because it has been {submission.status}.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
