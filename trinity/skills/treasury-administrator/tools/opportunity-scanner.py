#!/usr/bin/env python3
"""
UBOS Treasury Grant Opportunity Scanner

Scans EU funding portals for grant opportunities and scores them using
the UBOS qualification framework (5 dimensions, 37.5 max score).

Scoring Dimensions:
1. Budget Alignment (1-5) × 2.0 weight
2. UBOS Fit (1-5) × 1.5 weight
3. Preparation Effort (inverted, 1-5) × 0.5 weight
4. Success Probability (1-5) × 1.5 weight
5. Strategic Impact (1-5) × 2.0 weight

Decision Thresholds:
- 35+: Strategic priority (maximum resources)
- 28-34: High-value target (pursue aggressively)
- 20-27: Worth pursuing if capacity available
- <20: Ignore unless strategic reasons

Usage:
    python opportunity-scanner.py [--json]
    python opportunity-scanner.py --score <budget> <fit> <prep> <success> <impact>
"""

import sys
import json
from typing import Dict, List, Tuple
from decimal import Decimal
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class Opportunity:
    """Grant opportunity data structure."""
    id: str
    program: str
    title: str
    budget_max: int
    deadline: str
    budget_score: int  # 1-5
    fit_score: int  # 1-5
    prep_score: int  # 1-5 (inverted: 5 = easy, 1 = hard)
    success_score: int  # 1-5
    impact_score: int  # 1-5
    url: str = ""
    notes: str = ""

    def calculate_composite_score(self) -> float:
        """
        Calculate composite score using UBOS qualification framework.

        Formula: (Budget × 2) + (Fit × 1.5) + (Prep × 0.5) + (Success × 1.5) + (Impact × 2)
        Maximum: 37.5
        """
        score = (
            (self.budget_score * 2.0) +
            (self.fit_score * 1.5) +
            (self.prep_score * 0.5) +
            (self.success_score * 1.5) +
            (self.impact_score * 2.0)
        )
        return round(score, 2)

    def get_priority_tier(self) -> Tuple[str, str]:
        """
        Determine priority tier based on composite score.

        Returns:
            (tier_name, tier_action)
        """
        score = self.calculate_composite_score()

        if score >= 35:
            return ("STRATEGIC PRIORITY", "Allocate maximum resources, convene Trinity immediately")
        elif score >= 28:
            return ("HIGH-VALUE TARGET", "Pursue aggressively, allocate standard budget")
        elif score >= 20:
            return ("WORTH PURSUING", "Pursue if capacity available, lower priority")
        else:
            return ("IGNORE", "Below threshold unless strategic reasons")


