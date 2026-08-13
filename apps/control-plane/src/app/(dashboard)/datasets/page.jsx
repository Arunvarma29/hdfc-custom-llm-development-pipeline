"use client";

import { useState } from "react";
import PageHeader from "@/components/common/PageHeader";
import DatasetContent from "@/components/dataset/DatasetContent";
import { useDatasets } from "@/hooks/useDatasets";
import { useDebounce } from "@/hooks/useDebounce";
 

export default function DatasetPage() {
  const [filters, setFilters] = useState({
    page: 1,
    limit: 10,
    search: "",
    dataset_type: "",
    status: "",
  });

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
      page: 1,
    }));
  };

  const debouncedSearch = useDebounce(filters.search);

  const { data, isLoading, isFetching, isError } = useDatasets({
    ...filters,
    search: debouncedSearch,
  });

  const handlePageChange = (page) => {
    setFilters((prev) => ({
      ...prev,
      page,
    }));
  };

  return (
    <>
      <PageHeader
        title="Dataset Registry"
        description="Manage datasets used for AI model development."
      />


      <DatasetContent
        filters={filters}
        onFilterChange={handleFilterChange}
        onPageChange={handlePageChange}
        data={data}
        isLoading={isLoading}
        isFetching={isFetching}
        isError={isError}
      />
    </>
  );
}
