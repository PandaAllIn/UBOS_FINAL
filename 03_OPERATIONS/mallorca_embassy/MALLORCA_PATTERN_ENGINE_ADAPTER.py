#!/usr/bin/env python3
"""
Mallorca/XYL-PHOS-CURE Mission Adapter for UBOS Pattern Engine

This adapter HOOKS INTO the existing Pattern Engine Core to monitor:
- EU Funding Pulse (Stage 1 results, Stage 2 timeline)
- Scientific Precedent (competitive papers/patents)
- Partner Availability (UIB-INAGEA, CIHEAM-Bari activity)
- Market Demand (Xylella outbreak reports, crop prices)

DOES NOT replace Pattern Engine - just adds Mallorca-specific datastreams.
"""
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
import json

# Hook into existing Pattern Engine
PATTERN_ENGINE_PATH = Path("/srv/janus/balaur/projects/05_software/pattern_engine")
if PATTERN_ENGINE_PATH.exists():
    sys.path.insert(0, str(PATTERN_ENGINE_PATH.parent))
    from pattern_engine.pattern_engine_core import PatternEngineCore
else:
    # Fallback for development
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "balaur/projects/05_software"))
    from pattern_engine.pattern_engine_core import PatternEngineCore

# Hook into Oracle Bridge for Perplexity/Wolfram/Data Commons
TRINITY_PATH = Path("/srv/janus/trinity")
if TRINITY_PATH.exists():
    sys.path.insert(0, str(TRINITY_PATH.parent))
    from trinity.oracle_bridge import OracleBridge
else:
    # Fallback for development
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "trinity"))
    from trinity.oracle_bridge import OracleBridge


@dataclass
class MallorcaSignal:
    """Signal specific to Mallorca/XYL-PHOS-CURE mission"""
    stream_id: str  # 'eu_funding', 'scientific', 'partner', 'market', 'stage1'
    timestamp: float
    data: Dict
    metrics: Optional[Dict] = None  # Pattern Engine metrics
    alert_level: Optional[str] = None  # LOW/MEDIUM/HIGH/CRITICAL


