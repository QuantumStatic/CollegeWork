import { useState } from "react";
import React from "react";
import axios from "axios";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { Link, useNavigate } from "react-router-dom";

import "../styles/ranking.css";

export function Ranking() {
    const [start, setStart] = useState(new Date());
    const [end, setEnd] = useState("");
    const [response, setResponse] = useState(null);
    const [error, setError] = useState();
    const [loading, setLoading] = useState(false)
    const nav = useNavigate();

    const handleClick = async(event) => {
        event.preventDefault();
        setLoading(true);
        setError(null);
        setResponse(null);
        const start_date = new Date(start).toISOString().split("T")[0];
        const end_date = new Date(end).toISOString().split("T")[0];
        const formData = new FormData();
        formData.append("start", start_date);
        formData.append("end", end_date);
        try {
            const response = await axios.post(
                "http://127.0.0.1:5000/api/rank",
                formData,
                {
                  headers: {
                    "Content-Type": "multipart/form-data",
                  },
                  withCredentials: true,
                }
              );
            setResponse(response.data)
        } catch (error) {
            if (error.response) {
                setError(error.response.data.error);
            }else{
                nav("/");
            }
            
        }finally{
            setLoading(false);
        }
    }

return (
    <>
        <div className="ranking-container">
            <div className="ranking-top-bar">
                <Link to="/" className="ranking-home-link">Home</Link>
                <h1 className="ranking-heading">Ranking</h1>
            </div>
            <div className="ranking-card">
                <form onSubmit={handleClick} className="ranking-form">
                    <label htmlFor="start" className="ranking-label">Start Date</label>
                    <DatePicker
                        selected={start}
                        placeholderText="MM/DD/YYYY"
                        onChange={(date) => setStart((currentState) => (date))}
                        className="ranking-date-picker"
                        required
                    />
                    <label htmlFor="end" className="ranking-label">End Date</label>
                    <DatePicker
                        selected={end}
                        placeholderText="MM/DD/YYYY"
                        onChange={(date) => setEnd((currentState) => (date))}
                        minDate={start}
                        className="ranking-date-picker"
                        required
                    />
                    <br />
                    <button type="submit" className="ranking-submit-button">
                        {!loading ? <span>Submit</span> : <span>Sending</span>}
                    </button>
                </form>
                <br />
                <br />
                {error && <div className="ranking-error">{error}</div>}
                {response && (
                    <div className="ranking-chart-container">
                        <BarChart width={600} height={300} data={response} className="ranking-bar-chart">
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="userName" />
                            <YAxis />
                            <Tooltip />
                            <Legend />
                            <Bar dataKey="count" fill="#8884d8" />
                        </BarChart>
                    </div>
                )}
            </div>
        </div>
    </>
);
}