import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { createDataset } from "@/services/dataset.service";
import { QUERY_KEYS } from "@/constants/queryKeys";

export function useCreateDataset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createDataset,

    onSuccess: (dataset) => {
      toast.success(`${dataset.name} uploaded successfully.`);

      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.DATASETS,
      });
    },

    onError: (error) => {
      toast.error(
        error?.response?.data?.detail ||
        "Upload failed."
      );
    },
  });
}