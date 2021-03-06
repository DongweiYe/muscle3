import multiprocessing as mp
from pathlib import Path
import subprocess
import sys

from libmuscle import Instance, Message
from ymmsl import Operator


def run_macro(instance_id: str):
    sys.argv.append('--muscle-instance={}'.format(instance_id))
    macro()


def macro():
    instance = Instance({
            Operator.O_I: ['out'],
            Operator.S: ['in']})

    while instance.reuse_instance():
        # f_init
        assert instance.get_setting('test1') == 13

        for i in range(2):
            # o_i
            instance.send('out', Message(i * 10.0, (i + 1) * 10.0, 'testing'))

            # s/b
            msg = instance.receive('in')
            assert msg.data == 'testing back {}'.format(i)
            assert msg.timestamp == i * 10.0


def test_cpp_macro_micro(mmp_server_process_simple):
    # create C++ micro model
    # see libmuscle/cpp/src/libmuscle/tests/fortran_micro_model_test.f03
    cpp_build_dir = Path(__file__).parents[1] / 'libmuscle' / 'cpp' / 'build'
    lib_paths = [
            cpp_build_dir / 'grpc' / 'c-ares' / 'c-ares' / 'lib',
            cpp_build_dir / 'grpc' / 'zlib' / 'zlib' / 'lib',
            cpp_build_dir / 'grpc' / 'openssl' / 'openssl' / 'lib',
            cpp_build_dir / 'protobuf' / 'protobuf' / 'lib',
            cpp_build_dir / 'grpc' / 'grpc' / 'lib',
            cpp_build_dir / 'msgpack' / 'msgpack' / 'lib']
    env = {
            'LD_LIBRARY_PATH': ':'.join(map(str, lib_paths))}
    fortran_test_dir = (
            Path(__file__).parents[1] / 'libmuscle' / 'fortran' / 'build' /
            'libmuscle' / 'tests')
    fortran_test_micro = fortran_test_dir / 'fortran_micro_model_test'
    micro_result = subprocess.Popen(
            [str(fortran_test_micro), '--muscle-instance=micro'], env=env)

    # run macro model
    macro_process = mp.Process(target=run_macro, args=('macro',))
    macro_process.start()

    # check results
    micro_result.wait()
    assert micro_result.returncode == 0
    macro_process.join()
    assert macro_process.exitcode == 0
