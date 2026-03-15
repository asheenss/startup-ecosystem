import { fetchJson } from "../../../lib/api";
import { founderDashboard as fallback } from "../../../lib/mock-data";
import { FounderDashboardContent } from "../../../components/dashboard/FounderDashboardContent";

export default async function FounderDashboardPage({
  searchParams
}: {
  searchParams?: Promise<{ user?: string }>;
}) {
  const params = await searchParams;
  const user = params?.user ?? "1";
  const initialData = await fetchJson(`/dashboard/founder/${user}`, fallback);

  return <FounderDashboardContent initialData={initialData} userId={user} />;
}
