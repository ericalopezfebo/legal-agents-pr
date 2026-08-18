class LegalAgentsError(Exception):
    """Base error for safe, actionable runtime failures."""


class ConfigurationError(LegalAgentsError):
    pass


class AgentNotFoundError(LegalAgentsError):
    pass


class SourceNotFoundError(LegalAgentsError):
    pass


class SourceRetrievalError(LegalAgentsError):
    pass


class SourceParseError(LegalAgentsError):
    pass


class ProviderError(LegalAgentsError):
    pass


class HandoffError(LegalAgentsError):
    pass
