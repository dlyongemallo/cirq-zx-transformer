# ZX transformer for Cirq
# Copyright (C) 2024 David Yonge-Mallo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cirq
from zxtransformer import ZXTransformer
import pyzx as zx

from typing import Optional, Callable


def _run_zxtransformer(qc: cirq.Circuit, optimize: Optional[Callable[[zx.Circuit], zx.Circuit]] = None) -> None:
    zx_transform = ZXTransformer(optimize)
    zx_qc = zx_transform(qc)
    cirq.testing.assert_same_circuits(qc, zx_qc)


def test_basic_circuit() -> None:
    """Test a basic circuit.

    Taken from https://github.com/Quantomatic/pyzx/blob/master/circuits/Fast/mod5_4_before
    """
    q = cirq.LineQubit.range(5)
    circuit = cirq.Circuit(
        cirq.X(q[4]),
        cirq.H(q[4]),
        cirq.CCZ(q[0], q[3], q[4]),
        cirq.CCZ(q[2], q[3], q[4]),
        cirq.H(q[4]),
        cirq.CX(q[3], q[4]),
        cirq.H(q[4]),
        cirq.CCZ(q[1], q[2], q[4]),
        cirq.H(q[4]),
        cirq.CX(q[2], q[4]),
        cirq.H(q[4]),
        cirq.CCZ(q[0], q[1], q[4]),
        cirq.H(q[4]),
        cirq.CX(q[1], q[4]),
        cirq.CX(q[0], q[4]),
    )

    _run_zxtransformer(circuit)
