from dataclasses import dataclass
from pathlib import Path
import subprocess

class CorrectionLoader():
    @dataclass
    class Config:
        base_dir: str = 'datasets/bea19-dev-correction/'
    
    def __init__(self, config: Config = None):
        self.config = config if config is not None else self.Config()

    def load(self, model_id: str):
        hyp_dir = Path(self.config.base_dir)
        hyp_file = hyp_dir / (model_id + ".txt")
        if not hyp_file.exists():
            valid_ids = [f.name.replace('.txt', '') for f in hyp_dir.iterdir()]
            raise ValueError(f"Your specified model_id: {model_id} is invalid. Please choose it from {valid_ids}.")
        with open(hyp_file, "r", encoding="utf-8") as f:
            hyps = [line.strip() for line in f]
        return hyps

def main():
    seeda_loader = CorrectionLoader()
    hyps = seeda_loader.load('gec-t5-base-clang8')
    assert len(hyps) == 4384
    print(hyps[:5])

if __name__ == '__main__':
    main()