class MallorcaPatternEngineAdapter:
    """
    Adapter that connects Mallorca mission monitoring to existing Pattern Engine.
    
    Does NOT modify Pattern Engine Core - just feeds mission-specific data to it.
    """
    
    def __init__(
        self,
        mission_dir: Path,
        pattern_engine: Optional[PatternEngineCore] = None,
        oracle_bridge: Optional[OracleBridge] = None
    ):
        """
        Initialize adapter with mission directory and existing infrastructure.
        
        Args:
            mission_dir: Path to mallorca_embassy folder
            pattern_engine: Existing Pattern Engine instance (or creates new)
            oracle_bridge: Existing Oracle Bridge instance (or creates new)
        """
        self.mission_dir = mission_dir
        self.signals_dir = mission_dir / "signals"
        self.signals_dir.mkdir(parents=True, exist_ok=True)
        
        # Use existing Pattern Engine or create mission-specific instance
        if pattern_engine:
            self.pattern_engine = pattern_engine
        else:
            # Create mission-specific instance
            self.pattern_engine = PatternEngineCore(
                project_dir=mission_dir / "pattern_engine_artifacts",
                orchestrion_spec=mission_dir / "MALLORCA_MISSION_SPEC.md"
            )
        
        # Use existing Oracle Bridge
        self.oracle_bridge = oracle_bridge
        
        # Mission-specific thresholds
        self.thresholds = {
            'eu_funding': {'resonance': 0.85, 'entropy': 0.40},
            'scientific': {'cohesion': 0.70, 'resonance': 0.80},
            'partner': {'entropy': 0.40, 'integrity': 0.85},
            'market': {'integrity': 0.85, 'resonance': 0.90},
            'stage1': {'any_change': True}  # ANY status change = alert
        }
    
    # ------------------------------------------------------------------
    # Public API - Monitor Mallorca-specific datastreams
    # ------------------------------------------------------------------
    
    def monitor_stage1_results(self) -> Optional[MallorcaSignal]:
        """
        Monitor EU portal for Stage 1 results (proposal 101271185-1).
        
        This is PRIORITY OVERRIDE stream - ANY change triggers alert.
        """
        # TODO: Implement EU portal scraping or API check
        # For now, returns None (manual check required)
        
        # When implemented, would check:
        # - EU Funding & Tenders Portal status
        # - Email notifications
        # - CORDIS database updates
        
        signal = MallorcaSignal(
            stream_id='stage1_results_pulse',
            timestamp=datetime.now(timezone.utc).timestamp(),
            data={'status': 'pending', 'last_check': datetime.now(timezone.utc).isoformat()},
            alert_level='MONITORING'
        )
        
        self._save_signal(signal)
        return signal
    
    def monitor_scientific_precedent(self, use_oracle: bool = True) -> MallorcaSignal:
        """
        Monitor for competitive research on phosphinate/Xylella.
        
        Args:
            use_oracle: If True, use Oracle Bridge for Perplexity queries
        
        Returns:
            Signal with Pattern Engine metrics
        """
        keywords = [
            'phosphinic acid',
            'phosphonate plant pathogen',
            'xylella fastidiosa cure',
            'fosfomycin plant',
            'systemic bactericide'
        ]
        
        # Collect frequency data (would be real RSS/PubMed scraping in production)
        frequency_data = self._mock_frequency_data(keywords)  # TODO: Real implementation
        
        # Feed to Pattern Engine
        # Convert to time series format Pattern Engine expects
        timestamps = [d['timestamp'] for d in frequency_data]
        amplitudes = [d['mentions'] for d in frequency_data]
        
        # Pattern Engine analysis (using existing infrastructure)
        window = (
            [t for t in timestamps],
            [a for a in amplitudes]
        )
        # metrics = self.pattern_engine._compute_metrics(window)
        
        # For now, mock metrics (real Pattern Engine would compute)
        metrics = {
            'entropy': 0.70,  # Moderate volatility
            'resonance': 0.75,  # Some cross-correlation
            'cohesion': 0.65,  # Gradual emergence
            'integrity': 0.80   # Good signal quality
        }
        
        # Determine alert level based on thresholds
        alert_level = self._classify_alert('scientific', metrics)
        
        signal = MallorcaSignal(
            stream_id='scientific_precedent_pulse',
            timestamp=datetime.now(timezone.utc).timestamp(),
            data={'keywords': keywords, 'frequency_data': frequency_data},
            metrics=metrics,
            alert_level=alert_level
        )
        
        # If CRITICAL, trigger Oracle query for chemical analysis
        if alert_level == 'CRITICAL' and use_oracle and self.oracle_bridge:
            chemical_analysis = self._query_wolfram_chemical_similarity()
            signal.data['oracle_analysis'] = chemical_analysis
        
        self._save_signal(signal)
        return signal
    
    def monitor_partner_availability(self) -> MallorcaSignal:
        """
        Monitor UIB-INAGEA, CIHEAM-Bari publication/project activity.
        
        Low entropy = stable landscape = optimal outreach window.
        """
        partners = ['UIB-INAGEA', 'CIHEAM-Bari', 'CSIC-QuantaLab']
        
        # Collect activity metrics (would be ResearchGate/ORCID scraping in production)
        activity_data = self._mock_partner_activity(partners)  # TODO: Real implementation
        
        # Pattern Engine analysis
        # Low entropy = predictable activity = good time to approach
        metrics = {
            'entropy': 0.30,  # Low = stable
            'resonance': 0.82,  # High alignment with our needs
            'cohesion': 0.65,
            'integrity': 0.90   # High quality signal
        }
        
        alert_level = self._classify_alert('partner', metrics)
        
        signal = MallorcaSignal(
            stream_id='partner_availability_pulse',
            timestamp=datetime.now(timezone.utc).timestamp(),
            data={'partners': partners, 'activity_data': activity_data},
            metrics=metrics,
            alert_level=alert_level
        )
        
        self._save_signal(signal)
        return signal
    
    def monitor_market_demand(self) -> MallorcaSignal:
        """
        Monitor Xylella outbreak reports, farmer sentiment, crop prices.
        
        High signal integrity + resonance = validated market urgency.
        """
        indicators = [
            'xylella_outbreak_reports',
            'olive_oil_prices',
            'almond_prices',
            'farmer_sentiment',
            'eu_policy_shifts'
        ]
        
        # Collect market data (would be EPPO alerts, price APIs in production)
        market_data = self._mock_market_data(indicators)  # TODO: Real implementation
        
        # Pattern Engine analysis
        metrics = {
            'entropy': 0.75,  # High = volatile market
            'resonance': 0.88,  # Multiple indicators align
            'cohesion': 0.70,
            'integrity': 0.85   # High quality signal
        }
        
        alert_level = self._classify_alert('market', metrics)
        
        signal = MallorcaSignal(
            stream_id='market_demand_pulse',
            timestamp=datetime.now(timezone.utc).timestamp(),
            data={'indicators': indicators, 'market_data': market_data},
            metrics=metrics,
            alert_level=alert_level
        )
        
        # If CRITICAL, trigger Oracle query for economic quantification
        if alert_level == 'CRITICAL' and self.oracle_bridge:
            economic_data = self._query_data_commons_timeseries()
            signal.data['oracle_analysis'] = economic_data
        
        self._save_signal(signal)
        return signal
    
    def monitor_eu_funding_pulse(self) -> MallorcaSignal:
        """
        Monitor Horizon Europe calls, Agriculture of Data, EIC Accelerator.
        
        High resonance = multiple programs mentioning similar themes = cluster opportunity.
        """
        programs = [
            'horizon_europe',
            'agriculture_of_data',
            'eic_accelerator',
            'innovation_fund',
            'digital_europe'
        ]
        
        # Collect funding signals (would be RSS/API scraping in production)
        funding_data = self._mock_funding_data(programs)  # TODO: Real implementation
        
        # Pattern Engine analysis
        metrics = {
            'entropy': 0.50,  # Moderate stability
            'resonance': 0.80,  # Strong cross-program alignment
            'cohesion': 0.60,
            'integrity': 0.85
        }
        
        alert_level = self._classify_alert('eu_funding', metrics)
        
        signal = MallorcaSignal(
            stream_id='eu_funding_pulse',
            timestamp=datetime.now(timezone.utc).timestamp(),
            data={'programs': programs, 'funding_data': funding_data},
            metrics=metrics,
            alert_level=alert_level
        )
        
        self._save_signal(signal)
        return signal
    
    # ------------------------------------------------------------------
    # Alert Classification & Actions
    # ------------------------------------------------------------------
    
    def _classify_alert(self, stream_id: str, metrics: Dict) -> str:
        """
        Classify alert level based on stream-specific thresholds.
        
        Args:
            stream_id: Which datastream (eu_funding, scientific, etc.)
            metrics: Pattern Engine metrics
        
        Returns:
            'LOW', 'MEDIUM', 'HIGH', or 'CRITICAL'
        """
        thresholds = self.thresholds.get(stream_id, {})
        
        critical_conditions = 0
        high_conditions = 0
        
        # Check stream-specific thresholds
        if 'resonance' in thresholds:
            if metrics.get('resonance', 0) > thresholds['resonance']:
                critical_conditions += 1
        
        if 'entropy' in thresholds:
            if metrics.get('entropy', 1) < thresholds['entropy']:
                high_conditions += 1
        
        if 'cohesion' in thresholds:
            if metrics.get('cohesion', 0) > thresholds['cohesion']:
                high_conditions += 1
        
        if 'integrity' in thresholds:
            if metrics.get('integrity', 0) > thresholds['integrity']:
                high_conditions += 1
        
        # Classification logic
        if critical_conditions >= 2:
            return 'CRITICAL'
        elif critical_conditions >= 1 or high_conditions >= 2:
            return 'HIGH'
        elif high_conditions >= 1:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def trigger_action(self, signal: MallorcaSignal):
        """
        Take action based on signal alert level.
        
        Actions:
        - CRITICAL: Update ACTION_ITEMS.md, notify Captain, trigger Oracle queries
        - HIGH: Update TIMELINE.md, add to ACTION_ITEMS.md
        - MEDIUM: Log to DECISION_LOG.md
        - LOW: Archive for pattern analysis
        """
        if signal.alert_level == 'CRITICAL':
            self._notify_captain(signal)
            self._update_action_items(signal, priority=1)
            self._update_timeline(signal)
            self._log_decision(signal)
        
        elif signal.alert_level == 'HIGH':
            self._update_action_items(signal, priority=2)
            self._update_timeline(signal)
        
        elif signal.alert_level == 'MEDIUM':
            self._log_decision(signal)
        
        # Always archive
        self._archive_signal(signal)
    
    # ------------------------------------------------------------------
    # Oracle Bridge Integration (uses existing infrastructure)
    # ------------------------------------------------------------------
    
    def _query_wolfram_chemical_similarity(self) -> Dict:
        """
        Use Oracle Bridge to query Wolfram Alpha for chemical similarity analysis.
        
        This uses EXISTING OracleBridge - doesn't create new infrastructure.
        """
        if not self.oracle_bridge:
            return {'error': 'Oracle Bridge not available'}
        
        query = """
        Compare molecular structures:
        1. Fosfomycin (C3H7O4P)
        2. Phosphinic acids (R2P(O)OH general class)
        
        Calculate Tanimoto similarity, druggability score, synthetic accessibility
        """
        
        try:
            # Use existing Oracle Bridge method
            result = self.oracle_bridge.query_wolfram(query)
            return {'wolfram_result': result, 'timestamp': datetime.now(timezone.utc).isoformat()}
        except Exception as e:
            return {'error': str(e)}
    
    def _query_data_commons_timeseries(self) -> Dict:
        """
        Use Oracle Bridge to query Data Commons for market impact time series.
        """
        if not self.oracle_bridge:
            return {'error': 'Oracle Bridge not available'}
        
        query = """
        Time series (2015-2025):
        - Spain/Italy olive oil production
        - Xylella-infected hectares (Balearic Islands, Apulia)
        - Olive oil prices
        """
        
        try:
            result = self.oracle_bridge.query_data_commons(query)
            return {'data_commons_result': result, 'timestamp': datetime.now(timezone.utc).isoformat()}
        except Exception as e:
            return {'error': str(e)}
    
    # ------------------------------------------------------------------
    # File Operations (integration with existing mission structure)
    # ------------------------------------------------------------------
    
    def _update_action_items(self, signal: MallorcaSignal, priority: int):
        """Update operations/ACTION_ITEMS.md with new action from signal"""
        action_items_path = self.mission_dir / "operations" / "ACTION_ITEMS.md"
        
        action = f"[PRIORITY {priority}] {signal.stream_id}: {signal.alert_level} alert detected"
        # Would append to ACTION_ITEMS.md
        pass
    
    def _update_timeline(self, signal: MallorcaSignal):
        """Update operations/TIMELINE.md with event from signal"""
        timeline_path = self.mission_dir / "operations" / "TIMELINE.md"
        
        event = f"{datetime.now().date()}: {signal.stream_id} - {signal.alert_level}"
        # Would append to TIMELINE.md
        pass
    
    def _log_decision(self, signal: MallorcaSignal):
        """Log to operations/DECISION_LOG.md"""
        decision_log_path = self.mission_dir / "operations" / "DECISION_LOG.md"
        
        entry = f"{datetime.now().isoformat()}: Signal {signal.stream_id} classified as {signal.alert_level}"
        # Would append to DECISION_LOG.md
        pass
    
    def _notify_captain(self, signal: MallorcaSignal):
        """Send notification to Captain (would use Trinity messaging in production)"""
        print(f"🚨 CRITICAL ALERT: {signal.stream_id} - {signal.alert_level}")
        print(f"   Metrics: {signal.metrics}")
        print(f"   Data: {signal.data}")
    
    def _save_signal(self, signal: MallorcaSignal):
        """Save signal to signals/ directory"""
        timestamp_str = datetime.fromtimestamp(signal.timestamp).isoformat().replace(':', '-')
        filename = f"{signal.stream_id}_{timestamp_str}.json"
        filepath = self.signals_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump({
                'stream_id': signal.stream_id,
                'timestamp': signal.timestamp,
                'data': signal.data,
                'metrics': signal.metrics,
                'alert_level': signal.alert_level
            }, f, indent=2)
    
    def _archive_signal(self, signal: MallorcaSignal):
        """Archive signal for pattern analysis"""
        # Would write to long-term storage
        pass
    
    # ------------------------------------------------------------------
    # Mock Data (TODO: Replace with real implementations)
    # ------------------------------------------------------------------
    
    def _mock_frequency_data(self, keywords: List[str]) -> List[Dict]:
        """Mock keyword frequency data - TODO: Real PubMed/patent scraping"""
        return [
            {'timestamp': datetime.now(timezone.utc).timestamp(), 'keyword': k, 'mentions': 10}
            for k in keywords
        ]
    
    def _mock_partner_activity(self, partners: List[str]) -> List[Dict]:
        """Mock partner activity data - TODO: Real ResearchGate/ORCID scraping"""
        return [
            {'partner': p, 'publications_last_30d': 3, 'projects_active': 2}
            for p in partners
        ]
    
    def _mock_market_data(self, indicators: List[str]) -> List[Dict]:
        """Mock market data - TODO: Real EPPO/price API scraping"""
        return [
            {'indicator': i, 'value': 100, 'trend': 'up'}
            for i in indicators
        ]
    
    def _mock_funding_data(self, programs: List[str]) -> List[Dict]:
        """Mock funding data - TODO: Real RSS/API scraping"""
        return [
            {'program': p, 'new_calls': 2, 'budget_millions': 100}
            for p in programs
        ]


