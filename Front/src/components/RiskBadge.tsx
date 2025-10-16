import { cn } from "@/lib/utils";

interface RiskBadgeProps {
  score: number;
  className?: string;
}

export function RiskBadge({ score, className }: RiskBadgeProps) {
  const getRiskLevel = (score: number) => {
    if (score < 0.3) return { label: "Faible", color: "bg-success text-success-foreground" };
    if (score < 0.7) return { label: "Moyen", color: "bg-warning text-warning-foreground" };
    return { label: "Élevé", color: "bg-destructive text-destructive-foreground" };
  };

  const risk = getRiskLevel(score);

  return (
    <span className={cn("px-2 py-1 rounded-full text-xs font-medium", risk.color, className)}>
      {risk.label}
    </span>
  );
}
