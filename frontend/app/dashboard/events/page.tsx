import { DashboardShell } from "@/components/dashboard/DashboardShell";
import { EntityCard } from "@/components/dashboard/EntityCard";
import { fetchJson } from "@/lib/api";
import { Calendar } from "lucide-react";

export default async function EventsDirectoryPage() {
  const events = await fetchJson("/events", [
    { id: 1, title: "Founders x Builders Night", date: "April 3, 2026", location: "Dubai" },
    { id: 2, title: "Seed Stage Demo Day", date: "April 10, 2026", location: "Global / Remote" },
    { id: 3, title: "AI in Fintech Summit", date: "May 15, 2026", location: "London" },
  ]);

  return (
    <DashboardShell
      title="Platform Events"
      subtitle="Networking events, demo days, and ecosystem summits."
    >
      <div className="grid-2">
        {events.map((event: any) => (
          <EntityCard
            key={event.id}
            title={event.title}
            subtitle={`${event.date} | ${event.location}`}
            icon={<Calendar className="text-primary" size={20} />}
          />
        ))}
      </div>
    </DashboardShell>
  );
}
