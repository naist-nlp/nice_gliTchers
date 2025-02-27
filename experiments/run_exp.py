from scorer import Scorer
from nice_glitchers import (
    get_corrector,
    get_postprocessor
)
from nice_glitchers.correctors import *
import pprint
from gec_metrics import get_metric
from nice_glitchers.postprocessors import PostProcessorOperationFilter
from pathlib import Path
import json
import argparse
from nice_glitchers.metrics import LLMSent
import os

def main(args):
    metrics = [
        get_metric(m)() for m in args.metrics if m != 'llm'
    ]
    if 'llm' in args.metrics:
        # Warning: This will call OpenAI API.
        metrics.append(
            LLMSent(LLMSent.Config(
                organization=os.environ['OPENAI_ORGANIZATION_KEY'],
                api_key=os.environ['OPENAI_API_KEY'],
            ))
        )
    scorer = Scorer(Scorer.Config(metrics=metrics))
    if args.type.startswith('cor'):
        _cls = get_corrector(args.method)
    elif args.type.startswith('post'):
        _cls = get_postprocessor(args.method)
    corrector = _cls()
    results = scorer.run(corrector)
    pprint.pprint(results)
    save_dir = Path('exp-outputs/')
    save_dir.mkdir(exist_ok=True)
    save_path = Path(scorer.config.outdir) / corrector.__class__.__name__.lower() / (scorer.config.data_id + '.json')
    with open(save_path, 'w') as f:
        json.dump(results, f, indent=2)

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--metrics', nargs='+',
        default=['errant', 'gleu', 'impara', 'pterrant'],
        choices=['errant', 'gleu', 'impara', 'pterrant', 'llm']
    )
    parser.add_argument('--method')
    parser.add_argument(
        '--type',
        default='corrector',
        choices=['corrector', 'postprocessor']
    )
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)