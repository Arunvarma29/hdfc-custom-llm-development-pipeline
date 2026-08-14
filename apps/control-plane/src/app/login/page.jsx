"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { FaArrowRight, FaUserCircle, FaTimes } from "react-icons/fa";
import toast from "react-hot-toast";

import { loginUser } from "@/services/auth.service";

import {
  getRecentAccounts,
  removeRecentAccount,
  saveAuth,
  saveRecentAccount,
} from "@/services/auth.storage";

export default function LoginPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [recentAccounts, setRecentAccounts] = useState([]);

  const [showRecentAccounts, setShowRecentAccounts] = useState(true);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setRecentAccounts(getRecentAccounts());
  }, []);

  const handleChange = (event) => {
    setForm((prev) => ({
      ...prev,
      [event.target.name]: event.target.value,
    }));
  };

  const handleSelectAccount = (account) => {
    setForm((prev) => ({
      ...prev,
      email: account.email,
      password: "",
    }));

    setShowRecentAccounts(false);
  };

  const handleRemoveAccount = (event, email) => {
    event.stopPropagation();

    removeRecentAccount(email);

    setRecentAccounts(getRecentAccounts());
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.email || !form.password) {
      toast.error("Please enter email and password.");
      return;
    }

    setLoading(true);

    try {
      const data = await loginUser(form);

      saveAuth(data.access_token, data.user);

      saveRecentAccount(data.user);

      toast.success("Signed in successfully.");

      router.replace("/overview");
    } catch (error) {
      toast.error(
        error?.response?.data?.detail || "Invalid email or password.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-3xl bg-white shadow-xl lg:grid-cols-2">
        {/* Brand Panel */}

        <div className="hidden bg-slate-900 p-10 text-white lg:flex lg:flex-col lg:justify-between">
          <div>
            <div className="text-3xl">🏦</div>

            <p className="mt-8 text-sm font-semibold uppercase tracking-[0.2em] text-blue-300">
              HDFC LLM Pipeline
            </p>

            <h1 className="mt-4 text-4xl font-bold leading-tight">
              Controlled AI development for banking.
            </h1>

            <p className="mt-5 max-w-md text-sm leading-6 text-slate-300">
              Govern datasets, prepare data, develop models, evaluate releases,
              and control deployment from one internal workspace.
            </p>
          </div>

          <p className="text-xs text-slate-500">Internal AI Control Plane</p>
        </div>

        {/* Login Panel */}

        <div className="p-6 sm:p-10 lg:p-12">
          <div className="mx-auto w-full max-w-md">
            <p className="text-sm font-medium text-blue-600">Welcome back</p>

            <h2 className="mt-2 text-3xl font-bold text-slate-900">Sign in</h2>

            <p className="mt-2 text-sm text-slate-500">
              Access the HDFC LLM development workspace.
            </p>

            {/* Recent Accounts */}

            {recentAccounts.length > 0 && showRecentAccounts && (
              <div className="mt-7">
                <div className="mb-3 flex items-center justify-between">
                  <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Recent Accounts
                  </p>

                  <button
                    type="button"
                    onClick={() => setShowRecentAccounts(false)}
                    className="text-xs font-medium text-slate-400 hover:text-slate-600"
                  >
                    Hide
                  </button>
                </div>

                <div className="max-h-39 space-y-2 overflow-y-auto pr-1">
                  {recentAccounts.map((account) => (
                    <div
                      key={account.email}
                      className="group flex w-full items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 transition hover:border-blue-300 hover:bg-blue-50"
                    >
                      <button
                        type="button"
                        onClick={() => handleSelectAccount(account)}
                        className="flex min-w-0 flex-1 items-center gap-3 text-left"
                      >
                        <FaUserCircle
                          size={30}
                          className="shrink-0 text-slate-400 transition group-hover:text-blue-500"
                        />

                        <span className="min-w-0 flex-1">
                          <span className="block truncate text-sm font-semibold text-slate-800">
                            {account.full_name}
                          </span>

                          <span className="mt-0.5 block truncate text-xs text-slate-500">
                            {account.email}
                          </span>
                        </span>

                        <FaArrowRight
                          size={13}
                          className="shrink-0 text-slate-300 transition group-hover:translate-x-0.5 group-hover:text-blue-500"
                        />
                      </button>

                      <button
                        type="button"
                        onClick={(event) =>
                          handleRemoveAccount(event, account.email)
                        }
                        className="rounded-md p-1 text-slate-300 transition hover:bg-white hover:text-red-500"
                        title="Remove account"
                      >
                        <FaTimes size={12} />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}
            {recentAccounts.length > 0 && !showRecentAccounts && (
              <button
                type="button"
                onClick={() => setShowRecentAccounts(true)}
                className="mt-6 text-xs font-semibold text-blue-600 hover:text-blue-700"
              >
                Show recent accounts
              </button>
            )}

            {/* Login Form */}

            <form onSubmit={handleSubmit} className="mt-7 space-y-5">
              <div>
                <label
                  htmlFor="email"
                  className="mb-2 block text-sm font-semibold text-slate-700"
                >
                  Work Email
                </label>

                <input
                  id="email"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="you@hdfc.com"
                  autoComplete="email"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="mb-2 block text-sm font-semibold text-slate-700"
                >
                  Password
                </label>

                <input
                  id="password"
                  name="password"
                  type="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Enter your password"
                  autoComplete="current-password"
                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                />

                <p className="mt-2 text-xs text-slate-400">
                  For your security, your password is never saved on this
                  device.
                </p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>

            <p className="mt-7 text-center text-sm text-slate-500">
              Don't have an account?{" "}
              <Link
                href="/signup"
                className="font-semibold text-blue-600 hover:text-blue-700"
              >
                Create account
              </Link>
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}
