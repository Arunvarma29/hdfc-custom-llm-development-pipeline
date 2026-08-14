"use client";

import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

import { clearAuth } from "@/services/auth.storage";

export default function LogoutButton() {
  const router = useRouter();

  const handleLogout = () => {
    clearAuth();

    toast.success("Signed out successfully.");

    router.replace("/login");
  };

  return (
    <button
      type="button"
      onClick={handleLogout}
      className="w-full rounded-lg px-3 py-2 text-left text-lg font-medium text-slate-300 transition hover:bg-slate-700 hover:text-white"
    >
      Sign Out
    </button>
  );
}