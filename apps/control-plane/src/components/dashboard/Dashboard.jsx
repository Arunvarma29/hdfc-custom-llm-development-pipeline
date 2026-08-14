"use client";

import {
  FaDatabase,
  FaCloudUploadAlt,
  FaClock,
  FaCheckCircle,
} from "react-icons/fa";
import { MdCancel } from "react-icons/md";

import useDashboardSummary from "@/hooks/useDashboardSummary";

import StatsCard from "./StatsCard";
import QuickActions from "./QuickActions";
import RecentDatasets from "./RecentDatasets";

export default function Dashboard() {
  const {
    data,
    isLoading,
    isFetching,
    isError,
  } = useDashboardSummary();

  if (isLoading) {
    return <DashboardSkeleton />;
  }

  if (isError) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 p-5">
        <p className="text-sm font-semibold text-red-700">
          Failed to load dashboard data.
        </p>

        <p className="mt-1 text-sm text-red-600">
          Please refresh the page and try again.
        </p>
      </div>
    );
  }

  const stats = data?.stats ?? {};

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-end">
        {isFetching && (
          <div className="flex items-center gap-2 text-xs text-blue-600">
            <div className="h-3 w-3 animate-spin rounded-full border-2 border-blue-600 border-t-transparent" />
            Updating...
          </div>
        )}
      </div>

      <section className="grid grid-cols-2 gap-3 sm:gap-4 xl:grid-cols-5">
        <StatsCard
          title="Total Datasets"
          value={stats.total_datasets ?? 0}
          icon={FaDatabase}
          description="Registered datasets"
        />

        <StatsCard
          title="Uploaded"
          value={stats.uploaded ?? 0}
          icon={FaCloudUploadAlt}
          description="Awaiting preparation"
        />

        <StatsCard
          title="Preparing"
          value={stats.preparing ?? 0}
          icon={FaClock}
          description="Preparation in progress"
        />

        <StatsCard
          title="Approved"
          value={stats.approved ?? 0}
          icon={FaCheckCircle}
          description="Approved dataset versions"
        />

        <StatsCard
          title="Rejected"
          value={stats.rejected ?? 0}
          icon={MdCancel}
          description="Rejected dataset versions"
        />
      </section>

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">
        <div>
          <QuickActions />
        </div>

        <div className="xl:col-span-2">
          <RecentDatasets
            datasets={
              data?.recent_datasets ?? []
            }
          />
        </div>
      </section>
    </div>
  );
}

function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-5">
        {[1, 2, 3, 4, 5].map((item) => (
          <div
            key={item}
            className="h-32 animate-pulse rounded-2xl bg-white shadow-sm"
          />
        ))}
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <div className="h-80 animate-pulse rounded-2xl bg-white shadow-sm" />

        <div className="h-80 animate-pulse rounded-2xl bg-white shadow-sm xl:col-span-2" />
      </div>
    </div>
  );
}