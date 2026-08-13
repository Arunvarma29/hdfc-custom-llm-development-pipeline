import { useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";

import { deleteDataset } from "@/services/dataset.service";
import { QUERY_KEYS } from "@/constants/queryKeys";

export function useDeleteDataset() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: deleteDataset,

    onSuccess: () => {
      toast.success("Dataset deleted successfully.");

      queryClient.invalidateQueries({
        queryKey: QUERY_KEYS.DATASETS,
      });
    },

    onError: (error) => {
      toast.error(
        error?.response?.data?.detail ??
        "Failed to delete dataset."
      );
    },
  });
}