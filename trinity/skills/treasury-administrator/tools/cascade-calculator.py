#!/usr/bin/env python3
"""
UBOS Treasury Revenue Cascade Calculator

Constitutional Amendment UBOS-AMEND-001 Article III Section 3.2
Revenue Cascade Formula: 20/10/15/40/15

Usage:
    python cascade-calculator.py <revenue_amount>
    python cascade-calculator.py 1000.00

Output:
    Constitutional allocation breakdown for the given revenue amount.
"""

import sys
import json
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
from typing import Dict, Tuple


class CascadeCalculator:
    """
    Constitutional revenue cascade calculator.

    Implements UBOS-AMEND-001 Article III Section 3.2:
    - Constitutional Reserve: 20%
    - Oracle Operations Pool: 10%
    - Infrastructure Maintenance: 15%
    - Active Projects: 40%
    - Innovation Pool: 15%
    """

    # Constitutional allocation percentages (UBOS-AMEND-001 Art III Sec 3.2)
    ALLOCATIONS = {
        'constitutional_reserve': Decimal('0.20'),
        'oracle_operations_pool': Decimal('0.10'),
        'infrastructure_maintenance': Decimal('0.15'),
        'active_projects': Decimal('0.40'),
        'innovation_pool': Decimal('0.15'),
    }

    def __init__(self):
        """Initialize cascade calculator."""
        # Verify constitutional formula sums to 100%
        total = sum(self.ALLOCATIONS.values())
        if total != Decimal('1.00'):
            raise ValueError(
                f"Constitutional formula error: Allocations sum to {total}, must be 1.00"
            )

    def calculate(self, revenue: float) -> Dict[str, Decimal]:
        """
        Calculate constitutional allocation for given revenue.

        Args:
            revenue: Revenue amount to allocate (EUR)

        Returns:
            Dict mapping pool names to allocated amounts (Decimal for precision)
        """
        revenue_decimal = Decimal(str(revenue))

        allocations = {}
        total_allocated = Decimal('0.00')

        for pool_name, percentage in self.ALLOCATIONS.items():
            amount = (revenue_decimal * percentage).quantize(
                Decimal('0.01'), rounding=ROUND_HALF_UP
            )
            allocations[pool_name] = amount
            total_allocated += amount

        # Handle rounding discrepancies (ensure total = revenue)
        # If rounding created gap, adjust Active Projects pool (largest allocation)
        gap = revenue_decimal - total_allocated
        if gap != Decimal('0.00'):
            allocations['active_projects'] += gap

        return allocations

    def verify_compliance(
        self,
        revenue: float,
        allocations: Dict[str, Decimal]
    ) -> Tuple[bool, str]:
        """
        Verify allocation compliance with constitutional formula.

        Args:
            revenue: Original revenue amount
            allocations: Calculated allocations

        Returns:
            (is_compliant, message)
        """
        revenue_decimal = Decimal(str(revenue))

        # Check 1: Total equals revenue
        total = sum(allocations.values())
        if total != revenue_decimal:
            return (
                False,
                f"Total allocation {total} ≠ revenue {revenue_decimal}"
            )

        # Check 2: Each pool within tolerance (±€0.02 for rounding)
        tolerance = Decimal('0.02')
        for pool_name, percentage in self.ALLOCATIONS.items():
            expected = revenue_decimal * percentage
            actual = allocations[pool_name]
            diff = abs(actual - expected)

            if diff > tolerance:
                return (
                    False,
                    f"{pool_name}: Expected {expected}, got {actual} (diff {diff} > tolerance {tolerance})"
                )

        return (True, "Constitutional compliance: 100%")

    def format_output(
        self,
        revenue: float,
        allocations: Dict[str, Decimal],
        format_type: str = 'text'
    ) -> str:
        """
        Format allocation output.

        Args:
            revenue: Original revenue amount
            allocations: Calculated allocations
            format_type: 'text' or 'json'

        Returns:
            Formatted output string
        """
        if format_type == 'json':
            output_dict = {
                'revenue': float(revenue),
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'allocations': {
                    pool: float(amount) for pool, amount in allocations.items()
                },
                'constitutional_reference': 'UBOS-AMEND-001 Art III Sec 3.2'
            }
            return json.dumps(output_dict, indent=2)

        # Text format
        is_compliant, compliance_msg = self.verify_compliance(revenue, allocations)

        lines = [
            "=" * 70,
            "UBOS TREASURY REVENUE CASCADE CALCULATOR",
            "Constitutional Amendment UBOS-AMEND-001 Article III Section 3.2",
            "=" * 70,
            "",
            f"Revenue Amount: €{revenue:,.2f}",
            "",
            "ALLOCATION BREAKDOWN:",
            "-" * 70,
        ]

        for pool_name, amount in allocations.items():
            percentage = self.ALLOCATIONS[pool_name] * 100
            pool_display = pool_name.replace('_', ' ').title()
            lines.append(
                f"  {pool_display:35} €{float(amount):>10,.2f}  ({percentage:>5.1f}%)"
            )

        total = sum(allocations.values())
        lines.extend([
            "-" * 70,
            f"  {'TOTAL':35} €{float(total):>10,.2f}  (100.0%)",
            "",
            f"Constitutional Compliance: {'✅ PASS' if is_compliant else '❌ FAIL'}",
            f"  {compliance_msg}",
            "",
            "=" * 70,
        ])

        return "\n".join(lines)


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python cascade-calculator.py <revenue_amount> [format]")
        print("Example: python cascade-calculator.py 1000.00")
        print("Example: python cascade-calculator.py 1000.00 json")
        sys.exit(1)

    try:
        revenue = float(sys.argv[1])
    except ValueError:
        print(f"Error: Invalid revenue amount '{sys.argv[1]}'")
        print("Must be a numeric value (e.g., 1000.00)")
        sys.exit(1)

    if revenue < 0:
        print("Error: Revenue amount must be positive")
        sys.exit(1)

    format_type = 'text'
    if len(sys.argv) >= 3:
        format_type = sys.argv[2].lower()
        if format_type not in ['text', 'json']:
            print(f"Error: Invalid format '{format_type}'. Must be 'text' or 'json'")
            sys.exit(1)

    calculator = CascadeCalculator()
    allocations = calculator.calculate(revenue)
    output = calculator.format_output(revenue, allocations, format_type)

    print(output)

    # Exit code: 0 if compliant, 1 if not
    is_compliant, _ = calculator.verify_compliance(revenue, allocations)
    sys.exit(0 if is_compliant else 1)


if __name__ == '__main__':
    main()
