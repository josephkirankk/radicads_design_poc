"use client";

import { useState } from "react";

export default function TestAllEndpointsPage() {
    const [testResults, setTestResults] = useState<{
        endpoint: string;
        method: string;
        status: "pending" | "success" | "error" | "skipped";
        message: string;
        statusCode?: number;
    }[]>([]);
    const [isRunning, setIsRunning] = useState(false);

    const runTests = async () => {
        setIsRunning(true);
        setTestResults([]);
        const results: typeof testResults = [];

        // Helper function to add result
        const addResult = (endpoint: string, method: string, status: any, message: string, statusCode?: number) => {
            results.push({ endpoint, method, status, message, statusCode });
            setTestResults([...results]);
        };

        // Test 1: AI Generate Endpoint
        try {
            const response = await fetch("/api/ai/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt: "Test prompt" }),
            });
            addResult("/api/ai/generate", "POST", response.ok ? "success" : "error", 
                response.ok ? "✅ AI generate endpoint working" : `❌ Failed: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/ai/generate", "POST", "error", `❌ Error: ${error.message}`);
        }

        // Test 2: Designs - List (requires auth, will fail without token)
        try {
            const response = await fetch("/api/designs");
            addResult("/api/designs", "GET", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/designs", "GET", "error", `❌ Error: ${error.message}`);
        }

        // Test 3: Designs - Create (requires auth, will fail without token)
        try {
            const response = await fetch("/api/designs", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: "Test Design", json_data: {} }),
            });
            addResult("/api/designs", "POST", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/designs", "POST", "error", `❌ Error: ${error.message}`);
        }

        // Test 4: Designs - Get by ID (requires auth)
        try {
            const response = await fetch("/api/designs/test-id");
            addResult("/api/designs/[id]", "GET", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/designs/[id]", "GET", "error", `❌ Error: ${error.message}`);
        }

        // Test 5: Brands - List (requires auth)
        try {
            const response = await fetch("/api/brands");
            addResult("/api/brands", "GET", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/brands", "GET", "error", `❌ Error: ${error.message}`);
        }

        // Test 6: Brands - Create (requires auth)
        try {
            const response = await fetch("/api/brands", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name: "Test Brand" }),
            });
            addResult("/api/brands", "POST", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/brands", "POST", "error", `❌ Error: ${error.message}`);
        }

        // Test 7: Brands - Get by ID (requires auth)
        try {
            const response = await fetch("/api/brands/test-id");
            addResult("/api/brands/[id]", "GET", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/brands/[id]", "GET", "error", `❌ Error: ${error.message}`);
        }

        // Test 8: Auth - Me (requires auth)
        try {
            const response = await fetch("/api/auth/me");
            addResult("/api/auth/me", "GET", response.status === 401 ? "success" : "error",
                response.status === 401 ? "✅ Auth required (expected)" : `Status: ${response.status}`, response.status);
        } catch (error: any) {
            addResult("/api/auth/me", "GET", "error", `❌ Error: ${error.message}`);
        }

        // Test 9: Backend Health (via API route)
        try {
            const response = await fetch("/api/test-backend");
            const data = await response.json();
            addResult("/api/test-backend", "GET", data.success ? "success" : "error",
                data.success ? "✅ Backend connection working" : `❌ Failed: ${data.error}`, response.status);
        } catch (error: any) {
            addResult("/api/test-backend", "GET", "error", `❌ Error: ${error.message}`);
        }

        setIsRunning(false);
    };

    return (
        <div className="container mx-auto py-12 px-4">
            <div className="max-w-4xl mx-auto">
                <h1 className="text-3xl font-bold mb-6">Test All API Endpoints</h1>
                
                <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded">
                    <h2 className="font-bold mb-2">ℹ️ Test Information</h2>
                    <p className="text-sm">
                        This page tests all Next.js API routes to verify they are properly configured.
                        Most endpoints require authentication, so 401 (Unauthorized) responses are expected and indicate the routes are working correctly.
                    </p>
                </div>

                <button
                    onClick={runTests}
                    disabled={isRunning}
                    className="mb-6 px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:bg-gray-400"
                >
                    {isRunning ? "Running Tests..." : "Run All Tests"}
                </button>

                {testResults.length > 0 && (
                    <div className="space-y-2">
                        {testResults.map((result, index) => (
                            <div
                                key={index}
                                className={`p-4 rounded border ${
                                    result.status === "success"
                                        ? "bg-green-50 border-green-200"
                                        : result.status === "error"
                                        ? "bg-red-50 border-red-200"
                                        : "bg-gray-50 border-gray-200"
                                }`}
                            >
                                <div className="flex justify-between items-start">
                                    <div>
                                        <div className="font-mono text-sm font-bold">
                                            {result.method} {result.endpoint}
                                        </div>
                                        <div className="text-sm mt-1">{result.message}</div>
                                    </div>
                                    {result.statusCode && (
                                        <span className="text-xs font-mono bg-gray-200 px-2 py-1 rounded">
                                            {result.statusCode}
                                        </span>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

