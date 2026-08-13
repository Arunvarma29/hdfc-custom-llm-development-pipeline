"use client";

import {
  dashboardStats,
  quickActions,
  recentDatasets,
} from "@/constants/dashboard";

import StatsCard from "./StatsCard";
import QuickActions from "./QuickActions";
import RecentDatasets from "./RecentDatasets";

export default function Dashboard() {
  return (
    <div className="space-y-8">

      {/* Stats */}

      <section className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-4">

        {dashboardStats.map((stat) => (

          <StatsCard
            key={stat.title}
            {...stat}
          />

        ))}

      </section>

      {/* Content */}

      <section className="grid grid-cols-1 gap-6 xl:grid-cols-3">

        <div className="xl:col-span-1">

          <QuickActions
            actions={quickActions}
          />

        </div>

        <div className="xl:col-span-2">

          <RecentDatasets
            datasets={recentDatasets}
          />

        </div>

      </section>

    </div>
  );
}