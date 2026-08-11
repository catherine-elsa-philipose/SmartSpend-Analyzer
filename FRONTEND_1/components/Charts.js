import React, { useState, useEffect } from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';
import { Typography, Box } from '@mui/material';
import api from '../utils/api';

ChartJS.register(...registerables);

const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
};

export function BarChart() {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        const fetchData = async() => {
            try {
                // ✅ USE DASHBOARD API
                const res = await api.get('/dashboard');

                const data = res.data;

                // ✅ CONVERT BACKEND DATA → BAR CHART FORMAT
                setChartData({
                    labels: data.daily_labels || [],
                    datasets: [{
                        label: 'Expenses',
                        data: data.daily_data || [],
                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    }, ],
                });
            } catch (err) {
                console.error(err);
            }
        };

        fetchData();
    }, []);

    if (!chartData) return <Typography > Loading bar chart... < /Typography>;

    return ( <
        Box sx = {
            { height: '300px' } } >
        <
        Bar data = { chartData }
        options = { chartOptions }
        /> <
        /Box>
    );
}

export function PieChart() {
    const [chartData, setChartData] = useState(null);

    useEffect(() => {
        const fetchData = async() => {
            try {
                // ✅ SAME DASHBOARD API
                const res = await api.get('/dashboard');

                const data = res.data;

                // ✅ CONVERT BACKEND DATA → PIE FORMAT
                setChartData({
                    labels: data.category_labels || [],
                    datasets: [{
                        data: data.category_data || [],
                        backgroundColor: [
                            '#FF6384',
                            '#36A2EB',
                            '#FFCE56',
                        ],
                    }, ],
                });
            } catch (err) {
                console.error(err);
            }
        };

        fetchData();
    }, []);

    if (!chartData) return <Typography > Loading pie chart... < /Typography>;

    return ( <
        Box sx = {
            { height: '300px' } } >
        <
        Pie data = { chartData }
        options = { chartOptions }
        /> <
        /Box>
    );
}