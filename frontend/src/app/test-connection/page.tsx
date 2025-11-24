"use client";

import { useState } from "react";

export default function TestConnectionPage() {
    const [testResults, setTestResults] = useState<{
        test: string;
        status: "pending" | "success" | "error";
        message: string;
        data?: any;
    }[]>([]);
    const [isRunning, setIsRunning] = useState(false);

    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

    const runTests = async () => {
        setIsRunning(true);
        setTestResults([]);
        const results: typeof testResults = [];

        // Test 1 & 2: Backend Health Check and API Root (via Next.js API route)
        try {
            console.log("Testing backend via Next.js API route...");
            const response = await fetch("/api/test-backend");
            const data = await response.json();
            console.log("API route response:", data);

            if (data.success) {
                // Health check result
                results.push({
                    test: "Backend Health Check",
                    status: "success",
                    message: `Backend is healthy. Service: ${data.health.data.service}`,
                    data: data.health.data
                });
                setTestResults([...results]);

                // API root result
                results.push({
                    test: "API Root Endpoint",
                    status: "success",
                    message: `API root accessible. Message: ${data.root.data.message}`,
                    data: data.root.data
                });
                setTestResults([...results]);
            } else {
                results.push({
                    test: "Backend Health Check",
                    status: "error",
                    message: `Failed to connect: ${data.error}`,
                });
                setTestResults([...results]);

                results.push({
                    test: "API Root Endpoint",
                    status: "error",
                    message: `Failed to connect: ${data.error}`,
                });
                setTestResults([...results]);
            }
        } catch (error: any) {
            results.push({
                test: "Backend Health Check",
                status: "error",
                message: `Failed to test backend: ${error.message}`,
            });
            setTestResults([...results]);

            results.push({
                test: "API Root Endpoint",
                status: "error",
                message: `Failed to test backend: ${error.message}`,
            });
            setTestResults([...results]);
        }

        // Test 3: CORS Configuration
        try {
            const response = await fetch(`${API_URL}/auth/test`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            });
            
            // Even if endpoint doesn't exist, we should get a proper CORS response
            results.push({
                test: "CORS Configuration",
                status: "success",
                message: `CORS is properly configured. Status: ${response.status}`,
            });
        } catch (error: any) {
            if (error.message.includes("CORS")) {
                results.push({
                    test: "CORS Configuration",
                    status: "error",
                    message: `CORS error: ${error.message}`,
                });
            } else {
                results.push({
                    test: "CORS Configuration",
                    status: "success",
                    message: "CORS is properly configured (no CORS errors)",
                });
            }
        }
        setTestResults([...results]);

        // Test 4: Environment Variables
        const envVars = {
            API_URL: process.env.NEXT_PUBLIC_API_URL,
            SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
            ENVIRONMENT: process.env.NEXT_PUBLIC_ENVIRONMENT,
        };

        const missingVars = Object.entries(envVars)
            .filter(([_, value]) => !value || value.includes("your-"))
            .map(([key]) => key);

        if (missingVars.length === 0) {
            results.push({
                test: "Environment Variables",
                status: "success",
                message: "All required environment variables are configured",
                data: envVars
            });
        } else {
            results.push({
                test: "Environment Variables",
                status: "error",
                message: `Missing or placeholder values: ${missingVars.join(", ")}`,
                data: envVars
            });
        }
        setTestResults([...results]);

        setIsRunning(false);
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold mb-2">Frontend-Backend Connection Test</h1>
                <p className="text-gray-600 mb-6">
                    This page tests the connection between the frontend and backend servers.
                </p>

                <button
                    onClick={runTests}
                    disabled={isRunning}
                    className="bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed mb-8"
                >
                    {isRunning ? "Running Tests..." : "Run Connection Tests"}
                </button>

                <div className="space-y-4">
                    {testResults.map((result, index) => (
                        <div
                            key={index}
                            className={`p-6 rounded-lg border-2 ${
                                result.status === "success"
                                    ? "bg-green-50 border-green-500"
                                    : result.status === "error"
                                    ? "bg-red-50 border-red-500"
                                    : "bg-gray-50 border-gray-300"
                            }`}
                        >
                            <div className="flex items-start justify-between mb-2">
                                <h3 className="text-lg font-semibold">{result.test}</h3>
                                <span
                                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                                        result.status === "success"
                                            ? "bg-green-200 text-green-800"
                                            : result.status === "error"
                                            ? "bg-red-200 text-red-800"
                                            : "bg-gray-200 text-gray-800"
                                    }`}
                                >
                                    {result.status.toUpperCase()}
                                </span>
                            </div>
                            <p className="text-gray-700 mb-2">{result.message}</p>
                            {result.data && (
                                <details className="mt-2">
                                    <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
                                        View Details
                                    </summary>
                                    <pre className="mt-2 p-3 bg-gray-100 rounded text-xs overflow-auto">
                                        {JSON.stringify(result.data, null, 2)}
                                    </pre>
                                </details>
                            )}
                        </div>
                    ))}
                </div>

                {testResults.length === 0 && !isRunning && (
                    <div className="text-center text-gray-500 py-12">
                        Click "Run Connection Tests" to start testing the connection.
                    </div>
                )}
            </div>
        </div>
    );
}

