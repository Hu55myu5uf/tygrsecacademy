import { useState } from 'react';
import { Flag, CheckCircle, XCircle, Terminal } from 'lucide-react';
import { challengeService } from '../services/api';

interface ChallengeSubmissionProps {
    challengeId: number;
    onSuccess: () => void;
}

export default function ChallengeSubmission({ challengeId, onSuccess }: ChallengeSubmissionProps) {
    const [flag, setFlag] = useState('');
    const [status, setStatus] = useState<'idle' | 'submitting' | 'success' | 'error'>('idle');
    const [message, setMessage] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!flag.trim()) return;

        setStatus('submitting');
        setMessage('');

        try {
            const result = await challengeService.submitFlag(challengeId, flag);

            if (result.correct) {
                setStatus('success');
                setMessage(`Correct! You earned ${result.points_earned} points.`);
                onSuccess();
            } else {
                setStatus('error');
                setMessage('Incorrect flag. Try again!');
            }
        } catch (error: any) {
            setStatus('error');
            setMessage('Failed to submit flag. Please try again.');
        }
    };

    return (
        <div className="card bg-gray-900 border border-green-900/50 p-6 mt-8 relative overflow-hidden">
            {/* Cyberpunk accent */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-500 to-blue-600"></div>

            <h3 className="text-xl font-bold flex items-center mb-4 text-green-400">
                <Terminal className="w-5 h-5 mr-2" />
                Submit Flag
            </h3>

            <p className="text-gray-400 mb-6 text-sm">
                Enter the captured flag to verify your solution and earn points.
                Format: <code className="text-green-500 bg-black px-2 py-1 rounded">TYGR&#123;...&#125;</code>
            </p>

            <form onSubmit={handleSubmit} className="space-y-4">
                <div className="relative">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Flag className={`h-5 w-5 ${status === 'error' ? 'text-red-500' : 'text-gray-500'}`} />
                    </div>
                    <input
                        type="text"
                        value={flag}
                        onChange={(e) => setFlag(e.target.value)}
                        className={`
                            block w-full pl-10 pr-3 py-3 border rounded-md leading-5 bg-black text-white placeholder-gray-500
                            focus:outline-none focus:ring-1 sm:text-sm transition-colors
                            ${status === 'error' ? 'border-red-500 focus:border-red-500 focus:ring-red-500' : 'border-gray-700 focus:border-green-500 focus:ring-green-500'}
                            ${status === 'success' ? 'border-green-500 text-green-500' : ''}
                        `}
                        placeholder="TYGR{flag_goes_here}"
                        disabled={status === 'success' || status === 'submitting'}
                    />
                </div>

                {message && (
                    <div className={`text-sm flex items-center ${status === 'success' ? 'text-green-400' : 'text-red-400'}`}>
                        {status === 'success' ? <CheckCircle className="w-4 h-4 mr-2" /> : <XCircle className="w-4 h-4 mr-2" />}
                        {message}
                    </div>
                )}

                <div className="flex justify-end">
                    <button
                        type="submit"
                        disabled={status === 'submitting' || status === 'success'}
                        className={`
                            px-6 py-2 rounded-md text-sm font-medium focus:outline-none transition-all
                            ${status === 'success'
                                ? 'bg-green-600 text-white cursor-default'
                                : 'bg-green-600 hover:bg-green-700 text-white focus:ring-2 focus:ring-offset-2 focus:ring-green-500'}
                            disabled:opacity-50 disabled:cursor-not-allowed
                        `}
                    >
                        {status === 'submitting' ? 'Verifying...' : (status === 'success' ? 'Solved!' : 'Submit Flag')}
                    </button>
                </div>
            </form>
        </div>
    );
}
