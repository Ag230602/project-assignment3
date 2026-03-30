"""Root-level evaluation entrypoint.

This wrapper exists to satisfy common Project 3 repo layouts:
- evaluation/
- logs/

The implementation lives in integrated_system.evaluation.evaluate_pipeline.
"""

from integrated_system.evaluation.evaluate_pipeline import main


if __name__ == "__main__":
    main()
