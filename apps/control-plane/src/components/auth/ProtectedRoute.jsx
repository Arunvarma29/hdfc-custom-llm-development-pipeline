"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { getCurrentUser } from "@/services/auth.service";
import {
  getAuthToken,
  saveAuth,
  clearAuth,
} from "@/services/auth.storage";

export default function ProtectedRoute({ children }) {
  const router = useRouter();

  const [status, setStatus] = useState("checking");

  useEffect(() => {
    let mounted = true;

    const validateSession = async () => {
      const token = getAuthToken();

      if (!token) {
        router.replace("/login");
        return;
      }

      try {
        const user = await getCurrentUser();

        if (!mounted) return;

        /*
         * Refresh the locally cached user in case
         * account information changed.
         */
        saveAuth(token, user);

        setStatus("authenticated");
      } catch {
        clearAuth();

        if (mounted) {
          router.replace("/login");
        }
      }
    };

    validateSession();

    return () => {
      mounted = false;
    };
  }, [router]);

  if (status === "checking") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-100">
        <div className="flex items-center gap-3 rounded-xl bg-white px-5 py-4 shadow-sm">
          <div className="h-4 w-4 animate-spin rounded-full border-2 border-slate-300 border-t-slate-900" />

          <span className="text-sm font-medium text-slate-600">
            Verifying your session...
          </span>
        </div>
      </div>
    );
  }

  if (status !== "authenticated") {
    return null;
  }

  return children;
}