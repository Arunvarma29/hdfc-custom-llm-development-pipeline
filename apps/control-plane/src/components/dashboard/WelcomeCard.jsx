"use client";

import { useEffect, useState } from "react";

import { getAuthUser } from "@/services/auth.storage";

export default function WelcomeCard() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    setUser(getAuthUser());
  }, []);

  const firstName =
    user?.full_name?.split(" ")[0] || "User";

  return (
    <div className="mb-6 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="bg-slate-900 px-5 py-6 text-white sm:px-7">
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-blue-300">
          Internal AI Control Plane
        </p>

        <h1 className="mt-2 text-2xl font-bold sm:text-3xl">
          Welcome back, {firstName}
        </h1>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-300">
          Manage governed datasets, preparation workflows,
          model development, evaluation, and deployment from
          one workspace.
        </p>
      </div>

      <div className="grid gap-3 border-t border-slate-200 bg-slate-50 p-4 sm:grid-cols-3 sm:p-5">
        <StatusItem
          label="Workspace"
          value="AI Development"
        />

        <StatusItem
          label="Access"
          value="Authenticated"
        />

        <StatusItem
          label="Environment"
          value="Internal"
        />
      </div>
    </div>
  );
}

function StatusItem({ label, value }) {
  return (
    <div className="rounded-xl bg-white p-3">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-sm font-semibold text-slate-900">
        {value}
      </p>
    </div>
  );
}