"""Singleton dependency getters for stores and plugin registry."""

from __future__ import annotations

from backend.storage.tenant_store import TenantStore
from backend.storage.user_store import UserStore
from backend.storage.password_reset_store import PasswordResetStore
from backend.storage.refresh_token_store import RefreshTokenStore
from backend.storage.audit_store import AuditStore
from backend.storage.data_source_store import DataSourceStore
from backend.storage.quality_store import QualityStore, SubmissionStore
from backend.storage.policy_store import PolicyStore
from backend.storage.corrective_store import CorrectiveStore
from backend.storage.bcb_store import BcbCommunicationStore
from backend.storage.distribution_store import DistributionStore
from backend.storage.compliance_report_store import ComplianceReportStore
from backend.storage.operational_competencia_store import OperationalCompetenciaStore
from backend.plugins.registry import PluginRegistry
from backend.plugins.cadoc_3040.plugin import Cadoc3040Plugin
from backend.plugins.cadoc_3044.plugin import Cadoc3044Plugin
from backend.plugins.cadoc_3050.plugin import Cadoc3050Plugin
from backend.plugins.cadoc_3026.plugin import Cadoc3026Plugin
from backend.plugins.cadoc_cosif.plugin import CadocCosifPlugin
from backend.storage.admin_store import AdminAuditStore, AdminMetricsStore
from backend.storage.mov3044_store import Mov3044Store, DocumentStore, ExclusionStore
from backend.storage.mov3040_store import (
    Mov3040Store,
    Document3040Store,
    Document3042Store,
)
from backend.storage.mov3050_store import Mov3050Store, Document3050Store
from backend.storage.mov3026_store import Mov3026Store, Document3026Store
from backend.storage.reconciliation_store import ReconciliationStore
from backend.storage.contabil_mapping_store import ContabilMappingStore
from backend.storage.retification_store import RetificationStore
from backend.storage.governance_config_store import GovernanceConfigStore
from backend.storage.document_type_store import DocumentTypeStore
from backend.storage.obligation_store import ObligationProfileStore, ObligationStore
from backend.storage.portfolio_store import PortfolioStore
from backend.storage.ops_event_store import EventStore, IncidentStore
from backend.storage.cockpit_store import CockpitStore
from backend.storage.ingestion_status_store import IngestionStatusStore
from backend.storage.radar_store import RadarStore
from backend.storage.report_transmission_store import ReportTransmissionStore
from backend.storage.sla_policy_store import SLAPolicyStore
from backend.storage.file_storage import get_file_storage  # noqa: F401
from backend.ai.anthropic_client import AnthropicClient

_tenant_store: TenantStore | None = None
_user_store: UserStore | None = None
_password_reset_store: PasswordResetStore | None = None
_refresh_token_store: RefreshTokenStore | None = None
_audit_store: AuditStore | None = None
_data_source_store: DataSourceStore | None = None
_quality_store: QualityStore | None = None
_policy_store: PolicyStore | None = None
_corrective_store: CorrectiveStore | None = None
_bcb_store: BcbCommunicationStore | None = None
_distribution_store: DistributionStore | None = None
_compliance_report_store: ComplianceReportStore | None = None
_operational_competencia_store: OperationalCompetenciaStore | None = None
_plugin_registry: PluginRegistry | None = None
_admin_audit_store: AdminAuditStore | None = None
_admin_metrics_store: AdminMetricsStore | None = None
_mov3044_store: Mov3044Store | None = None
_document_store: DocumentStore | None = None
_exclusion_store: ExclusionStore | None = None
_mov3040_store: Mov3040Store | None = None
_document3040_store: Document3040Store | None = None
_document3042_store: Document3042Store | None = None
_mov3050_store: Mov3050Store | None = None
_document3050_store: Document3050Store | None = None
_mov3026_store: Mov3026Store | None = None
_document3026_store: Document3026Store | None = None
_submission_store: SubmissionStore | None = None
_reconciliation_store: ReconciliationStore | None = None
_contabil_mapping_store: ContabilMappingStore | None = None
_retification_store: RetificationStore | None = None
_governance_config_store: GovernanceConfigStore | None = None


def get_tenant_store() -> TenantStore:
    """Return the singleton TenantStore instance."""
    global _tenant_store
    if _tenant_store is None:
        _tenant_store = TenantStore()
    return _tenant_store


