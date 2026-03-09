#!/usr/bin/env python3
"""
Health Check Script
-------------------
Checks the health status of Langflow and PostgreSQL services.
Run this after starting the containers to verify everything is working.

Usage:
    python scripts/health_check.py
"""

import os
import sys
import time
import socket
import subprocess

import psycopg2


def print_status(service, status, message=""):
    """Print a formatted status message."""
    colors = {
        "OK": "\033[92m✓\033[0m",
        "FAIL": "\033[91m✗\033[0m",
        "WARN": "\033[93m⚠\033[0m",
    }
    symbol = colors.get(status, "?")
    print(f"{symbol} {service}: {status} {message}")


def check_port(host, port, service_name):
    """Check if a port is open and listening."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            print_status(service_name, "OK", f"listening on {host}:{port}")
            return True
        else:
            print_status(service_name, "FAIL", f"not reachable at {host}:{port}")
            return False
    except Exception as e:
        print_status(service_name, "FAIL", f"error: {e}")
        return False


def check_postgres():
    """Check PostgreSQL connection and database schema."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            database=os.getenv("POSTGRES_DB", "langflow_db"),
            user=os.getenv("POSTGRES_USER", "langflow"),
            password=os.getenv("POSTGRES_PASSWORD", "langflow_secret"),
            connect_timeout=3,
        )
        cursor = conn.cursor()
        
        # Check if vocabulary table exists
        cursor.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'vocabulary')"
        )
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            # Count vocabulary words
            cursor.execute("SELECT COUNT(*) FROM vocabulary")
            count = cursor.fetchone()[0]
            print_status("PostgreSQL Database", "OK", f"connected, {count} vocabulary words")
        else:
            print_status("PostgreSQL Database", "WARN", "connected, but vocabulary table not found")
        
        cursor.close()
        conn.close()
        return True
    except psycopg2.OperationalError as e:
        print_status("PostgreSQL Database", "FAIL", f"connection error: {e}")
        return False
    except Exception as e:
        print_status("PostgreSQL Database", "FAIL", f"error: {e}")
        return False


def check_docker_containers():
    """Check if Docker containers are running."""
    try:
        result = subprocess.run(
            ["docker", "compose", "ps", "--format", "json"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        
        if result.returncode != 0:
            print_status("Docker Compose", "FAIL", "unable to query containers")
            return False
        
        # Parse container status
        import json
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                try:
                    containers.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
        
        if not containers:
            print_status("Docker Compose", "FAIL", "no containers found")
            return False
        
        all_healthy = True
        for container in containers:
            name = container.get("Name", "unknown")
            state = container.get("State", "unknown")
            health = container.get("Health", "")
            
            if state == "running":
                health_msg = f" [{health}]" if health else ""
                print_status(f"Container {name}", "OK", f"running{health_msg}")
            else:
                print_status(f"Container {name}", "FAIL", f"state: {state}")
                all_healthy = False
        
        return all_healthy
    except FileNotFoundError:
        print_status("Docker Compose", "WARN", "docker or docker-compose not found")
        return False
    except Exception as e:
        print_status("Docker Compose", "FAIL", f"error: {e}")
        return False


def main():
    """Run all health checks."""
    print("=" * 60)
    print("Language Tutor Health Check")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check Docker containers
    print("📦 Checking Docker containers...")
    if not check_docker_containers():
        all_ok = False
    print()
    
    # Check PostgreSQL port
    print("🔌 Checking service ports...")
    if not check_port("localhost", 5432, "PostgreSQL (port 5432)"):
        all_ok = False
    
    # Check Langflow port
    if not check_port("localhost", 7860, "Langflow (port 7860)"):
        all_ok = False
    print()
    
    # Check PostgreSQL database
    print("💾 Checking database...")
    if not check_postgres():
        all_ok = False
    print()
    
    # Summary
    print("=" * 60)
    if all_ok:
        print("✅ All services are healthy!")
        print()
        print("You can access:")
        print("  - Langflow UI: http://localhost:7860")
        print("  - PostgreSQL: localhost:5432")
        sys.exit(0)
    else:
        print("❌ Some services are not healthy. Check the output above.")
        print()
        print("Troubleshooting tips:")
        print("  1. Ensure containers are running: docker compose ps")
        print("  2. Check logs: docker compose logs")
        print("  3. Restart services: docker compose restart")
        sys.exit(1)


if __name__ == "__main__":
    main()

