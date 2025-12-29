import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useAuth } from './AuthContext';
import { authService } from '../services/api';

interface ProfilePictureContextType {
    profilePicture: string | null;
    setProfilePicture: (picture: string | null) => void;
    uploadPicture: (file: File) => void;
    removePicture: () => void;
}

const ProfilePictureContext = createContext<ProfilePictureContextType | undefined>(undefined);

export function ProfilePictureProvider({ children }: { children: ReactNode }) {
    const { user, updateUser } = useAuth();
    const [profilePicture, setProfilePictureState] = useState<string | null>(null);

    // Generate user-specific storage key
    const getStorageKey = () => {
        return user?.id ? `tygrsec_profile_picture_user${user.id}` : null;
    };

    // Load from user.avatar_url or localStorage whenever user changes
    useEffect(() => {
        if (user?.id) {
            // User is logged in - load their picture
            if (user.avatar_url) {
                // Use avatar from database
                console.log('Loading avatar from database:', user.avatar_url.substring(0, 50));
                setProfilePictureState(user.avatar_url);
            } else {
                // Fallback to localStorage
                const storageKey = `tygrsec_profile_picture_user${user.id}`;
                const stored = localStorage.getItem(storageKey);
                if (stored) {
                    console.log('Loading avatar from localStorage');
                    setProfilePictureState(stored);
                } else {
                    setProfilePictureState(null);
                }
            }
        } else {
            // No user logged in
            setProfilePictureState(null);
        }
    }, [user?.id]); // Only re-run when user ID changes, NOT when avatar_url changes

    // Save to localStorage AND database
    const setProfilePicture = async (picture: string | null) => {
        console.log('setProfilePicture called, picture length:', picture?.length || 0);
        setProfilePictureState(picture);
        const storageKey = getStorageKey();

        // Save to localStorage
        if (storageKey) {
            if (picture) {
                localStorage.setItem(storageKey, picture);
                console.log('Saved to localStorage');
            } else {
                localStorage.removeItem(storageKey);
            }
        }

        // Save to database
        if (user) {
            try {
                console.log('Saving to database for user:', user.id);
                await authService.updateProfile({ avatar_url: picture || undefined });
                // Update the user context with new avatar
                updateUser({ ...user, avatar_url: picture || undefined });
                console.log('Successfully saved to database');
            } catch (error) {
                console.error('Failed to save avatar to database:', error);
            }
        }
    };

    const uploadPicture = (file: File) => {
        console.log('Uploading profile picture, file size:', file.size);
        const reader = new FileReader();
        reader.onloadend = () => {
            const result = reader.result as string;
            console.log('Image read complete, data URL length:', result.length);
            setProfilePicture(result);
        };
        reader.onerror = (error) => {
            console.error('Failed to read file:', error);
        };
        reader.readAsDataURL(file);
    };

    const removePicture = () => {
        setProfilePicture(null);
    };

    return (
        <ProfilePictureContext.Provider value={{ profilePicture, setProfilePicture, uploadPicture, removePicture }}>
            {children}
        </ProfilePictureContext.Provider>
    );
}

export function useProfilePicture() {
    const context = useContext(ProfilePictureContext);
    if (context === undefined) {
        throw new Error('useProfilePicture must be used within a ProfilePictureProvider');
    }
    return context;
}
