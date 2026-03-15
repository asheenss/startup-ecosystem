import { fetchJson } from "../../../lib/api";
import { investorDashboard as fallback } from "../../../lib/mock-data";
import { InvestorDashboardContent } from "../../../components/dashboard/InvestorDashboardContent";

export default async function InvestorDashboardPage({
  searchParams
}: {
  searchParams?: Promise<{ user?: string }>;
}) {
  const params = await searchParams;
  const user = params?.user ?? "2";
  const data = await fetchJson(`/dashboard/investor/${user}`, fallback);

  return <InvestorDashboardContent initialData={data} />;
}
