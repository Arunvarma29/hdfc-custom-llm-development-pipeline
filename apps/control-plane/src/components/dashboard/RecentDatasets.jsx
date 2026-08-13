export default function RecentDatasets({
  datasets,
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">

      <h2 className="mb-6 text-lg font-semibold text-slate-900">
        Recent Dataset Uploads
      </h2>

      <table className="w-full">

        <thead>

          <tr className="border-b">

            <th className="py-3 text-left text-sm text-slate-500">
              Name
            </th>

            <th className="py-3 text-left text-sm text-slate-500">
              Type
            </th>

            <th className="py-3 text-left text-sm text-slate-500">
              Status
            </th>

          </tr>

        </thead>

        <tbody>

          {datasets.map((dataset) => (

            <tr
              key={dataset.name}
              className="border-b last:border-0"
            >

              <td className="py-4 font-medium">
                {dataset.name}
              </td>

              <td className="py-4">
                {dataset.type}
              </td>

              <td className="py-4">
                {dataset.status}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );
}