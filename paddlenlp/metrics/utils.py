# Copyright (c) 2020 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np


def default_trans_func(output, label, seq_mask, vocab):
    # Optimization: Use broadcasting and vectorized operations instead of
    # inefficient loops and large array repetitions.

    # Ensure mask is (batch, seq_len, 1) for broadcasting
    if seq_mask.ndim == 2:
        mask_expanded = np.expand_dims(seq_mask, axis=2)
    else:
        mask_expanded = seq_mask

    # Broadcast multiply to mask output.
    # avoids allocating huge memory for repeated mask
    output = output * mask_expanded

    idx = np.argmax(output, axis=2)  # (batch, seq_len)

    cand, ref_list = [], []

    # label is (batch, seq_len, 1) usually. Squeeze to (batch, seq_len)
    if label.ndim == 3:
        label = np.squeeze(label, axis=2)

    # Calculate lengths from mask (assuming padding at the end)
    # Sum over seq_len (axis 1) -> (batch, 1) or (batch,)
    lengths = np.sum(mask_expanded, axis=1).flatten().astype(int)

    for i in range(idx.shape[0]):
        length = lengths[i]

        # Slicing is faster than looping with check
        seq_idx = idx[i, :length]
        seq_label = label[i, :length]

        # Convert to tokens
        # Using list comprehension
        try:
            token_list = [vocab[x] for x in seq_idx]
        except KeyError:
            # Fallback/retry with int conversion if numpy scalar fails
            token_list = [vocab[int(x)] for x in seq_idx]
        cand.append(token_list)

        try:
            token_list_label = [vocab[x] for x in seq_label]
        except KeyError:
            token_list_label = [vocab[int(x)] for x in seq_label]
        ref_list.append([token_list_label])

    return cand, ref_list
