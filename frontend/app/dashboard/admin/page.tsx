import { fetchJson } from "../../../lib/api";
import { adminDashboard as fallback } from "../../../lib/mock-data";
import { AdminDashboardContent } from "../../../components/dashboard/AdminDashboardContent";

export default async function AdminDashboardPage() {
  const data = await fetchJson("/dashboard/admin", fallback);

  return <AdminDashboardContent initialData={data} />;
}
