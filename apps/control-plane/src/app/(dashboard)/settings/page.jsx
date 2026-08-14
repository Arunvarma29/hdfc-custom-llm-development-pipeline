"use client";

import { useEffect, useState } from "react";
import {
  FaUser,
  FaLock,
  FaBuilding,
  FaDatabase,
} from "react-icons/fa";

import PageHeader from "@/components/common/PageHeader";
import { getAuthUser } from "@/services/auth.storage";

export default function SettingsPage() {
  const [user, setUser] = useState(null);
  const [activeSection, setActiveSection] = useState("profile");

  useEffect(() => {
    setUser(getAuthUser());
  }, []);

  return (
    <>
      <PageHeader
        title="Settings"
        description="Manage your account, workspace, security, and data controls."
      />

      <div className="grid gap-6 lg:grid-cols-[240px_minmax(0,1fr)]">
        {/* Settings Navigation */}
        <aside className="rounded-2xl border border-slate-200 bg-white p-3 shadow-sm">
          <SettingsNavItem
            icon={FaUser}
            label="Profile"
            active={activeSection === "profile"}
            onClick={() => setActiveSection("profile")}
          />

          <SettingsNavItem
            icon={FaLock}
            label="Security"
            active={activeSection === "security"}
            onClick={() => setActiveSection("security")}
          />

          <SettingsNavItem
            icon={FaBuilding}
            label="Workspace"
            active={activeSection === "workspace"}
            onClick={() => setActiveSection("workspace")}
          />

          <SettingsNavItem
            icon={FaDatabase}
            label="Data Management"
            active={activeSection === "data"}
            onClick={() => setActiveSection("data")}
          />
        </aside>

        {/* Content */}
        <section>
          {activeSection === "profile" && (
            <ProfileSection user={user} />
          )}

          {activeSection === "security" && (
            <SecuritySection />
          )}

          {activeSection === "workspace" && (
            <WorkspaceSection />
          )}

          {activeSection === "data" && (
            <DataManagementSection />
          )}
        </section>
      </div>
    </>
  );
}

function SettingsNavItem({
  icon: Icon,
  label,
  active,
  onClick,
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex w-full items-center gap-3 rounded-xl px-4 py-3 text-left text-sm font-medium transition ${
        active
          ? "bg-blue-50 text-blue-700"
          : "text-slate-600 hover:bg-slate-50 hover:text-slate-900"
      }`}
    >
      <Icon size={16} />

      <span>{label}</span>
    </button>
  );
}

function ProfileSection({ user }) {
  return (
    <div className="space-y-6">
      <SettingsCard
        title="Profile"
        description="Your authenticated workspace identity."
      >
        <div className="grid gap-5 sm:grid-cols-2">
          <Info
            label="Full Name"
            value={user?.full_name || "—"}
          />

          <Info
            label="Email"
            value={user?.email || "—"}
          />

          <Info
            label="Account Status"
            value={user?.is_active ? "Active" : "Inactive"}
          />

          <Info
            label="Access"
            value="AI Platform"
          />
        </div>
      </SettingsCard>

      <SettingsCard
        title="Account"
        description="Account actions will be added here."
      >
        <p className="text-sm text-slate-500">
          Profile editing can be connected to the backend later.
        </p>
      </SettingsCard>
    </div>
  );
}

function SecuritySection() {
  return (
    <SettingsCard
      title="Security"
      description="Manage authentication and account security."
    >
      <div className="space-y-4">
        <SecurityItem
          title="Password"
          description="Change your account password."
          action="Change Password"
        />

        <SecurityItem
          title="Session"
          description="Your current authenticated session is active."
          action="Active"
          disabled
        />

        <SecurityItem
          title="Authentication"
          description="JWT-based authentication is enabled."
          action="Enabled"
          disabled
        />
      </div>
    </SettingsCard>
  );
}

function WorkspaceSection() {
  return (
    <SettingsCard
      title="Workspace"
      description="Information about the current AI development environment."
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <Info
          label="Application"
          value="HDFC LLM Pipeline"
        />

        <Info
          label="Environment"
          value="Internal"
        />

        <Info
          label="Backend"
          value="FastAPI"
        />

        <Info
          label="Database"
          value="PostgreSQL"
        />

        <Info
          label="Object Storage"
          value="MinIO"
        />

        <Info
          label="Frontend"
          value="Next.js"
        />
      </div>
    </SettingsCard>
  );
}

function DataManagementSection() {
  return (
    <SettingsCard
      title="Data Management"
      description="Administrative controls for dataset lifecycle and storage."
    >
      <div className="space-y-4">
        <AdminItem
          title="Deleted Datasets"
          description="View datasets that were soft-deleted from the Dataset Registry."
          action="Coming soon"
        />

        <AdminItem
          title="Restore Dataset"
          description="Restore an eligible soft-deleted dataset."
          action="Coming soon"
        />

        <AdminItem
          title="Storage"
          description="Object storage and artifact retention controls."
          action="Coming soon"
        />
      </div>
    </SettingsCard>
  );
}

function SettingsCard({
  title,
  description,
  children,
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:p-6">
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-slate-900">
          {title}
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>

      {children}
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-4">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>

      <p className="mt-1 break-all text-sm font-semibold text-slate-900">
        {value}
      </p>
    </div>
  );
}

function SecurityItem({
  title,
  description,
  action,
  disabled = false,
}) {
  return (
    <div className="flex flex-col gap-4 rounded-xl border border-slate-200 p-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-semibold text-slate-900">
          {title}
        </p>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>

      <button
        type="button"
        disabled={disabled}
        className="shrink-0 rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 disabled:cursor-not-allowed disabled:bg-slate-50 disabled:text-slate-400"
      >
        {action}
      </button>
    </div>
  );
}

function AdminItem({
  title,
  description,
  action,
}) {
  return (
    <div className="flex flex-col gap-4 rounded-xl border border-slate-200 p-4 sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-semibold text-slate-900">
          {title}
        </p>

        <p className="mt-1 text-sm text-slate-500">
          {description}
        </p>
      </div>

      <span className="shrink-0 rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-500">
        {action}
      </span>
    </div>
  );
}