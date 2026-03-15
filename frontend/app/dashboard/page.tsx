import { redirect } from "next/navigation";

export default function DashboardPage() {
  // Simple default redirect to founder dashboard for now
  // In a real app, this would check user role from session/context
  redirect("/dashboard/founder?user=1");
}
