import { FaEye, FaTrash } from "react-icons/fa";
import StatusBadge from "./StatusBadge";

export default function DatasetRow({
  dataset,
  onDelete,
  onView,
}) {
  return (
    <tr className="border-b border-slate-100 transition hover:bg-slate-50 last:border-0">
      {/* Dataset */}
      <td className="px-5 py-4">
        <div className="min-w-0">
          <p className="truncate text-sm font-semibold text-slate-900">
            {dataset.name}
          </p>

          <p className="mt-1 truncate text-xs text-slate-500">
            v{dataset.version}
          </p>
        </div>
      </td>

      {/* Type */}
      <td className="px-5 py-4">
        <span className="inline-flex rounded-lg bg-slate-100 px-2.5 py-1 text-xs font-medium capitalize text-slate-600">
          {dataset.dataset_type}
        </span>
      </td>

      {/* Status */}
      <td className="px-5 py-4">
        <StatusBadge status={dataset.status} />
      </td>

      {/* Actions */}
      <td className="px-5 py-4">
        <div className="flex justify-end gap-2">
          <button
            onClick={() => onView(dataset)}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 transition hover:bg-blue-50 hover:text-blue-600"
            title="View Details"
            aria-label="View Details"
          >
            <FaEye size={14} />
          </button>

          <button
            onClick={() => onDelete(dataset)}
            className="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 transition hover:bg-red-50 hover:text-red-600"
            title="Delete"
            aria-label="Delete"
          >
            <FaTrash size={13} />
          </button>
        </div>
      </td>
    </tr>
  );
}