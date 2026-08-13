"use client";

import {
  FaBars,
  FaSearch,
  FaUserCircle,
} from "react-icons/fa";

export default function Header({ onMenuClick }) {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 bg-white px-4 shadow-sm sm:px-6">
      {/* Left */}
      <div className="flex min-w-0 items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          className="rounded-lg p-2 text-slate-600 transition hover:bg-slate-100 lg:hidden"
          aria-label="Open navigation"
        >
          <FaBars size={18} />
        </button>

        {/* Search */}
        <div className="relative hidden w-64 sm:block md:w-80">
          <FaSearch
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <input
            type="text"
            placeholder="Search..."
            className="w-full rounded-lg border border-slate-300 py-2 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>
      </div>

      {/* Profile */}
      <div className="flex items-center gap-2 sm:gap-3">
        <FaUserCircle
          size={30}
          className="text-slate-600 sm:hidden"
        />

        <FaUserCircle
          size={34}
          className="hidden text-slate-600 sm:block"
        />

        <div className="hidden sm:block">
          <p className="text-sm font-semibold text-slate-900">
            Admin
          </p>

          <p className="text-xs text-slate-500">
            AI Platform
          </p>
        </div>
      </div>
    </header>
  );
}