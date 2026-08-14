"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { FaTimes } from "react-icons/fa";
import { sidebarItems } from "@/constants/sidebar";
import LogoutButton from "@/components/auth/LogoutButton";

export default function Sidebar({ isOpen, onClose }) {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <button
          type="button"
          aria-label="Close navigation"
          onClick={onClose}
          className="fixed inset-0 z-40 bg-slate-950/50 lg:hidden"
        />
      )}

      <aside
        className={`
          fixed inset-y-0 left-0 z-50 flex w-64 flex-col
          bg-slate-900 text-white shadow-xl
          transition-transform duration-200
          lg:static lg:z-auto lg:min-h-screen lg:translate-x-0 lg:shadow-none
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        {/* Logo */}
        <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-800 px-5">
          <h1 className="text-sm font-bold tracking-wide sm:text-base">
            🏦 HDFC LLM Pipeline
          </h1>

          <button
            type="button"
            onClick={onClose}
            className="rounded-lg p-2 text-slate-400 hover:bg-slate-800 hover:text-white lg:hidden"
            aria-label="Close navigation"
          >
            <FaTimes size={18} />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4">
          {sidebarItems.map((item) => {
            const Icon = item.icon;
            const active = pathname === item.href;

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={`
                  mx-3 mb-1 flex items-center gap-3 rounded-lg px-4 py-3
                  transition-all
                  ${
                    active
                      ? "bg-blue-600 text-white shadow-sm"
                      : "text-slate-300 hover:bg-slate-800 hover:text-white"
                  }
                `}
              >
                <Icon size={18} />

                <span className="text-sm font-medium">{item.title}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="shrink-0 border-t border-slate-800 p-4">
          <div className="rounded-lg bg-slate-800 p-3">
            <p className="text-sm font-semibold">Admin</p>
            <div className="mt-3 rounded-lg bg-slate-800">
              <LogoutButton />
            </div>
            <p className="text-xs text-slate-400">AI Platform</p>
          </div>
        </div>
      </aside>
    </>
  );
}
