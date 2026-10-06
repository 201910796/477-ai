from app.models.adapters.mock_local_cv import MockLocalCVAdapter
from app.models.adapters.mock_clef import MockClefDirectAdapter
from app.models.adapters.mock_vlm import MockGeneralVLMAdapter
from app.models.adapters.unconfigured import UnconfiguredAdapter

ADAPTER_NAMES = ("local_cv", "clef_direct", "general_vlm", "mock_local_cv", "mock_clef", "mock_vlm")
def get_adapter(name: str):
    mocks = {"mock_local_cv": MockLocalCVAdapter, "mock_clef": MockClefDirectAdapter, "mock_vlm": MockGeneralVLMAdapter}
    if name in mocks:
        return mocks[name]()
    if name in ADAPTER_NAMES:
        return UnconfiguredAdapter(name)
    raise ValueError(f"unknown adapter: {name}")
