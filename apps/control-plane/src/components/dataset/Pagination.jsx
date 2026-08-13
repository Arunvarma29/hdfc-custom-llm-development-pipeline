export default function Pagination({
  pagination,
  onPageChange,
}) {
  const {
    page,
    total,
    total_pages,
    has_next,
    has_previous,
    limit,
  } = pagination;

  const start = total === 0 ? 0 : (page - 1) * limit + 1;
  const end = Math.min(page * limit, total);

  return (
    <div className="mt-6 flex items-center justify-between rounded-xl border border-slate-200 bg-white px-6 py-4 shadow-sm">

      <p className="text-sm text-slate-600">
        Showing <span className="font-semibold">{start}</span>–
        <span className="font-semibold">{end}</span> of{" "}
        <span className="font-semibold">{total}</span> datasets
      </p>

      <div className="flex items-center gap-2">

        <button
          disabled={!has_previous}
          onClick={() => onPageChange(page - 1)}
          className="rounded-lg border px-4 py-2 disabled:cursor-not-allowed disabled:opacity-50 hover:bg-slate-100"
        >
          Previous
        </button>

        <span className="rounded-lg bg-blue-600 px-4 py-2 text-white">
          {page}
        </span>

        <button
          disabled={!has_next}
          onClick={() => onPageChange(page + 1)}
          className="rounded-lg border px-4 py-2 disabled:cursor-not-allowed disabled:opacity-50 hover:bg-slate-100"
        >
          Next
        </button>

      </div>
    </div>
  );
}