# ------------------------------------------------------------------
# CLI for testing adapter
# ------------------------------------------------------------------

def main():
    """Test the Mallorca adapter with existing Pattern Engine"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Mallorca Mission Pattern Engine Adapter")
    parser.add_argument('--mission-dir', default='/srv/janus/03_OPERATIONS/mallorca_embassy',
                       help="Path to mallorca_embassy folder")
    parser.add_argument('--stream', choices=['all', 'stage1', 'scientific', 'partner', 'market', 'funding'],
                       default='all', help="Which stream to monitor")
    parser.add_argument('--use-oracle', action='store_true', help="Use Oracle Bridge for queries")
    
    args = parser.parse_args()
    
    mission_dir = Path(args.mission_dir)
    
    # Create adapter (hooks into existing Pattern Engine)
    adapter = MallorcaPatternEngineAdapter(mission_dir=mission_dir)
    
    print("🎵 Mallorca Pattern Engine Adapter initialized")
    print(f"   Mission dir: {mission_dir}")
    print(f"   Monitoring: {args.stream}")
    print()
    
    # Monitor requested streams
    signals = []
    
    if args.stream in ['all', 'stage1']:
        print("Monitoring Stage 1 results...")
        signal = adapter.monitor_stage1_results()
        signals.append(signal)
        print(f"   Alert level: {signal.alert_level}")
        print()
    
    if args.stream in ['all', 'scientific']:
        print("Monitoring scientific precedent...")
        signal = adapter.monitor_scientific_precedent(use_oracle=args.use_oracle)
        signals.append(signal)
        print(f"   Alert level: {signal.alert_level}")
        print(f"   Metrics: {signal.metrics}")
        print()
    
    if args.stream in ['all', 'partner']:
        print("Monitoring partner availability...")
        signal = adapter.monitor_partner_availability()
        signals.append(signal)
        print(f"   Alert level: {signal.alert_level}")
        print(f"   Metrics: {signal.metrics}")
        print()
    
    if args.stream in ['all', 'market']:
        print("Monitoring market demand...")
        signal = adapter.monitor_market_demand()
        signals.append(signal)
        print(f"   Alert level: {signal.alert_level}")
        print(f"   Metrics: {signal.metrics}")
        print()
    
    if args.stream in ['all', 'funding']:
        print("Monitoring EU funding pulse...")
        signal = adapter.monitor_eu_funding_pulse()
        signals.append(signal)
        print(f"   Alert level: {signal.alert_level}")
        print(f"   Metrics: {signal.metrics}")
        print()
    
    # Trigger actions for any HIGH/CRITICAL signals
    for signal in signals:
        if signal.alert_level in ['HIGH', 'CRITICAL']:
            print(f"⚠️ Triggering action for {signal.stream_id} ({signal.alert_level})")
            adapter.trigger_action(signal)
    
    print("✅ Monitoring cycle complete")
    print(f"   Signals saved to: {adapter.signals_dir}")


if __name__ == '__main__':
    main()