class OpportunityScanner:
    """EU grant opportunity scanner and qualifier."""

    def __init__(self):
        """Initialize scanner."""
        pass

    def scan_portals(self) -> List[Opportunity]:
        """
        Scan EU funding portals for opportunities.

        NOTE: This is a stub for demonstration. Full implementation would:
        - Use requests library to fetch portal HTML
        - Parse HTML with BeautifulSoup
        - Extract call details (title, deadline, budget)
        - Return list of opportunities

        For MVP, returns sample opportunities demonstrating scoring.
        """
        # Sample opportunities for demonstration
        opportunities = [
            Opportunity(
                id="INNOVFUND-2026-LSP-GEO",
                program="Innovation Fund",
                title="Large-Scale Clean Energy Infrastructure",
                budget_max=100_000_000,
                deadline="2026-10-31",
                budget_score=5,  # €70M target
                fit_score=5,  # Perfect fit (geothermal + AI)
                prep_score=2,  # 6 months + consortium (challenging)
                success_score=5,  # 40-50% probability
                impact_score=5,  # Template for 18 EU regions
                url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
                notes="GeoDataCenter primary target - strategic priority"
            ),
            Opportunity(
                id="DIGITAL-EU-2025-AI-FACTORIES",
                program="Digital Europe Programme",
                title="European AI Factories Initiative",
                budget_max=50_000_000,
                deadline="2025-12-15",
                budget_score=5,  # €60M target
                fit_score=5,  # AI infrastructure perfect fit
                prep_score=3,  # 4-6 months, moderate partnerships
                success_score=4,  # 30-40% probability
                impact_score=4,  # High strategic value
                url="https://digital-strategy.ec.europa.eu/",
                notes="Complement to Innovation Fund - dual-track application"
            ),
            Opportunity(
                id="HORIZON-CL5-2025-D3-GEOTHERMAL",
                program="Horizon Europe",
                title="Novel Geothermal Energy Technologies",
                budget_max=6_000_000,
                deadline="2025-09-15",
                budget_score=3,  # €3-6M range
                fit_score=4,  # Strong fit (geothermal R&D)
                prep_score=3,  # 2-4 months, existing relationships
                success_score=2,  # 10-15% success rate (highly competitive)
                impact_score=3,  # Moderate strategic value
                url="https://ec.europa.eu/info/funding-tenders/opportunities/portal/",
                notes="Pre-commercial R&D to strengthen Innovation Fund proposal"
            ),
            Opportunity(
                id="ERDF-RO-2025-DIGITAL-INFRA",
                program="ERDF Romania",
                title="Digital Infrastructure - Bihor County",
                budget_max=10_000_000,
                deadline="2025-11-30",
                budget_score=4,  # €5-10M range
                fit_score=4,  # Strong fit (site preparation)
                prep_score=4,  # 1-2 months, local coordination
                success_score=4,  # 30-40% (regional priority)
                impact_score=3,  # Moderate (enables GeoDataCenter site prep)
                url="https://www.fonduri-ue.ro/",
                notes="Site preparation co-funding for GeoDataCenter"
            ),
            Opportunity(
                id="INTERREG-RO-HU-2025-GREEN",
                program="Romania-Hungary Interreg",
                title="Cross-Border Green Energy Cooperation",
                budget_max=5_000_000,
                deadline="2025-08-31",
                budget_score=3,  # €3-5M range
                fit_score=3,  # Moderate fit (cross-border reservoir)
                prep_score=2,  # 4-6 months, need Hungarian partner
                success_score=3,  # 20-30% (competitive)
                impact_score=2,  # Some strategic value
                url="https://rohu.eu/",
                notes="Cross-border research, lower priority"
            ),
            Opportunity(
                id="SAMPLE-LOW-BUDGET",
                program="Regional Innovation Grant",
                title="SME Digital Transformation",
                budget_max=100_000,
                deadline="2025-07-15",
                budget_score=1,  # <€100K (too small)
                fit_score=2,  # Weak fit
                prep_score=5,  # <1 month (easy)
                success_score=4,  # 30-40%
                impact_score=1,  # One-off, no replication
                url="",
                notes="Below threshold - ignore"
            ),
        ]

        return opportunities

    def score_opportunity(
        self,
        budget: int,
        fit: int,
        prep: int,
        success: int,
        impact: int
    ) -> Dict:
        """
        Score a single opportunity using qualification framework.

        Args:
            budget: Budget score (1-5)
            fit: UBOS fit score (1-5)
            prep: Preparation effort score (1-5, inverted)
            success: Success probability score (1-5)
            impact: Strategic impact score (1-5)

        Returns:
            Dict with composite score, tier, and recommendations
        """
        # Validate scores
        for score_name, score_value in [
            ('budget', budget), ('fit', fit), ('prep', prep),
            ('success', success), ('impact', impact)
        ]:
            if not (1 <= score_value <= 5):
                raise ValueError(f"{score_name} score must be 1-5, got {score_value}")

        # Create temporary opportunity for scoring
        opp = Opportunity(
            id="CUSTOM",
            program="Custom",
            title="Custom Opportunity",
            budget_max=0,
            deadline="TBD",
            budget_score=budget,
            fit_score=fit,
            prep_score=prep,
            success_score=success,
            impact_score=impact
        )

        composite = opp.calculate_composite_score()
        tier, action = opp.get_priority_tier()

        return {
            'composite_score': composite,
            'max_score': 37.5,
            'priority_tier': tier,
            'recommended_action': action,
            'breakdown': {
                'budget': f"{budget} × 2.0 = {budget * 2.0}",
                'fit': f"{fit} × 1.5 = {fit * 1.5}",
                'prep': f"{prep} × 0.5 = {prep * 0.5}",
                'success': f"{success} × 1.5 = {success * 1.5}",
                'impact': f"{impact} × 2.0 = {impact * 2.0}",
            }
        }

    def generate_report(
        self,
        opportunities: List[Opportunity],
        format_type: str = 'text'
    ) -> str:
        """
        Generate opportunity scanner report.

        Args:
            opportunities: List of scanned opportunities
            format_type: 'text' or 'json'

        Returns:
            Formatted report string
        """
        # Calculate composite scores and sort
        scored_opps = [
            (opp, opp.calculate_composite_score(), opp.get_priority_tier())
            for opp in opportunities
        ]
        scored_opps.sort(key=lambda x: x[1], reverse=True)

        if format_type == 'json':
            output_list = []
            for opp, score, (tier, action) in scored_opps:
                opp_dict = asdict(opp)
                opp_dict['composite_score'] = score
                opp_dict['priority_tier'] = tier
                opp_dict['recommended_action'] = action
                output_list.append(opp_dict)

            return json.dumps({
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'total_opportunities': len(opportunities),
                'opportunities': output_list
            }, indent=2)

        # Text format
        lines = [
            "=" * 90,
            "UBOS TREASURY GRANT OPPORTUNITY SCANNER",
            f"Scan Date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
            "=" * 90,
            "",
            f"Total Opportunities Scanned: {len(opportunities)}",
            "",
        ]

        # Group by priority tier
        strategic = [x for x in scored_opps if x[1] >= 35]
        high_value = [x for x in scored_opps if 28 <= x[1] < 35]
        worth_pursuing = [x for x in scored_opps if 20 <= x[1] < 28]
        ignore = [x for x in scored_opps if x[1] < 20]

        lines.extend([
            "PRIORITY BREAKDOWN:",
            "-" * 90,
            f"  Strategic Priority (≥35):     {len(strategic)}",
            f"  High-Value Target (28-34):    {len(high_value)}",
            f"  Worth Pursuing (20-27):       {len(worth_pursuing)}",
            f"  Ignore (<20):                 {len(ignore)}",
            "",
        ])

        # Detailed listings
        for tier_name, tier_list in [
            ("STRATEGIC PRIORITY OPPORTUNITIES (≥35)", strategic),
            ("HIGH-VALUE TARGET OPPORTUNITIES (28-34)", high_value),
            ("WORTH PURSUING OPPORTUNITIES (20-27)", worth_pursuing),
        ]:
            if tier_list:
                lines.extend([
                    tier_name,
                    "=" * 90,
                ])

                for opp, score, (tier, action) in tier_list:
                    lines.extend([
                        f"[Score: {score:.2f}/37.5] {opp.program} - {opp.title}",
                        f"  ID: {opp.id}",
                        f"  Budget: €{opp.budget_max:,}  |  Deadline: {opp.deadline}",
                        f"  Scores: Budget={opp.budget_score}, Fit={opp.fit_score}, Prep={opp.prep_score}, Success={opp.success_score}, Impact={opp.impact_score}",
                        f"  Composite: {score:.2f} → {tier}",
                        f"  Action: {action}",
                        f"  Notes: {opp.notes}",
                        "",
                    ])

        # Summary recommendations
        lines.extend([
            "=" * 90,
            "TREASURY ADMINISTRATOR RECOMMENDATIONS:",
            "-" * 90,
        ])

        if strategic:
            lines.append(f"🚨 URGENT: {len(strategic)} strategic priority opportunity(ies) detected!")
            lines.append("   → Convene Trinity immediately")
            lines.append("   → Allocate Omega tier budget (€75K-€150K)")
            lines.append("")

        if high_value:
            lines.append(f"🎯 {len(high_value)} high-value target(s) identified")
            lines.append("   → Allocate Alpha tier budget (€50K-€75K)")
            lines.append("   → Begin consortium outreach")
            lines.append("")

        if worth_pursuing:
            lines.append(f"📋 {len(worth_pursuing)} opportunity(ies) worth pursuing if capacity available")
            lines.append("   → Monitor, pursue if strategic fit")
            lines.append("")

        if ignore:
            lines.append(f"⏸️  {len(ignore)} opportunity(ies) below threshold (archived)")
            lines.append("")

        lines.append("=" * 90)

        return "\n".join(lines)


