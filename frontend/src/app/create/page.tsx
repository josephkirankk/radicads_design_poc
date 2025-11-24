"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { useGenerateDesign } from "@/hooks/useDesign";
import { useAppStore } from "@/store/useStore";

export default function CreatePage() {
    const [prompt, setPrompt] = useState("");
    const router = useRouter();
    const generateMutation = useGenerateDesign();
    const { setCurrentDesignId, setCurrentDesignData, setIsGenerating } = useAppStore();

    // Suppress browser extension errors
    useEffect(() => {
        const originalError = console.error;
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        console.error = (...args: any[]) => {
            const errorString = args.join(' ');
            if (errorString.includes('content_script.js') ||
                errorString.includes('Cannot read properties of undefined')) {
                return; // Suppress extension errors
            }
            originalError.apply(console, args);
        };

        return () => {
            console.error = originalError;
        };
    }, []);

    // prompt = "Instagram ad for a coffee shop, warm colors, 50% off"

    const handleGenerate = async () => {
        if (!prompt) return;
        setIsGenerating(true);
        console.log("Starting design generation with prompt:", prompt);
        try {
            console.log("Calling generateMutation.mutateAsync...");
            const design = await generateMutation.mutateAsync(prompt);
            console.log("Design generated successfully:", design);
            console.log("Design structure:", {
                hasId: !!design?.id,
                hasDesignJson: !!design?.design_json,
                designJsonType: typeof design?.design_json,
                designKeys: design ? Object.keys(design) : null
            });
            if (design && design.id) {
                console.log("Storing design in app store:", design);
                setCurrentDesignId(design.id);
                setCurrentDesignData(design); // Store the full design data
                console.log("Redirecting to editor:", `/editor/${design.id}`);
                router.push(`/editor/${design.id}`);
            } else {
                console.error("Design returned but no ID found:", design);
                alert("Design generated but no ID found. Check console for details.");
            }
        } catch (error) {
            console.error("Failed to generate design - Full error:", error);
            console.error("Error type:", (error as any)?.constructor?.name);
            console.error("Error message:", (error as any)?.message);
            const errorMessage = (error as any)?.message || 'Unknown error';
            alert(`Failed to generate design: ${errorMessage}. Check console for details.`);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="container mx-auto py-12 px-4">
            <Card className="max-w-2xl mx-auto">
                <CardHeader>
                    <CardTitle>Create New Design</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label htmlFor="prompt">Describe your design</Label>
                        <Textarea
                            id="prompt"
                            name="design-prompt"
                            placeholder="Instagram ad for a coffee shop, warm colors, 50% off..."
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            className="min-h-[150px]"
                            autoComplete="off"
                            data-form-type="other"
                            data-lpignore="true"
                            data-1p-ignore="true"
                            data-bwignore="true"
                            data-dashlane-ignore="true"
                            data-keeper-ignore="true"
                        />
                    </div>
                    <Button
                        onClick={handleGenerate}
                        disabled={generateMutation.isPending || !prompt}
                        className="w-full"
                    >
                        {generateMutation.isPending ? "Generating..." : "Generate Design"}
                    </Button>
                </CardContent>
            </Card>
        </div>
    );
}
