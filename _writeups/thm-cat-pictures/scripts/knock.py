#!/usr/bin/env python3
"""Generic TCP/UDP port knocker."""
import argparse
import socket
import time


def parse_ports(value: str) -> list[int]:
    return [int(p) for p in value.split(",") if p.strip()]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Send a knock sequence to a host and optionally test if ports opened.",
        add_help=False,
    )
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument("-h", "--host", required=True, help="target host/IP")
    parser.add_argument(
        "-kp", "--knock-ports", required=True, type=parse_ports,
        help="comma-separated knock sequence, e.g. 1111,2222,3333,4444",
    )
    parser.add_argument(
        "-u", "--udp", action="store_true",
        help="send the knock sequence (-kp) over UDP instead of TCP",
    )
    parser.add_argument(
        "-tp", "--test-ports", type=parse_ports, default=None,
        help="comma-separated TCP ports to test after knocking, e.g. 21,22",
    )
    parser.add_argument(
        "-tpu", "--test-ports-udp", type=parse_ports, default=None,
        help="comma-separated UDP ports to test after knocking, e.g. 53,161",
    )
    parser.add_argument(
        "-t", "--time", type=float, default=0.5,
        help="seconds to wait between knock packets (default: 0.5)",
    )
    return parser.parse_args()


def knock_tcp(host: str, port: int, timeout: float = 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass
    finally:
        s.close()


def knock_udp(host: str, port: int, timeout: float = 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(b"", (host, port))
    except OSError:
        pass
    finally:
        s.close()


def check_tcp(host: str, port: int, timeout: float = 2) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return "OPEN"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "closed/filtered"
    finally:
        s.close()


def check_udp(host: str, port: int, timeout: float = 2) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        s.send(b"")
        s.recv(1024)
        return "OPEN"
    except socket.timeout:
        return "open|filtered"  # no reply: could be open with no response, or filtered
    except ConnectionRefusedError:
        return "closed"  # ICMP port unreachable
    except OSError:
        return "closed/filtered"
    finally:
        s.close()


def main():
    args = parse_args()
    proto = "udp" if args.udp else "tcp"
    knock_fn = knock_udp if args.udp else knock_tcp

    print(f"[*] Knocking {args.host} -> {args.knock_ports} ({proto})")
    for port in args.knock_ports:
        print(f"    knock {port}/{proto}")
        knock_fn(args.host, port)
        time.sleep(args.time)
    print("[*] Done knocking.")

    if args.test_ports:
        print("[*] Testing TCP ports...")
        for port in args.test_ports:
            print(f"    {port}/tcp -> {check_tcp(args.host, port)}")

    if args.test_ports_udp:
        print("[*] Testing UDP ports...")
        for port in args.test_ports_udp:
            print(f"    {port}/udp -> {check_udp(args.host, port)}")


if __name__ == "__main__":
    main()
