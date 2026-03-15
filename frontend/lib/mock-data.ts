export const founderDashboard = {
  startup_overview: {
    startup_name: "DevBridge AI",
    industry: "Developer Tools",
    stage: "Seed",
    funding_needed: 450000
  },
  latest_analysis: {
    score: 82,
    status: "completed",
    problem_clarity: 84,
    market_size: 79,
    traction: 76,
    team_strength: 85,
    financial_potential: 81,
    improvement_suggestions: "Clarify target persona.\nAdd pricing proof.\nShow pipeline conversion."
  },
  investor_matches: [
    { investor_name: "Atlas Capital", match_score: 92, preferred_industries: ["developer tools", "ai"] },
    { investor_name: "Kernel Ventures", match_score: 86, preferred_industries: ["developer tools"] }
  ],
  event_recommendations: [
    { id: 1, title: "Founders x Builders Night", description: "Meet founders, investors, and senior engineers.", location: "Dubai", event_date: "2026-04-03T18:00:00Z" }
  ]
};

export const investorDashboard = {
  metrics: {
    total_startups_discovered: 124,
    new_startups_this_week: 11,
    top_rated_startups: 8,
    startups_seeking_funding: 67
  },
  recommended_startups: [
    { id: 1, startup_name: "DevBridge AI", industry: "Developer Tools", stage: "Seed", funding_needed: 450000 },
    { id: 2, startup_name: "TalentGrid", industry: "HR Tech", stage: "Pre-seed", funding_needed: 200000 }
  ],
  pipeline: {
    interested: [{ id: 1, startup_name: "DevBridge AI", stage: "Seed" }],
    reviewing: [{ id: 2, startup_name: "TalentGrid", stage: "Pre-seed" }],
    meeting: [],
    invested: []
  }
};

export const adminDashboard = {
  metrics: {
    total_startups: 124,
    total_investors: 39,
    events_hosted: 14,
    evaluations_generated: 97,
    connections_requested: 53,
    event_registrations: 218
  },
  industry_distribution: { "Developer Tools": 28, Fintech: 22, HealthTech: 17, ClimateTech: 13 },
  stage_distribution: { Idea: 19, "Pre-seed": 37, Seed: 49, "Series A": 19 }
};
