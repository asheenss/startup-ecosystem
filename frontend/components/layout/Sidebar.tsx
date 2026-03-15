"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  BarChart3, 
  Rocket, 
  Users, 
  Search, 
  Calendar, 
  Settings, 
  LayoutDashboard,
  BrainCircuit,
  LogOut
} from "lucide-react";
import { cn } from "@/lib/utils";

const navigation = [
  { name: "Founder", href: "/dashboard/founder?user=1", icon: LayoutDashboard },
  { name: "Investor", href: "/dashboard/investor?user=2", icon: Search },
  { name: "Admin", href: "/dashboard/admin", icon: BarChart3 },
  { name: "All Startups", href: "/dashboard/startups", icon: Rocket },
  { name: "Events", href: "/dashboard/events", icon: Calendar },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="sidebar">
      <div className="flex items-center gap-3 px-4 mb-10">
        <div className="w-10 h-10 bg-primary rounded-2xl flex items-center justify-center shadow-glow">
          <Rocket className="w-6 h-6 text-canvas" />
        </div>
        <h1 className="text-xl font-bold tracking-tight">EcoSystem<span className="text-primary italic">AI</span></h1>
      </div>

      <nav className="flex-1 space-y-2">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "nav-link",
                isActive && "nav-link-active"
              )}
            >
              <item.icon className="w-5 h-5" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="mt-auto pt-6 border-t border-white/10 space-y-2">
        <Link href="/dashboard/settings" className="nav-link">
          <Settings className="w-5 h-5" />
          <span>Settings</span>
        </Link>
        <button className="nav-link w-full text-red-400/70 hover:text-red-400 hover:bg-red-400/5">
          <LogOut className="w-5 h-5" />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
}
