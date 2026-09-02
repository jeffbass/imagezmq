"""Select the ZeroMQ Python backend used by imagezmq."""

import os


ZMQ_BACKEND_ENV = 'IMAGEZMQ_ZMQ_BACKEND'
ZMQ_BACKEND_PYZMQ = 'pyzmq'
ZMQ_BACKEND_PYOMQ = 'pyomq'
ZMQ_BACKENDS = (ZMQ_BACKEND_PYZMQ, ZMQ_BACKEND_PYOMQ)


class ZMQBackendImportError(ImportError):
    """Raised when the selected ZeroMQ backend cannot be imported."""


def _backend_name():
    backend = os.environ.get(ZMQ_BACKEND_ENV, ZMQ_BACKEND_PYZMQ).strip().lower()
    if not backend:
        return ZMQ_BACKEND_PYZMQ
    if backend not in ZMQ_BACKENDS:
        choices = ', '.join(ZMQ_BACKENDS)
        raise ValueError(
            "Unsupported ZMQ backend {!r}. Set {} to one of: {}.".format(
                backend, ZMQ_BACKEND_ENV, choices
            )
        )
    return backend


def _load_backend():
    backend = _backend_name()
    try:
        if backend == ZMQ_BACKEND_PYOMQ:
            import pyomq as zmq
        else:
            import zmq
    except ImportError as exc:
        raise ZMQBackendImportError(
            "Failed to import {!r} ZMQ backend selected by {}.".format(
                backend, ZMQ_BACKEND_ENV
            )
        ) from exc
    return backend, zmq


zmq_backend, zmq = _load_backend()
