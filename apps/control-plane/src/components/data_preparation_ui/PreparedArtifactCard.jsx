"use client";

import { FaBoxOpen } from "react-icons/fa";

export default function PreparedArtifactCard({
  artifact,
  loading,
}) {
  return (
    <div className="mt-6 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="flex items-start gap-3">
        <div className="rounded-xl bg-slate-100 p-3 text-slate-600">
          <FaBoxOpen />
        </div>
        <div>
          <h2 className="text-lg font-semibold text-slate-900">
            Prepared Artifact
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Versioned outputs generated for downstream model development.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="mt-6 rounded-xl bg-slate-50 p-6">
          <p className="text-sm text-slate-500">
            Loading artifact...
          </p>
        </div>
      ) : artifact ? (
        <>
          <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <Info label="Artifact ID" value={artifact.artifact_id} />
            <Info label="Version" value={artifact.dataset_version} />
            <Info label="Train Records" value={artifact.train_record_count} />
            <Info
              label="Validation Records"
              value={artifact.validation_record_count}
            />
            <Info label="Test Records" value={artifact.test_record_count} />
            <Info
              label="Duplicates Removed"
              value={artifact.duplicate_count}
            />
            <Info
              label="Created"
              value={
                artifact.created_at
                  ? new Date(artifact.created_at).toLocaleString()
                  : "—"
              }
            />
          </div>

          <div className="mt-5 grid gap-3 lg:grid-cols-2">
            <ArtifactPath label="Train" value={artifact.train_object_key} />
            <ArtifactPath
              label="Validation"
              value={artifact.validation_object_key}
            />
            <ArtifactPath label="Test" value={artifact.test_object_key} />
            <ArtifactPath
              label="Manifest"
              value={artifact.manifest_object_key}
            />
          </div>
        </>
      ) : (
        <div className="mt-6 rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
          <p className="text-sm text-slate-500">
            No prepared artifact available yet.
          </p>
        </div>
      )}
    </div>
  );
}

function Info({ label, value }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 break-all text-sm font-semibold text-slate-900">
        {value ?? "—"}
      </p>
    </div>
  );
}

function ArtifactPath({ label, value }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-3">
      <p className="text-xs font-medium text-slate-500">{label}</p>
      <p className="mt-1 break-all font-mono text-xs text-slate-700">
        {value ?? "—"}
      </p>
    </div>
  );
}
