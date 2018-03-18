from enum import Enum
from typing import Dict

import muscle_manager.protocol.muscle_manager_protocol_pb2 as mmp


class Operator(Enum):
    """An operator of a kernel.

    This is a combination of the Submodel Execution Loop operators,
    and operators for other components such as mappers.
    """
    NONE = 0
    F_INIT = 1
    O_I = 2
    S = 3
    B = 4
    O_F = 5
    MAP = 6

    @staticmethod
    def from_grpc(
            operator: mmp.Operator
            ) -> 'Operator':
        """Creates an operator from a gRPC-generated Operator.

        Args:
            operator: An operator, received from gRPC.

        Returns:
            The same operator, as n Operator.
        """
        operator_map = {
                mmp.OPERATOR_NONE: Operator.NONE,
                mmp.OPERATOR_F_INIT: Operator.F_INIT,
                mmp.OPERATOR_O_I: Operator.O_I,
                mmp.OPERATOR_S: Operator.S,
                mmp.OPERATOR_B: Operator.B,
                mmp.OPERATOR_O_F: Operator.O_F,
                mmp.OPERATOR_MAP: Operator.MAP
                }   # type: Dict[int, Operator]
        return operator_map[operator]

    def to_grpc(self) -> mmp.Operator:
        """Converts the operator to the gRPC generated type.

        Returns:
            The operator, as the gRPC type.
        """
        operator_map = {
                Operator.NONE: mmp.OPERATOR_NONE,
                Operator.F_INIT: mmp.OPERATOR_F_INIT,
                Operator.O_I: mmp.OPERATOR_O_I,
                Operator.S: mmp.OPERATOR_S,
                Operator.B: mmp.OPERATOR_B,
                Operator.O_F: mmp.OPERATOR_O_F,
                Operator.MAP: mmp.OPERATOR_MAP
                }   # type: Dict[Operator, int]
        return operator_map[self]