def main():
    """Main entry point for CLI usage."""
    if '--score' in sys.argv:
        # Manual scoring mode
        try:
            idx = sys.argv.index('--score')
            budget = int(sys.argv[idx + 1])
            fit = int(sys.argv[idx + 2])
            prep = int(sys.argv[idx + 3])
            success = int(sys.argv[idx + 4])
            impact = int(sys.argv[idx + 5])
        except (IndexError, ValueError):
            print("Usage: python opportunity-scanner.py --score <budget> <fit> <prep> <success> <impact>")
            print("Example: python opportunity-scanner.py --score 5 5 2 5 5")
            print("All scores must be 1-5")
            sys.exit(1)

        scanner = OpportunityScanner()
        result = scanner.score_opportunity(budget, fit, prep, success, impact)

        print("OPPORTUNITY SCORING RESULT:")
        print("=" * 70)
        print(f"Composite Score: {result['composite_score']:.2f} / {result['max_score']}")
        print(f"Priority Tier: {result['priority_tier']}")
        print(f"Recommended Action: {result['recommended_action']}")
        print("\nBreakdown:")
        for dimension, calculation in result['breakdown'].items():
            print(f"  {dimension.title():10} {calculation}")
        print("=" * 70)

        sys.exit(0)

    # Default mode: Scan portals
    format_type = 'json' if '--json' in sys.argv else 'text'

    scanner = OpportunityScanner()
    opportunities = scanner.scan_portals()
    report = scanner.generate_report(opportunities, format_type)

    print(report)

    # Alert on strategic priorities
    strategic_count = sum(
        1 for opp in opportunities
        if opp.calculate_composite_score() >= 35
    )
    sys.exit(0 if strategic_count == 0 else 2)  # Exit 2 = strategic priority detected


if __name__ == '__main__':
    main()
