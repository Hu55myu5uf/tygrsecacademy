import { useAuth } from '../context/AuthContext';
import { useProfilePicture } from '../context/ProfilePictureContext';
import { X, Github, Linkedin } from 'lucide-react';

interface StudentProfileHeaderProps {
    greeting?: string;
    hideProfilePicture?: boolean;
    showTierProgress?: boolean;
    currentTier?: number;
    totalPoints?: number;
}

export default function StudentProfileHeader({ greeting, hideProfilePicture = false, showTierProgress = false, currentTier = 0, totalPoints = 0 }: StudentProfileHeaderProps) {
    const { user } = useAuth();
    const { profilePicture, uploadPicture, removePicture } = useProfilePicture();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            uploadPicture(file);
        }
    };

    const defaultGreeting = `Welcome back, ${user?.first_name || user?.username}!`;

    return (
        <div className="flex items-center gap-6 mb-8">
            {!hideProfilePicture && (
                <div className="relative">
                    <div className="relative w-24 h-24">
                        {/* Outer glow effect */}
                        <div className="absolute inset-0 bg-gradient-to-br from-primary-500/20 to-purple-500/20 rounded-xl blur-lg"></div>

                        {/* Simple rounded square avatar */}
                        <div className="relative w-full h-full bg-gray-800 rounded-xl overflow-hidden border-4 border-primary-500/30 cursor-pointer group">
                            {profilePicture ? (
                                <img
                                    src={profilePicture}
                                    alt="Profile"
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <div className="w-full h-full bg-gradient-to-br from-gray-700 to-gray-800">
                                </div>
                            )}
                            {/* Upload overlay on hover */}
                            <label className="absolute inset-0 flex items-center justify-center bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity cursor-pointer">
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={handleFileChange}
                                    className="hidden"
                                />
                                <span className="text-xs text-white font-bold">Upload</span>
                            </label>

                            {/* Remove button - only show when picture exists */}
                            {profilePicture && (
                                <button
                                    onClick={removePicture}
                                    className="absolute -top-2 -right-2 bg-red-500 hover:bg-red-600 rounded-full p-1.5 transition-colors shadow-lg"
                                    title="Remove picture"
                                >
                                    <X className="w-4 h-4 text-white" />
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            )}

            {/* Welcome Text & Profile Details */}
            <div className="flex-1">
                <h2 className="text-3xl font-bold mb-2">{greeting || defaultGreeting}</h2>
                <div className="space-y-2">
                    {user?.bio && (
                        <p className="text-gray-400 max-w-2xl">{user.bio}</p>
                    )}

                    <div className="flex items-center gap-4 text-sm">
                        {(user as any).github_url && (
                            <a
                                href={(user as any).github_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-1.5 text-gray-500 hover:text-white transition-colors"
                            >
                                <Github className="w-4 h-4" />
                                <span>GitHub</span>
                            </a>
                        )}
                        {(user as any).linkedin_url && (
                            <a
                                href={(user as any).linkedin_url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-1.5 text-gray-500 hover:text-blue-400 transition-colors"
                            >
                                <Linkedin className="w-4 h-4" />
                                <span>LinkedIn</span>
                            </a>
                        )}
                        {!user?.bio && !(user as any).github_url && !(user as any).linkedin_url && (
                            <p className="text-gray-500 italic">Complete your profile in Settings to verify your identity.</p>
                        )}
                    </div>
                </div>
            </div>

            {/* Tier Progress (optional) */}
            {showTierProgress && (
                <div className="text-right">
                    {(() => {
                        const pointsPerTier = 1000;
                        const tierLabel = currentTier === 0 ? 'ZERO' : `${currentTier}`;
                        const currentTierStart = currentTier * pointsPerTier;
                        const pointsInCurrentTier = totalPoints - currentTierStart;
                        const nextTierStart = (currentTier + 1) * pointsPerTier;
                        const pointsNeeded = nextTierStart - currentTierStart;
                        const progressPercent = Math.min((pointsInCurrentTier / pointsNeeded) * 100, 100);

                        return (
                            <>
                                <div className="text-sm text-gray-400 mb-1">Tier {tierLabel}</div>
                                <div className="text-2xl font-bold text-primary-400">
                                    {pointsInCurrentTier} / {pointsPerTier}
                                </div>
                                <div className="text-xs text-gray-400 mb-2">Points to Next Tier</div>

                                {/* Mini Progress Bar */}
                                <div className="w-48">
                                    <div className="w-full bg-gray-700 rounded-full h-1.5 overflow-hidden">
                                        <div
                                            className="bg-gradient-to-r from-primary-500 to-purple-500 h-full rounded-full transition-all duration-500"
                                            style={{ width: `${progressPercent}%` }}
                                        >
                                        </div>
                                    </div>
                                </div>
                            </>
                        );
                    })()}
                </div>
            )}
        </div>
    );
}
