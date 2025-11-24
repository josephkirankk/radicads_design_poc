"use client";

import { useState } from "react";

export default function TestGeneratePage() {
    const [testResults, setTestResults] = useState<{
        test: string;
        status: "pending" | "success" | "error";
        message: string;
        data?: any;
    }[]>([]);
    const [isRunning, setIsRunning] = useState(false);

    const runTests = async () => {
        setIsRunning(true);
        setTestResults([]);
        const results: typeof testResults = [];

        // Test 1: Check current origin
        try {
            const origin = window.location.origin;
            results.push({
                test: "Current Origin",
                status: "success",
                message: `Browser is accessing frontend from: ${origin}`,
                data: { origin, hostname: window.location.hostname, port: window.location.port }
            });
        } catch (error: any) {
            results.push({
                test: "Current Origin",
                status: "error",
                message: `Failed to get origin: ${error.message}`,
            });
        }
        setTestResults([...results]);

        // Test 2: Check environment variables
        try {
            const apiUrl = process.env.NEXT_PUBLIC_API_URL;
            results.push({
                test: "Environment Variables",
                status: apiUrl ? "success" : "error",
                message: apiUrl ? `NEXT_PUBLIC_API_URL is set to: ${apiUrl}` : "NEXT_PUBLIC_API_URL is not set",
                data: { apiUrl }
            });
        } catch (error: any) {
            results.push({
                test: "Environment Variables",
                status: "error",
                message: `Failed to check env vars: ${error.message}`,
            });
        }
        setTestResults([...results]);

        // Test 3: Direct backend call (will likely fail with CORS)
        try {
            console.log("Testing DIRECT backend call (should fail)...");
            const response = await fetch("http://localhost:8000/health");
            const data = await response.json();
            
            results.push({
                test: "Direct Backend Call",
                status: "success",
                message: "Direct call succeeded (unexpected!)",
                data
            });
        } catch (error: any) {
            results.push({
                test: "Direct Backend Call",
                status: "error",
                message: `Direct call failed (expected): ${error.message}`,
            });
        }
        setTestResults([...results]);

        // Test 4: Via Next.js API route (should work)
        try {
            console.log("Testing via Next.js API route...");
            const response = await fetch("/api/test-backend");
            const data = await response.json();
            
            results.push({
                test: "Via Next.js API Route",
                status: data.success ? "success" : "error",
                message: data.success ? "API route working correctly" : `API route failed: ${data.error}`,
                data
            });
        } catch (error: any) {
            results.push({
                test: "Via Next.js API Route",
                status: "error",
                message: `API route failed: ${error.message}`,
            });
        }
        setTestResults([...results]);

        // Test 5: Test AI endpoint via API route (need to create this)
        try {
            console.log("Testing AI generate endpoint...");
            const response = await fetch("/api/ai/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ prompt: "Test prompt for connection check" }),
            });
            
            if (response.ok) {
                const data = await response.json();
                results.push({
                    test: "AI Generate Endpoint",
                    status: "success",
                    message: "AI endpoint accessible via API route",
                    data
                });
            } else {
                const errorText = await response.text();
                results.push({
                    test: "AI Generate Endpoint",
                    status: "error",
                    message: `AI endpoint returned ${response.status}: ${errorText}`,
                });
            }
        } catch (error: any) {
            results.push({
                test: "AI Generate Endpoint",
                status: "error",
                message: `AI endpoint test failed: ${error.message}`,
            });
        }
        setTestResults([...results]);

        setIsRunning(false);
    };

    return (
        <div className="min-h-screen bg-gray-50 p-8">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold mb-4">Generate Design Connection Test</h1>
                <p className="text-gray-600 mb-8">
                    This page tests the "Generate Design" functionality and identifies CORS/connection issues.
                </p>

                <button
                    type="button"
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
                            className={`p-4 rounded-lg border-2 ${
                                result.status === "success"
                                    ? "bg-green-50 border-green-500"
                                    : result.status === "error"
                                    ? "bg-red-50 border-red-500"
                                    : "bg-gray-50 border-gray-300"
                            }`}
                        >
                            <div className="flex items-center justify-between mb-2">
                                <h3 className="font-semibold text-lg">{result.test}</h3>
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
                            <p className="text-gray-700">{result.message}</p>
                            {result.data && (
                                <details className="mt-2">
                                    <summary className="cursor-pointer text-sm text-gray-600 hover:text-gray-800">
                                        View Details
                                    </summary>
                                    <pre className="mt-2 p-2 bg-gray-100 rounded text-xs overflow-auto">
                                        {JSON.stringify(result.data, null, 2)}
                                    </pre>
                                </details>
                            )}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}

