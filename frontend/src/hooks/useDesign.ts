import { useMutation, useQuery, UseQueryOptions } from "@tanstack/react-query";
import { api } from "@/lib/api";

export const useGenerateDesign = () => {
    return useMutation({
        mutationFn: (prompt: string) => api.generateDesign(prompt),
    });
};

export const useGetDesign = (id: string, options?: Partial<UseQueryOptions>) => {
    return useQuery({
        queryKey: ["design", id],
        queryFn: () => api.getDesign(id),
        enabled: !!id,
        ...options,
    });
};
