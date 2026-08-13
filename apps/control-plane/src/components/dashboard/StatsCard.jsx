export default function StatsCard({
  title,
  value,
  icon: Icon,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

      <div className="flex items-center justify-between">

        <div>

          <p className="text-sm text-slate-500">
            {title}
          </p>

          <h2 className="mt-2 text-3xl font-bold text-slate-900">
            {value}
          </h2>

        </div>

        <div className="rounded-full bg-blue-100 p-4">

          <Icon
            size={24}
            className="text-blue-600"
          />

        </div>

      </div>

    </div>
  );
}