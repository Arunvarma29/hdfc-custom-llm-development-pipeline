import PageHeader from "@/components/common/PageHeader";
import Dashboard from "@/components/dashboard/Dashboard";

export default function OverviewPage() {
  return (
    <>
      <PageHeader
        title="Overview"
        description="Monitor your AI pipeline from a single dashboard."
      />

      <Dashboard />
    </>
  );
}