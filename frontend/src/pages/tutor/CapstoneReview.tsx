import { useState, useEffect } from 'react';
import { FileEdit, CheckCircle, XCircle } from 'lucide-react';
import { publishingService } from '../../services/api';

interface Capstone {
    id: number;
    title: string;
    description: string;
    status: string;
    score?: number;
    submitted_at: string;
    author_id: number;
}

export default function CapstoneReview() {
    const [capstones, setCapstones] = useState<Capstone[]>([]);
    const [selectedCapstone, setSelectedCapstone] = useState<number | null>(null);
    const [feedback, setFeedback] = useState('');
    const [score, setScore] = useState(85);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadCapstones();
    }, []);

    const loadCapstones = async () => {
        try {
            const data = await publishingService.getCapstones();
            setCapstones(data.filter((c: Capstone) => c.status === 'submitted'));
        } catch (error) {
            console.error('Failed to load capstones:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleReview = async (capstoneId: number, approved: boolean) => {
        try {
            await publishingService.reviewCapstone(capstoneId, feedback, score);
            alert(`Capstone ${approved ? 'approved' : 'rejected'}`);
            loadCapstones();
            setSelectedCapstone(null);
            setFeedback('');
        } catch (error) {
            console.error('Failed to submit review:', error);
            alert('Failed to submit review');
        }
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
                <div className="flex items-center gap-3 mb-3">
                    <FileEdit className="w-10 h-10 text-primary-400" />
                    <h1 className="text-4xl font-bold">Capstone Review</h1>
                </div>
                <p className="text-gray-400">Review student capstone projects</p>
            </div>

            {/* Capstones List */}
            <div className="grid md:grid-cols-2 gap-6">
                {/* List */}
                <div className="space-y-4">
                    <h2 className="text-xl font-bold mb-4">Pending Reviews ({capstones.length})</h2>
                    {capstones.map((capstone) => (
                        <div
                            key={capstone.id}
                            onClick={() => setSelectedCapstone(capstone.id)}
                            className={`card p-4 cursor-pointer transition-all ${selectedCapstone === capstone.id
                                ? 'border-primary-500 bg-primary-500/5'
                                : 'hover:border-gray-600'
                                }`}
                        >
                            <h3 className="font-bold mb-2">{capstone.title}</h3>
                            <p className="text-sm text-gray-400 line-clamp-2">{capstone.description}</p>
                            <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                                <span>Student ID: {capstone.author_id}</span>
                                <span>Submitted: {new Date(capstone.submitted_at).toLocaleDateString()}</span>
                            </div>
                        </div>
                    ))}
                    {capstones.length === 0 && (
                        <div className="card p-8 text-center text-gray-500">
                            <FileEdit className="w-12 h-12 mx-auto mb-3 opacity-20" />
                            <p>No pending reviews</p>
                        </div>
                    )}
                </div>

                {/* Review Form */}
                {selectedCapstone && (
                    <div className="card p-6 sticky top-6">
                        <h2 className="text-xl font-bold mb-4">Review Submission</h2>

                        <div className="mb-6">
                            <label className="block text-sm font-bold mb-2">Score (0-100)</label>
                            <input
                                type="range"
                                min="0"
                                max="100"
                                value={score}
                                onChange={(e) => setScore(parseInt(e.target.value))}
                                className="w-full"
                            />
                            <div className="text-right text-2xl font-bold text-primary-400 mt-2">
                                {score}/100
                            </div>
                        </div>

                        <div className="mb-6">
                            <label className="block text-sm font-bold mb-2">Feedback</label>
                            <textarea
                                value={feedback}
                                onChange={(e) => setFeedback(e.target.value)}
                                placeholder="Provide constructive feedback..."
                                className="input min-h-32"
                                rows={6}
                            />
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={() => handleReview(selectedCapstone, true)}
                                className="btn btn-primary flex-1 flex items-center justify-center gap-2"
                            >
                                <CheckCircle className="w-4 h-4" />
                                Approve
                            </button>
                            <button
                                onClick={() => handleReview(selectedCapstone, false)}
                                className="btn btn-danger flex-1 flex items-center justify-center gap-2"
                            >
                                <XCircle className="w-4 h-4" />
                                Reject
                            </button>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}
