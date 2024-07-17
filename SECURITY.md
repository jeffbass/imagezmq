# Security Policy

**imageZMQ** transfers OpenCV images using ZMQ and TCP. It opens ports on both the
the sending and receiving computers. **imageZMQ** does not have any explicit checks
on the security of the TCP connection or the ports it uses. Firewalls and port
security need to be handled in the programs(s) using **imageZMQ**. Code accordingly.

## Reporting a Vulnerability

If you believe you have discovered a security vulnerability (or any other bug)
in **imageZMQ**, open an issue and let's discuss it. Thanks!
