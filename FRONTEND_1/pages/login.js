import { useState } from 'react';
import { useRouter } from 'next/router';
import {
    Button,
    TextField,
    Typography,
    Container,
    Paper,
    Box,
    Alert
} from '@mui/material';
import { loginUser } from '../utils/api';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';

export default function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const router = useRouter();
    const { login } = useAuth();

    const handleSubmit = async (event) => {
        event.preventDefault();
        setError('');

        if (isSubmitting) return;
        setIsSubmitting(true);

        try {
            const data = await loginUser({
                username,
                password
            });

            if (data.access_token) {
                login(data.access_token, { username });
                router.push('/');
            } else {
                setError(data.msg || data.error || 'Login failed. Invalid response from server.');
            }
        } catch (err) {
            console.error('Login failed:', err);
            setError(
                err?.response?.data?.msg ||
                err?.response?.data?.error ||
                'Login failed. Please check your credentials.'
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <Container component="main" maxWidth="xs">
            <motion.div
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <Paper
                    elevation={6}
                    sx={{
                        padding: 4,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        borderRadius: 3,
                        background: 'linear-gradient(135deg, #333 0%, #1a1a1a 100%)',
                        color: 'white'
                    }}
                >
                    <Typography component="h1" variant="h5" sx={{ color: 'primary.light' }}>
                        Login
                    </Typography>

                    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 1, width: '100%' }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            label="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            InputLabelProps={{ style: { color: '#B0BEC5' } }}
                            InputProps={{ style: { color: 'white' } }}
                        />

                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            label="Password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            InputLabelProps={{ style: { color: '#B0BEC5' } }}
                            InputProps={{ style: { color: 'white' } }}
                        />

                        {error && (
                            <Alert severity="error" sx={{ mt: 2 }}>
                                {error}
                            </Alert>
                        )}

                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            disabled={isSubmitting}
                            sx={{
                                mt: 3,
                                mb: 2,
                                background: 'linear-gradient(45deg, #D32F2F 30%, #FF6659 90%)'
                            }}
                        >
                            Sign In
                        </Button>

                        <Typography variant="body2" align="center">
                            Don't have an account?{' '}
                            <Button onClick={() => router.push('/signup')}>
                                Sign Up
                            </Button>
                        </Typography>
                    </Box>
                </Paper>
            </motion.div>
        </Container>
    );
}