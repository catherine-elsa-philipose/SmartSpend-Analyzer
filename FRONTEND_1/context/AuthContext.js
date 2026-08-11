// frontend/context/AuthContext.js
import { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/router';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
    const [user, setUser] = useState(null); // Stores { username, isLoggedIn: true } or null
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    const fetchUser = useCallback(() => {
        setLoading(true);
        try {
            if (typeof window !== 'undefined') {
                const token = localStorage.getItem('token');
                const storedUsername = localStorage.getItem('username');
                if (token) {
                    setUser({
                        username: storedUsername || 'User',
                        isLoggedIn: true
                    });
                } else {
                    setUser(null);
                }
            }
        } catch (error) {
            console.error('Failed to fetch local auth status:', error);
            setUser(null);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchUser();
    }, [fetchUser]);

    const login = useCallback((token, userData = {}) => {
        if (typeof window !== 'undefined') {
            if (token) {
                localStorage.setItem('token', token);
            }
            if (userData.username) {
                localStorage.setItem('username', userData.username);
            }
        }
        setUser({
            username: userData.username || 'User',
            isLoggedIn: true
        });
        setLoading(false);
    }, []);

    const logout = useCallback(async () => {
        try {
            setLoading(true);
            if (typeof window !== 'undefined') {
                localStorage.removeItem('token');
                localStorage.removeItem('username');
            }
            setUser(null);
            router.push('/login');
        } catch (error) {
            console.error('Logout failed:', error);
            setUser(null);
            router.push('/login');
        } finally {
            setLoading(false);
        }
    }, [router]);

    const value = {
        user,
        loading,
        login,
        logout,
        fetchUser
    };

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};