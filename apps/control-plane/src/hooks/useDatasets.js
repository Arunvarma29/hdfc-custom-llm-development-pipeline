import { useQuery } from "@tanstack/react-query";

import { getDatasets } from "@/services/dataset.service";
import { QUERY_KEYS } from "@/constants/queryKeys";

export function useDatasets(params = {}) {
  return useQuery({
    queryKey: [...QUERY_KEYS.DATASETS, params],
    queryFn: () => getDatasets(params),
  });
}