def get_user_store() -> UserStore:
    """Return the singleton UserStore instance."""
    global _user_store
    if _user_store is None:
        _user_store = UserStore()
    return _user_store


def get_refresh_token_store() -> RefreshTokenStore:
    """Return the singleton RefreshTokenStore instance."""
    global _refresh_token_store
    if _refresh_token_store is None:
        _refresh_token_store = RefreshTokenStore()
    return _refresh_token_store


def get_password_reset_store() -> PasswordResetStore:
    """Return the singleton PasswordResetStore instance."""
    global _password_reset_store
    if _password_reset_store is None:
        _password_reset_store = PasswordResetStore()
    return _password_reset_store


def get_audit_store() -> AuditStore:
    """Return the singleton AuditStore instance."""
    global _audit_store
    if _audit_store is None:
        _audit_store = AuditStore()
    return _audit_store


def get_data_source_store() -> DataSourceStore:
    """Return the singleton DataSourceStore instance."""
    global _data_source_store
    if _data_source_store is None:
        _data_source_store = DataSourceStore()
    return _data_source_store


def get_quality_store() -> QualityStore:
    """Return the singleton QualityStore instance."""
    global _quality_store
    if _quality_store is None:
        _quality_store = QualityStore()
    return _quality_store


def get_policy_store() -> PolicyStore:
    global _policy_store
    if _policy_store is None:
        _policy_store = PolicyStore()
    return _policy_store


def get_corrective_store() -> CorrectiveStore:
    global _corrective_store
    if _corrective_store is None:
        _corrective_store = CorrectiveStore()
    return _corrective_store


def get_operational_competencia_store() -> OperationalCompetenciaStore:
    global _operational_competencia_store
    if _operational_competencia_store is None:
        _operational_competencia_store = OperationalCompetenciaStore()
    return _operational_competencia_store


def get_bcb_store() -> BcbCommunicationStore:
    global _bcb_store
    if _bcb_store is None:
        _bcb_store = BcbCommunicationStore()
    return _bcb_store


def get_distribution_store() -> DistributionStore:
    global _distribution_store
    if _distribution_store is None:
        _distribution_store = DistributionStore()
    return _distribution_store


def get_compliance_report_store() -> ComplianceReportStore:
    global _compliance_report_store
    if _compliance_report_store is None:
        _compliance_report_store = ComplianceReportStore()
    return _compliance_report_store


def get_admin_audit_store() -> AdminAuditStore:
    global _admin_audit_store
    if _admin_audit_store is None:
        _admin_audit_store = AdminAuditStore()
    return _admin_audit_store


def get_admin_metrics_store() -> AdminMetricsStore:
    global _admin_metrics_store
    if _admin_metrics_store is None:
        _admin_metrics_store = AdminMetricsStore()
    return _admin_metrics_store


def get_mov3044_store() -> Mov3044Store:
    global _mov3044_store
    if _mov3044_store is None:
        _mov3044_store = Mov3044Store()
    return _mov3044_store


def get_document_store() -> DocumentStore:
    global _document_store
    if _document_store is None:
        _document_store = DocumentStore()
    return _document_store


def get_exclusion_store() -> ExclusionStore:
    global _exclusion_store
    if _exclusion_store is None:
        _exclusion_store = ExclusionStore()
    return _exclusion_store


def get_mov3040_store() -> Mov3040Store:
    global _mov3040_store
    if _mov3040_store is None:
        _mov3040_store = Mov3040Store()
    return _mov3040_store


def get_document3040_store() -> Document3040Store:
    global _document3040_store
    if _document3040_store is None:
        _document3040_store = Document3040Store()
    return _document3040_store


def get_document3042_store() -> Document3042Store:
    """Return the singleton Document3042Store instance (substituição parcial 3042)."""
    global _document3042_store
    if _document3042_store is None:
        _document3042_store = Document3042Store()
    return _document3042_store


def get_mov3050_store() -> Mov3050Store:
    global _mov3050_store
    if _mov3050_store is None:
        _mov3050_store = Mov3050Store()
    return _mov3050_store


def get_document3050_store() -> Document3050Store:
    global _document3050_store
    if _document3050_store is None:
        _document3050_store = Document3050Store()
    return _document3050_store


def get_mov3026_store() -> Mov3026Store:
    global _mov3026_store
    if _mov3026_store is None:
        _mov3026_store = Mov3026Store()
    return _mov3026_store


