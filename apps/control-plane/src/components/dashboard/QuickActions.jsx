"use client";

import Link from "next/link";
import { FaDatabase } from "react-icons/fa";
import { RiFileList3Line } from "react-icons/ri";
import { FaBrain } from "react-icons/fa";
import { MdAssessment } from "react-icons/md";

const actions = [
  {
    title: "Upload Dataset",
    description: "Register a new banking dataset.",
    route: "/datasets",
    icon: FaDatabase,
    enabled: true,
  },
  {
    title: "Data Preparation",
    description: "Prepare and validate registered data.",
    route: "/data-preparation",
    icon: RiFileList3Line,
    enabled: true,
  },
  {
    title: "Fine Tuning",
    description: "Start model development.",
    route: "/fine-tuning",
    icon: FaBrain,
    enabled: true,
  },
  {
    title: "Evaluation",
    description: "Evaluate model candidates.",
    route: "/evaluation",
    icon: MdAssessment,
    enabled: true,
  },
];

export default function QuickActions() {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-5">
        <h2 className="text-lg font-semibold text-slate-900">
          Quick Actions
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Jump directly to a development workflow.
        </p>
      </div>

      <div className="grid gap-3 sm:grid-cols-2 xl:grid-cols-1">
        {actions.map((action) => {
          const Icon = action.icon;

          return (
            <Link
              key={action.title}
              href={action.route}
              className="group rounded-xl border border-slate-200 p-4 transition hover:border-blue-300 hover:bg-blue-50"
            >
              <div className="flex items-start gap-3">
                <div className="rounded-lg bg-blue-50 p-2.5">
                  <Icon
                    size={19}
                    className="text-blue-600"
                  />
                </div>

                <div className="min-w-0">
                  <p className="font-semibold text-slate-900">
                    {action.title}
                  </p>

                  <p className="mt-1 text-xs leading-5 text-slate-500">
                    {action.description}
                  </p>
                </div>
              </div>
            </Link>
          );
        })}
      </div>
    </div>
  );
}