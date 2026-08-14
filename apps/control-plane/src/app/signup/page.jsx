"use client";

import Link from "next/link";
import { useState } from "react";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

import { signupUser } from "@/services/auth.service";

export default function SignupPage() {
  const router = useRouter();

  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [loading, setLoading] =
    useState(false);

  const handleChange = (event) => {
    setForm((prev) => ({
      ...prev,
      [event.target.name]:
        event.target.value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (
      !form.full_name ||
      !form.email ||
      !form.password ||
      !form.confirm_password
    ) {
      toast.error(
        "Please complete all fields."
      );
      return;
    }

    if (form.password.length < 8) {
      toast.error(
        "Password must contain at least 8 characters."
      );
      return;
    }

    if (
      form.password !==
      form.confirm_password
    ) {
      toast.error(
        "Passwords do not match."
      );
      return;
    }

    setLoading(true);

    try {
      await signupUser({
        full_name: form.full_name,
        email: form.email,
        password: form.password,
      });

      toast.success(
        "Account created successfully."
      );

      router.replace("/login");
    } catch (error) {
      toast.error(
        error?.response?.data?.detail ||
          "Unable to create account."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4 py-8">
      <div className="w-full max-w-lg rounded-3xl bg-white p-6 shadow-xl sm:p-10">
        <div>
          <p className="text-sm font-medium text-blue-600">
            HDFC LLM Pipeline
          </p>

          <h1 className="mt-2 text-3xl font-bold text-slate-900">
            Create your account
          </h1>

          <p className="mt-2 text-sm text-slate-500">
            Create an internal AI Control Plane account.
          </p>
        </div>

        <form
          onSubmit={handleSubmit}
          className="mt-8 space-y-5"
        >
          <div>
            <label
              htmlFor="full_name"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Full Name
            </label>

            <input
              id="full_name"
              name="full_name"
              type="text"
              value={form.full_name}
              onChange={handleChange}
              placeholder="Admin User"
              autoComplete="name"
              className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            />
          </div>

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
              autoComplete="new-password"
              className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            />
          </div>

          <div>
            <label
              htmlFor="confirm_password"
              className="mb-2 block text-sm font-semibold text-slate-700"
            >
              Confirm Password
            </label>

            <input
              id="confirm_password"
              name="confirm_password"
              type="password"
              value={form.confirm_password}
              onChange={handleChange}
              autoComplete="new-password"
              className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading
              ? "Creating account..."
              : "Create Account"}
          </button>
        </form>

        <p className="mt-7 text-center text-sm text-slate-500">
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-semibold text-blue-600 hover:text-blue-700"
          >
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}