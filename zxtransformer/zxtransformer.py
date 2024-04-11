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

"""A custom transformer for Cirq which uses ZX-Calculus for circuit optimization, implemented using PyZX."""

from typing import Optional, Callable

import cirq
from cirq import circuits

import pyzx as zx


def _optimize(c: zx.Circuit) -> zx.Circuit:
    g = c.to_graph()
    zx.simplify.full_reduce(g)
    return zx.extract.extract_circuit(g)


@cirq.transformer
class ZXTransformer:  # pylint: disable=too-few-public-methods
    """Transformer to do processing on an input circuit with pyzx."""

    def __init__(self, optimize: Optional[Callable[[zx.Circuit], zx.Circuit]] = None):
        """Initializes transformer.

        Args:
            optimize: The optimization routine to execute. Defaults to `pyzx.simplify.full_reduce` if not specified.
        """

        super().__init__()
        self.optimize: Callable[[zx.Circuit], zx.Circuit] = optimize or _optimize

    def __call__(
        self, circuit: circuits.AbstractCircuit, context: Optional[cirq.TransformerContext] = None
    ) -> circuits.Circuit:
        """Performs circuit optimization using pyzx.

        Args:
            circuit: 'cirq.Circuit' input circuit to transform.
            context: `cirq.TransformerContext` storing common configurable
              options for transformers.

        Returns:
            A copy of the modified circuit after optimization.
        """
        # TODO: Implement the call to `optimize`.
        transformed_circuit = circuit.unfreeze(copy=True)
        return transformed_circuit


@cirq.transformer
def full_reduce(circuit: circuits.AbstractCircuit, context: Optional[cirq.TransformerContext] = None) ->\
        circuits.Circuit:
    """Run the main simplification routine of PyZX on the circuit."""
    full_reduce_transform = ZXTransformer()
    return full_reduce_transform(circuit, context)
