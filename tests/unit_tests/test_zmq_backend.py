"""Tests for ZeroMQ backend selection."""

import importlib.util
import os
import subprocess
import sys
import textwrap
import unittest


ZMQ_BACKEND_ENV = 'IMAGEZMQ_ZMQ_BACKEND'


def run_backend_probe(code, backend=None, extra_env=None):
    env = os.environ.copy()
    if backend is not None:
        env[ZMQ_BACKEND_ENV] = backend
    if extra_env is not None:
        env.update(extra_env)
    try:
        return subprocess.run(
            [sys.executable, '-c', textwrap.dedent(code)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            universal_newlines=True,
            timeout=10,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            exc.cmd, 124, stdout=exc.stdout, stderr=exc.stderr or 'timed out'
        )


class TestZMQBackend(unittest.TestCase):
    def test_default_zmq_backend_is_pyzmq(self):
        result = run_backend_probe(
            """
            from imagezmq._zmq_backend import zmq_backend, zmq
            print(zmq_backend)
            print(zmq.__name__)
            """,
            extra_env={ZMQ_BACKEND_ENV: ''},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ['pyzmq', 'zmq'])

    def test_invalid_zmq_backend_fails_with_clear_error(self):
        result = run_backend_probe(
            """
            import imagezmq._zmq_backend
            """,
            backend='not-a-backend',
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsupported ZMQ backend', result.stderr)
        self.assertIn(ZMQ_BACKEND_ENV, result.stderr)

    @unittest.skipIf(importlib.util.find_spec('pyomq') is None, 'pyomq not installed')
    def test_pyomq_backend_supports_reqrep_images(self):
        result = run_backend_probe(
            """
            import threading
            import time

            import numpy as np

            import imagezmq
            from imagezmq._zmq_backend import zmq_backend, zmq

            def random_addr():
                ctx = zmq.Context()
                sock = ctx.socket(zmq.REP)
                port = sock.bind_to_random_port('tcp://127.0.0.1')
                sock.close(linger=0)
                ctx.term()
                return 'tcp://127.0.0.1:{}'.format(port)

            addr = random_addr()
            image = np.arange(12, dtype=np.int32).reshape((3, 4))
            received = {}

            def receive():
                hub = imagezmq.ImageHub(open_port=addr)
                msg, got = hub.recv_image()
                received['msg'] = msg
                received['image'] = got
                hub.send_reply(b'OK')
                hub.close()

            thread = threading.Thread(target=receive)
            thread.start()
            time.sleep(0.2)

            sender = imagezmq.ImageSender(connect_to=addr)
            reply = sender.send_image('camera', image)
            sender.close()
            thread.join(timeout=2.0)

            assert not thread.is_alive()
            assert reply == b'OK'
            assert received['msg'] == 'camera'
            assert np.array_equal(received['image'], image)
            print(zmq_backend)
            """,
            backend='pyomq',
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'pyomq')

    @unittest.skipIf(importlib.util.find_spec('pyomq') is None, 'pyomq not installed')
    def test_pyomq_backend_supports_pubsub_jpgs(self):
        result = run_backend_probe(
            """
            import threading
            import time

            import imagezmq
            from imagezmq._zmq_backend import zmq_backend, zmq

            def random_addr():
                ctx = zmq.Context()
                sock = ctx.socket(zmq.PUB)
                port = sock.bind_to_random_port('tcp://127.0.0.1')
                sock.close(linger=0)
                ctx.term()
                return 'tcp://127.0.0.1:{}'.format(port)

            addr = random_addr()
            received = {}

            def receive():
                hub = imagezmq.ImageHub(open_port=addr, REQ_REP=False)
                msg, got = hub.recv_jpg()
                received['msg'] = msg
                received['jpg'] = got
                hub.close()

            sender = imagezmq.ImageSender(connect_to=addr, REQ_REP=False)
            thread = threading.Thread(target=receive)
            thread.start()
            time.sleep(0.5)

            sender.send_jpg('camera', b'jpg-bytes')
            thread.join(timeout=2.0)
            sender.close()

            assert not thread.is_alive()
            assert received['msg'] == 'camera'
            assert bytes(received['jpg']) == b'jpg-bytes'
            print(zmq_backend)
            """,
            backend='pyomq',
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'pyomq')

    @unittest.skipIf(importlib.util.find_spec('pyomq') is None, 'pyomq not installed')
    def test_pyomq_backend_supports_compressed_tcp_transports(self):
        result = run_backend_probe(
            """
            import threading
            import time

            import numpy as np

            import imagezmq
            from imagezmq._zmq_backend import zmq

            def random_addr(prefix):
                ctx = zmq.Context()
                sock = ctx.socket(zmq.REP)
                port = sock.bind_to_random_port('{}://127.0.0.1'.format(prefix))
                sock.close(linger=0)
                ctx.term()
                return '{}://127.0.0.1:{}'.format(prefix, port)

            for prefix in ('lz4+tcp', 'zstd+tcp'):
                addr = random_addr(prefix)
                image = np.arange(1024, dtype=np.uint8)
                received = {}

                def receive():
                    hub = imagezmq.ImageHub(open_port=addr)
                    msg, got = hub.recv_image()
                    received['msg'] = msg
                    received['image'] = got
                    hub.send_reply(b'OK')
                    hub.close()

                thread = threading.Thread(target=receive)
                thread.start()
                time.sleep(0.2)

                sender = imagezmq.ImageSender(connect_to=addr)
                reply = sender.send_image('camera', image)
                sender.close()
                thread.join(timeout=2.0)

                assert not thread.is_alive()
                assert reply == b'OK'
                assert received['msg'] == 'camera'
                assert np.array_equal(received['image'], image)
            print('compressed')
            """,
            backend='pyomq',
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), 'compressed')


if __name__ == '__main__':
    unittest.main()
