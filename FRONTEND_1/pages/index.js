import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../context/AuthContext';
import { Typography, Box, CircularProgress, Paper, Grid, Card, CardContent, Alert } from '@mui/material';
import { getSpendingSummary, getForecast } from '../utils/api';
import { BarChart, PieChart } from '../components/Charts';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

export default function Home() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [summary, setSummary] = useState(null);
  const [forecast, setForecast] = useState(null);
  const [dataLoading, setDataLoading] = useState(true);
  const [dataError, setDataError] = useState('');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);

    if (!loading && (!user || !user.isLoggedIn)) {
      router.push('/login');
    }

    const fetchData = async () => {
      if (user && user.isLoggedIn) {
        setDataLoading(true);
        setDataError('');
        try {
          const [summaryRes, forecastRes] = await Promise.all([
            getSpendingSummary().catch(() => null),
            getForecast(6).catch(() => null),
          ]);
          setSummary(summaryRes);
          setForecast(forecastRes);
        } catch (err) {
          console.error('Failed to fetch dashboard data:', err);
          setDataError('Failed to load dashboard data. Please try again.');
        } finally {
          setDataLoading(false);
        }
      }
    };

    if (!loading) {
      fetchData();
    }
  }, [user, loading, router]);

  if (loading || dataLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          {loading ? 'Checking authentication...' : 'Loading dashboard data...'}
        </Typography>
      </Box>
    );
  }

  if (!user || !user.isLoggedIn) {
    return null;
  }

  const categoryEntries = summary?.by_category ? Object.entries(summary.by_category) : [];

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom sx={{ mb: 2 }}>
        Welcome, {user.username || 'User'}!
      </Typography>

      {dataError && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {dataError}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Spending Summary */}
        <Grid item xs={12} md={6} lg={4}>
          <Card elevation={3} sx={{
            height: '100%',
            background: 'linear-gradient(45deg, #D32F2F 30%, #B0BEC5 90%)',
            color: 'white',
            transition: 'transform 0.3s ease-in-out',
            '&:hover': { transform: 'scale(1.02)' }
          }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Overall Spending Summary
              </Typography>
              {summary ? (
                <Box>
                  <Typography variant="h4" sx={{ fontWeight: 'bold', my: 1 }}>
                    ${summary.total_spent?.toFixed(2) || '0.00'}
                  </Typography>
                  <Typography variant="body1">Total Receipts: {summary.transaction_count ?? 0}</Typography>
                  <Typography variant="body1">Period: {summary.period || 'all_time'}</Typography>
                  {summary.message && (
                    <Typography variant="body2" sx={{ mt: 1, opacity: 0.9 }}>
                      {summary.message}
                    </Typography>
                  )}
                </Box>
              ) : (
                <Typography>No spending summary available.</Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Bar Chart */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper elevation={3} sx={{ p: 2, height: '100%', transition: 'transform 0.3s ease-in-out', '&:hover': { transform: 'scale(1.02)' } }}>
            <Typography variant="h6" gutterBottom align="center">
              Daily Spending Trends
            </Typography>
            {isClient && <BarChart />}
          </Paper>
        </Grid>

        {/* Pie Chart */}
        <Grid item xs={12} md={6} lg={4}>
          <Paper elevation={3} sx={{ p: 2, height: '100%', transition: 'transform 0.3s ease-in-out', '&:hover': { transform: 'scale(1.02)' } }}>
            <Typography variant="h6" gutterBottom align="center">
              Spending Categories
            </Typography>
            {isClient && <PieChart />}
          </Paper>
        </Grid>

        {/* Spending by Category & Forecast Breakdown */}
        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, mt: 3, transition: 'transform 0.3s ease-in-out', '&:hover': { transform: 'scale(1.01)' } }}>
            <Typography variant="h5" component="h2" gutterBottom>
              Category Breakdown
            </Typography>
            {categoryEntries.length > 0 ? (
              <Box>
                {categoryEntries.map(([cat, amt]) => (
                  <Box key={cat} sx={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px dashed #eee', py: 1 }}>
                    <Typography variant="body1">{cat}</Typography>
                    <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                      ${amt?.toFixed(2) || '0.00'}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography>No category data found. Upload receipts to populate spending categories!</Typography>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper elevation={3} sx={{ p: 3, mt: 3, transition: 'transform 0.3s ease-in-out', '&:hover': { transform: 'scale(1.01)' } }}>
            <Typography variant="h5" component="h2" gutterBottom>
              6-Month Spending Forecast
            </Typography>
            {forecast?.success && forecast?.forecast_months?.length > 0 ? (
              <Box>
                {forecast.forecast_months.map((m, idx) => (
                  <Box key={m} sx={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px dashed #eee', py: 1 }}>
                    <Typography variant="body1">{m}</Typography>
                    <Typography variant="body1" sx={{ fontWeight: 'bold', color: 'primary.main' }}>
                      ${forecast.forecast_amounts[idx]?.toFixed(2) || '0.00'}
                    </Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography>{forecast?.message || 'Upload receipts to generate historical expense forecasts.'}</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}