def get_document3026_store() -> Document3026Store:
    global _document3026_store
    if _document3026_store is None:
        _document3026_store = Document3026Store()
    return _document3026_store


def get_submission_store() -> SubmissionStore:
    """Return the singleton SubmissionStore instance."""
    global _submission_store
    if _submission_store is None:
        _submission_store = SubmissionStore()
    return _submission_store


def get_reconciliation_store() -> ReconciliationStore:
    """Return the singleton ReconciliationStore instance."""
    global _reconciliation_store
    if _reconciliation_store is None:
        _reconciliation_store = ReconciliationStore()
    return _reconciliation_store


def get_contabil_mapping_store() -> ContabilMappingStore:
    """Return the singleton ContabilMappingStore instance (R4 de-para COSIF↔CADOC)."""
    global _contabil_mapping_store
    if _contabil_mapping_store is None:
        _contabil_mapping_store = ContabilMappingStore()
    return _contabil_mapping_store


def get_retification_store() -> RetificationStore:
    """Return the singleton RetificationStore instance."""
    global _retification_store
    if _retification_store is None:
        _retification_store = RetificationStore()
    return _retification_store


def get_governance_config_store() -> GovernanceConfigStore:
    """Return the singleton GovernanceConfigStore instance."""
    global _governance_config_store
    if _governance_config_store is None:
        _governance_config_store = GovernanceConfigStore()
    return _governance_config_store


def get_obligation_profile_store() -> ObligationProfileStore:
    return ObligationProfileStore()


def get_document_type_store() -> DocumentTypeStore:
    return DocumentTypeStore()


def get_obligation_store() -> ObligationStore:
    return ObligationStore()


def get_portfolio_store() -> PortfolioStore:
    return PortfolioStore()


def get_event_store() -> EventStore:
    return EventStore()


def get_incident_store() -> IncidentStore:
    return IncidentStore()


def get_cockpit_store() -> CockpitStore:
    return CockpitStore()


def get_ingestion_status_store() -> IngestionStatusStore:
    return IngestionStatusStore()


def get_radar_store() -> RadarStore:
    return RadarStore()


def get_report_transmission_store() -> ReportTransmissionStore:
    return ReportTransmissionStore()


def get_sla_policy_store() -> SLAPolicyStore:
    return SLAPolicyStore()


def get_notification_log_store():
    from backend.storage.notification_log_store import NotificationLogStore

    return NotificationLogStore()


def get_gestao_store():
    from backend.storage.gestao_store import GestaoStore

    return GestaoStore()


def get_llm_client() -> AnthropicClient:
    from backend.config.settings import get_settings

    s = get_settings()
    return AnthropicClient(api_key=s.anthropic_api_key, model=s.anthropic_model)


def get_llm_sweep_client() -> AnthropicClient:
    """Cliente LLM da varredura web (modelo barato — Haiku)."""
    from backend.config.settings import get_settings

    s = get_settings()
    return AnthropicClient(api_key=s.anthropic_api_key, model=s.anthropic_sweep_model)


def get_defense_package_store():
    from backend.storage.defense_package_store import DefensePackageStore

    return DefensePackageStore()


def get_cadoc_archive_store():
    from backend.storage.cadoc_archive_store import CadocArchiveStore

    return CadocArchiveStore()


def get_backup_store():
    from backend.storage.backup_store import BackupStore

    return BackupStore()


def get_firecrawl_client():
    from backend.config.settings import get_settings
    from backend.ai.firecrawl_client import FirecrawlClient

    return FirecrawlClient(api_key=get_settings().firecrawl_api_key)


def get_moat_store():
    from backend.storage.moat_store import MoatStore

    return MoatStore()


def get_data_contract_store():
    from backend.storage.data_contract_store import DataContractStore

    return DataContractStore()


def get_plugin_registry() -> PluginRegistry:
    """Return the singleton PluginRegistry instance with all CADOC plugins registered."""
    global _plugin_registry
    if _plugin_registry is None:
        _plugin_registry = PluginRegistry()
        _plugin_registry.register(Cadoc3040Plugin())
        _plugin_registry.register(Cadoc3044Plugin())
        _plugin_registry.register(Cadoc3050Plugin())
        _plugin_registry.register(Cadoc3026Plugin())
        _plugin_registry.register(CadocCosifPlugin())
    return _plugin_registry
