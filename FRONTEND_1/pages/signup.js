import { useState } from "react";
import { useRouter } from "next/router";
import { registerUser } from "../utils/api";
import {
    Button,
    TextField,
    Typography,
    Container,
    Paper,
    Box,
    Alert
} from "@mui/material";
import { motion } from "framer-motion";

export default function Signup() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [successMsg, setSuccessMsg] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const router = useRouter();

    const handleSignup = async (e) => {
        e.preventDefault();
        setError("");
        setSuccessMsg("");

        if (isSubmitting) return;
        setIsSubmitting(true);

        try {
            const data = await registerUser({
                username,
                password,
            });

            setSuccessMsg("Signup successful! Redirecting to login...");
            setTimeout(() => {
                router.push("/login");
            }, 1500);
        } catch (err) {
            console.error("Signup error:", err);
            setError(
                err?.response?.data?.message ||
                err?.response?.data?.error ||
                "Error connecting to backend during registration."
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
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        borderRadius: 3,
                        background: "linear-gradient(135deg, #333 0%, #1a1a1a 100%)",
                        color: "white"
                    }}
                >
                    <Typography component="h1" variant="h5" sx={{ color: "primary.light" }}>
                        Sign Up
                    </Typography>

                    <Box component="form" onSubmit={handleSignup} sx={{ mt: 1, width: "100%" }}>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            label="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            InputLabelProps={{ style: { color: "#B0BEC5" } }}
                            InputProps={{ style: { color: "white" } }}
                        />

                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            label="Password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            InputLabelProps={{ style: { color: "#B0BEC5" } }}
                            InputProps={{ style: { color: "white" } }}
                        />

                        {error && (
                            <Alert severity="error" sx={{ mt: 2 }}>
                                {error}
                            </Alert>
                        )}

                        {successMsg && (
                            <Alert severity="success" sx={{ mt: 2 }}>
                                {successMsg}
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
                                background: "linear-gradient(45deg, #D32F2F 30%, #FF6659 90%)"
                            }}
                        >
                            Sign Up
                        </Button>

                        <Typography variant="body2" align="center">
                            Already have an account?{" "}
                            <Button onClick={() => router.push("/login")}>
                                Sign In
                            </Button>
                        </Typography>
                    </Box>
                </Paper>
            </motion.div>
        </Container>
    );
}