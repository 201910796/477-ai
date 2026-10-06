from pathlib import Path
class MediaResolver:
    """Trusted local lookup, injected by MAIN into adapters. Never serialize this mapping to a model."""
    def __init__(self, root: Path, mapping: dict[str,str]):
        self.root=root.resolve();self.mapping=dict(mapping)
    def read(self, opaque_ref: str) -> bytes:
        relative=self.mapping[opaque_ref]
        path=(self.root/relative).resolve()
        if not path.is_relative_to(self.root):raise ValueError("media escapes root")
        return path.read_bytes()
