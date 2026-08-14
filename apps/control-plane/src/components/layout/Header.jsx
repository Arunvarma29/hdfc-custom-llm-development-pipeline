"use client";

import { useEffect, useState } from "react";
import {
  FaSearch,
  FaUserCircle,
  FaChevronDown,
} from "react-icons/fa";

import { getAuthUser } from "@/services/auth.storage";
import LogoutButton from "@/components/auth/LogoutButton";

export default function Header({ onMenuClick }) {
  const [user, setUser] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);

  useEffect(() => {
    setUser(getAuthUser());
  }, []);

  return (
    <header className="relative z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 shadow-sm sm:px-6">
      {/* Left */}
      <div className="flex min-w-0 items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          className="rounded-lg p-2 text-slate-600 transition hover:bg-slate-100 lg:hidden"
          aria-label="Open navigation"
        >
          ☰
        </button>

        <div className="relative hidden w-72 md:block lg:w-80">
          <FaSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />

          <input
            type="text"
            placeholder="Search workspace..."
            className="w-full rounded-xl border border-slate-300 bg-slate-50 py-2 pl-10 pr-4 text-sm outline-none transition focus:border-blue-500 focus:bg-white focus:ring-2 focus:ring-blue-100"
          />
        </div>
      </div>

      {/* Right */}
      <div className="relative">
        <button
          type="button"
          onClick={() =>
            setProfileOpen((prev) => !prev)
          }
          className="flex items-center gap-3 rounded-xl px-2 py-1.5 transition hover:bg-slate-50"
        >
          <FaUserCircle
            size={32}
            className="text-slate-600"
          />

          <div className="hidden text-left sm:block">
            <p className="max-w-[180px] truncate text-sm font-semibold text-slate-900">
              {user?.full_name || "User"}
            </p>

            <p className="max-w-[180px] truncate text-xs text-slate-500">
              {user?.email || ""}
            </p>
          </div>

          <FaChevronDown
            size={11}
            className={`hidden text-slate-400 transition sm:block ${
              profileOpen ? "rotate-180" : ""
            }`}
          />
        </button>

        {profileOpen && (
          <div className="absolute right-0 mt-2 w-64 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-xl">
            <div className="border-b border-slate-100 p-4">
              <p className="text-sm font-semibold text-slate-900">
                {user?.full_name || "User"}
              </p>

              <p className="mt-1 break-all text-xs text-slate-500">
                {user?.email || ""}
              </p>

              <div className="mt-3 inline-flex rounded-full bg-blue-50 px-3 py-1 text-xs font-semibold text-blue-700">
                AI Platform User
              </div>
            </div>

            <div className="p-2 bg-gray-500">
              <LogoutButton />
            </div>
          </div>
        )}
      </div>
    </header>
  );
}