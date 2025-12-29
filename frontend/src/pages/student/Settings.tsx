import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';
import { authService } from '../../services/api';
import { User, Lock, Save, Github, Linkedin, AlertCircle, Calendar, MapPin, Phone, Globe } from 'lucide-react';

export default function Settings() {
    const { user, updateUser } = useAuth();
    const [activeTab, setActiveTab] = useState<'profile' | 'security'>('profile');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null);

    // Profile Form State
    const [profileData, setProfileData] = useState({
        first_name: user?.first_name || '',
        last_name: user?.last_name || '',
        bio: user?.bio || '',
        avatar_url: user?.avatar_url || '',
        linkedin_url: user ? (user as any).linkedin_url || '' : '',
        github_url: user ? (user as any).github_url || '' : '',
        date_of_birth: user ? (user as any).date_of_birth || '' : '',
        country: user ? (user as any).country || '' : '',
        city: user ? (user as any).city || '' : '',
        phone_number: user ? (user as any).phone_number || '' : ''
    });

    // Password Form State
    const [passwordData, setPasswordData] = useState({
        current_password: '',
        new_password: '',
        confirm_password: ''
    });

    const handleProfileSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setMessage(null);

        try {
            const updatedUser = await authService.updateProfile(profileData);
            updateUser(updatedUser);
            setMessage({ type: 'success', text: 'Profile updated successfully' });
        } catch (error: any) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to update profile' });
        } finally {
            setLoading(false);
        }
    };

    const handlePasswordSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (passwordData.new_password !== passwordData.confirm_password) {
            setMessage({ type: 'error', text: 'New passwords do not match' });
            return;
        }

        setLoading(true);
        setMessage(null);

        try {
            await authService.changePassword(passwordData.current_password, passwordData.new_password);
            setMessage({ type: 'success', text: 'Password changed successfully' });
            setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
        } catch (error: any) {
            setMessage({ type: 'error', text: error.response?.data?.detail || 'Failed to change password' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto px-6 py-8 max-w-4xl">
            <h1 className="text-3xl font-bold mb-8 flex items-center gap-3">
                <User className="w-8 h-8 text-primary-400" />
                Account Settings
            </h1>

            {/* Tabs */}
            <div className="flex gap-4 mb-8 border-b border-gray-700">
                <button
                    onClick={() => setActiveTab('profile')}
                    className={`pb-4 px-2 font-medium transition-colors ${activeTab === 'profile'
                        ? 'text-primary-400 border-b-2 border-primary-400'
                        : 'text-gray-400 hover:text-white'
                        }`}
                >
                    Profile Information
                </button>
                <button
                    onClick={() => setActiveTab('security')}
                    className={`pb-4 px-2 font-medium transition-colors ${activeTab === 'security'
                        ? 'text-primary-400 border-b-2 border-primary-400'
                        : 'text-gray-400 hover:text-white'
                        }`}
                >
                    Security
                </button>
            </div>

            {/* Messages */}
            {message && (
                <div className={`p-4 rounded-lg mb-6 flex items-center gap-3 ${message.type === 'success' ? 'bg-green-500/10 text-green-400 border border-green-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'
                    }`}>
                    {message.type === 'error' && <AlertCircle className="w-5 h-5" />}
                    {message.type === 'success' && <Save className="w-5 h-5" />}
                    {message.text}
                </div>
            )}

            {/* Profile Tab */}
            {activeTab === 'profile' && (
                <div className="card p-8 border border-gray-700">
                    <form onSubmit={handleProfileSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2">First Name</label>
                                <input
                                    type="text"
                                    value={profileData.first_name}
                                    onChange={(e) => setProfileData({ ...profileData, first_name: e.target.value })}
                                    className="input w-full"
                                    placeholder="Jane"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2">Last Name</label>
                                <input
                                    type="text"
                                    value={profileData.last_name}
                                    onChange={(e) => setProfileData({ ...profileData, last_name: e.target.value })}
                                    className="input w-full"
                                    placeholder="Doe"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Bio</label>
                            <textarea
                                value={profileData.bio}
                                onChange={(e) => setProfileData({ ...profileData, bio: e.target.value })}
                                className="input w-full h-32 resize-none"
                                placeholder="Tell us about yourself..."
                            />
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                                    <Calendar className="w-4 h-4" /> Date of Birth
                                </label>
                                <input
                                    type="date"
                                    value={profileData.date_of_birth}
                                    onChange={(e) => setProfileData({ ...profileData, date_of_birth: e.target.value })}
                                    className="input w-full"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                                    <Phone className="w-4 h-4" /> Phone Number
                                </label>
                                <input
                                    type="tel"
                                    value={profileData.phone_number}
                                    onChange={(e) => setProfileData({ ...profileData, phone_number: e.target.value })}
                                    className="input w-full"
                                    placeholder="+1 234 567 8900"
                                />
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                                    <Globe className="w-4 h-4" /> Country
                                </label>
                                <input
                                    type="text"
                                    value={profileData.country}
                                    onChange={(e) => setProfileData({ ...profileData, country: e.target.value })}
                                    className="input w-full"
                                    placeholder="United States"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                                    <MapPin className="w-4 h-4" /> City
                                </label>
                                <input
                                    type="text"
                                    value={profileData.city}
                                    onChange={(e) => setProfileData({ ...profileData, city: e.target.value })}
                                    className="input w-full"
                                    placeholder="New York"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Avatar URL</label>
                            <input
                                type="url"
                                value={profileData.avatar_url}
                                onChange={(e) => setProfileData({ ...profileData, avatar_url: e.target.value })}
                                className="input w-full"
                                placeholder="https://example.com/avatar.jpg"
                            />
                            <p className="text-xs text-gray-500 mt-1">Direct link to an image file</p>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                                    <Linkedin className="w-4 h-4" /> LinkedIn URL
                                </label>
                                <input
                                    type="url"
                                    value={profileData.linkedin_url}
                                    onChange={(e) => setProfileData({ ...profileData, linkedin_url: e.target.value })}
                                    className="input w-full"
                                    placeholder="https://linkedin.com/in/username"
                                />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-400 mb-2 flex items-center gap-2">
                                    <Github className="w-4 h-4" /> GitHub URL
                                </label>
                                <input
                                    type="url"
                                    value={profileData.github_url}
                                    onChange={(e) => setProfileData({ ...profileData, github_url: e.target.value })}
                                    className="input w-full"
                                    placeholder="https://github.com/username"
                                />
                            </div>
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className="btn btn-primary w-full md:w-auto"
                            >
                                {loading ? 'Saving...' : 'Save Changes'}
                            </button>
                        </div>
                    </form>
                </div>
            )}

            {/* Security Tab */}
            {activeTab === 'security' && (
                <div className="card p-8 border border-gray-700">
                    <form onSubmit={handlePasswordSubmit} className="space-y-6 max-w-md">
                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Current Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
                                <input
                                    type="password"
                                    required
                                    value={passwordData.current_password}
                                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                                    className="input w-full pl-10"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="pt-4 border-t border-gray-700">
                            <label className="block text-sm font-medium text-gray-400 mb-2">New Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
                                <input
                                    type="password"
                                    required
                                    minLength={8}
                                    value={passwordData.new_password}
                                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                                    className="input w-full pl-10"
                                    placeholder="••••••••"
                                />
                            </div>
                            <p className="text-xs text-gray-500 mt-1">Min. 8 chars, mixed case & numbers</p>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-400 mb-2">Confirm New Password</label>
                            <div className="relative">
                                <Lock className="absolute left-3 top-3 w-5 h-5 text-gray-500" />
                                <input
                                    type="password"
                                    required
                                    minLength={8}
                                    value={passwordData.confirm_password}
                                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                                    className="input w-full pl-10"
                                    placeholder="••••••••"
                                />
                            </div>
                        </div>

                        <div className="pt-4">
                            <button
                                type="submit"
                                disabled={loading}
                                className="btn btn-primary w-full"
                            >
                                {loading ? 'Updating...' : 'Update Password'}
                            </button>
                        </div>
                    </form>
                </div>
            )}
        </div>
    );
}
