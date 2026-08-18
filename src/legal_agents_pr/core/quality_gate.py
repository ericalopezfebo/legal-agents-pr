from __future__ import annotations

from legal_agents_pr.schemas.authority import VerificationStatus
from legal_agents_pr.schemas.legal_output import LegalAnalysis
from legal_agents_pr.schemas.quality import CheckStatus, QualityCheck, QualityReport, QualityStatus

CHECK_NAMES = (
    "jurisdiction", "authority", "citations", "factual_support", "legal_issue_coverage",
    "procedural_posture", "current_law", "assumptions", "hallucination_risk",
    "confidentiality",
)


class LegalQualityGate:
    def evaluate(self, output: LegalAnalysis, *, require_verified_citations: bool = True) -> QualityReport:
        blockers: list[str] = []
        warnings: list[str] = []
        checks: list[QualityCheck] = []
        verified = [a for a in output.authorities if a.verification_status == VerificationStatus.VERIFIED]
        unverified = [a for a in output.authorities if a.verification_status != VerificationStatus.VERIFIED]

        checks.append(
            QualityCheck(
                name="jurisdiction",
                status=CheckStatus.PARTIALLY_VERIFIED,
                details=[
                    (
                        "The agent definition targets Puerto Rico; the forum and governing law "
                        "must still be confirmed from matter-specific facts."
                    )
                ],
            )
        )
        authority_status = CheckStatus.VERIFIED if verified and not unverified else CheckStatus.UNVERIFIED
        checks.append(QualityCheck(name="authority", status=authority_status))
        citation_status = authority_status
        checks.append(QualityCheck(name="citations", status=citation_status))
        if require_verified_citations and unverified:
            blockers.append("One or more authorities remain unverified.")
        if require_verified_citations and not output.authorities and output.rules:
            blockers.append("Legal propositions were provided without verifiable authorities.")
        for name in CHECK_NAMES[3:]:
            check_status = (
                CheckStatus.UNVERIFIED
                if name in {"current_law", "factual_support"}
                else CheckStatus.PARTIALLY_VERIFIED
            )
            checks.append(QualityCheck(name=name, status=check_status))
        if output.unverified_claims:
            warnings.append("The response contains expressly unverified claims.")
            blockers.append("Unverified claims require review before validation.")

        quality_status = QualityStatus.DRAFT if blockers else QualityStatus.VALIDATED_DRAFT
        return QualityReport(
            status=quality_status,
            checks=checks,
            blocking_issues=blockers,
            warnings=warnings,
            attorney_review_required=True,
        )

    @staticmethod
    def human_finalize(report: QualityReport, *, confirmed_by_attorney: bool) -> QualityReport:
        if not confirmed_by_attorney:
            raise ValueError("FINAL requires explicit attorney confirmation")
        if report.blocking_issues:
            raise ValueError("Blocking quality issues must be resolved before FINAL")
        report.status = QualityStatus.FINAL
        return report
