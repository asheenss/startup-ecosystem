import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { EntityCard } from "@/components/dashboard/EntityCard";
import { fetchJson } from "@/lib/api";
import { Rocket } from "lucide-react";

export default async function StartupsDirectoryPage() {
  // In a real app, we'd fetch actual startups
  const startups = await fetchJson("/startups", [
    { id: 1, name: "DevBridge AI", industry: "DevTools", stage: "Seed" },
    { id: 2, name: "TalentGrid", industry: "HR Tech", stage: "Pre-seed" },
    { id: 3, name: "EcoStream", industry: "Sustainability", stage: "Series A" },
    { id: 4, name: "HealthPal", industry: "HealthTech", stage: "Seed" },
  ]);

  return (
    <DashboardShell
      title="Startup Directory"
      subtitle="Explore and filter all startups across the ecosystem."
    >
      <div className="flex flex-col gap-4">
        {startups.map((startup: any) => (
          <EntityCard
            key={startup.id}
            title={startup.name}
            subtitle={`${startup.industry} | ${startup.stage}`}
            icon={<Rocket className="text-primary" size={20} />}
          />
        ))}
      </div>
    </DashboardShell>
  );
}
