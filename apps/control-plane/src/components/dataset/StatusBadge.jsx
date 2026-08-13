const STATUS_STYLES = {
  UPLOADED: "bg-sky-50 text-sky-700 ring-sky-200",
  PREPARING: "bg-amber-50 text-amber-700 ring-amber-200",
  READY: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  APPROVED: "bg-green-50 text-green-700 ring-green-200",
  REJECTED: "bg-red-50 text-red-700 ring-red-200",
  FAILED: "bg-red-50 text-red-700 ring-red-200",
};

export default function StatusBadge({ status }) {
  const normalizedStatus = String(status || "").toUpperCase();

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold ring-1 ring-inset ${
        STATUS_STYLES[normalizedStatus] ||
        "bg-slate-50 text-slate-700 ring-slate-200"
      }`}
    >
      {normalizedStatus || "UNKNOWN"}
    </span>
  );
}