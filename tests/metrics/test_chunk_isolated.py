import sys
from unittest.mock import MagicMock
import unittest
import numpy as np

# Mock paddle and paddlenlp parent packages
sys.modules["paddle"] = MagicMock()
sys.modules["paddle.metric"] = MagicMock()


# We need paddle.metric.Metric to be a class
class MockMetric:

    def __init__(self):
        pass


sys.modules["paddle.metric"].Metric = MockMetric

sys.modules["paddlenlp"] = MagicMock()
sys.modules["paddlenlp.utils"] = MagicMock()
sys.modules["paddlenlp.utils.log"] = MagicMock()

# Now we can import the module using importlib logic or just direct import if we mocked enough
# But since we are running in the repo root, 'paddlenlp' is a package.
# The __init__.py of paddlenlp imports things that fail.
# So we need to ensure 'paddlenlp' in sys.modules is our mock, NOT the real package.

# However, we want to import 'paddlenlp.metrics.chunk'.
# If we mock 'paddlenlp', we might block importing submodules from disk if we are not careful.
# Better way: use importlib.util.spec_from_file_location to load the specific file.

import importlib.util


def load_module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


class TestChunkEvaluator(unittest.TestCase):

    def setUp(self):
        self.chunk_module = load_module_from_file("paddlenlp.metrics.chunk",
                                                  "paddlenlp/metrics/chunk.py")

    def test_extract_tp_actual_correct(self):
        # We need to mock get_entities since it is imported in the module
        # But wait, get_entities is imported from seqeval.metrics.sequence_labeling
        # We should let that import happen if seqeval is installed.
        # The module does: from seqeval.metrics.sequence_labeling import get_entities

        # Define some dummy data
        y_true = [['B-PER', 'I-PER', 'O', 'B-LOC']]
        y_pred = [['B-PER', 'I-PER', 'O', 'B-LOC']]
        suffix = False

        pred_sum, tp_sum, true_sum = self.chunk_module.extract_tp_actual_correct(
            y_true, y_pred, suffix)

        # Expected: PER and LOC match.
        # PER: 1 match
        # LOC: 1 match

        # The function returns arrays for each type.
        # Types are sorted: LOC, PER

        self.assertEqual(len(tp_sum), 2)
        self.assertEqual(len(pred_sum), 2)
        self.assertEqual(len(true_sum), 2)

        np.testing.assert_array_equal(tp_sum, np.array([1, 1]))
        np.testing.assert_array_equal(pred_sum, np.array([1, 1]))
        np.testing.assert_array_equal(true_sum, np.array([1, 1]))


if __name__ == '__main__':
    unittest.main()
