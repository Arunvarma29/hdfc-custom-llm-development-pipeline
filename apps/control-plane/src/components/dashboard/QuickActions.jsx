"use client";

import Link from "next/link";

export default function QuickActions({
  actions,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-lg font-semibold text-slate-900">
        Quick Actions
      </h2>

      <div className="grid grid-cols-2 gap-4">

        {actions.map((action) => {

          const Icon = action.icon;

          if (action.enabled) {
            return (
              <Link
                key={action.title}
                href={action.route}
                className="flex items-center gap-3 rounded-lg border border-slate-200 p-4 transition hover:border-blue-500 hover:bg-blue-50"
              >
                <Icon
                  size={22}
                  className="text-blue-600"
                />

                <span className="font-medium">
                  {action.title}
                </span>
              </Link>
            );
          }

          return (
            <button
              key={action.title}
              disabled
              className="flex cursor-not-allowed items-center justify-between rounded-lg border border-dashed border-slate-300 p-4 text-slate-400"
            >
              <div className="flex items-center gap-3">
                <Icon size={22} />
                <span>{action.title}</span>
              </div>

              <span className="rounded bg-slate-100 px-2 py-1 text-xs">
                Soon
              </span>
            </button>
          );

        })}

      </div>

    </div>
  );
}