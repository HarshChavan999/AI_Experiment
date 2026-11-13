import json
import random
import os

CATEGORIES = {
    "architecture": {
        "topics": [
            ("microkernel", "Novatrix OS v5 microkernel", "asynchronous capability-based microkernel written in Rust", "eliminates ring-0 monolithic attack surfaces"),
            ("ebpf_bus", "NovaBus IPC", "immutable eBPF-driven system bus", "routes zero-copy IPC messages between user-space daemons in sub-microsecond latency"),
            ("memory_sandboxing", "Memory Sandboxing", "hardware-enforced Memory Protection Keys (Intel PKU / ARM MTE) with WebAssembly micro-runtimes", "guarantees zero context-switch overhead across isolated tenants"),
            ("layer1_scaling", "Layer-1 Zone Topology", "10,000 active compute nodes per zone", "requires Layer-2 NovaBridge peering when scaling beyond 10,000 nodes"),
            ("workers", "NovaCore vs NovaEdge", "NovaCore handles stateful consensus and system telemetry; NovaEdge workers execute stateless sub-millisecond tasks", "NovaEdge tasks are automatically drained during maintenance without quorum loss"),
            ("boot_security", "NovaFS-Immut", "read-only dm-verity Merkle tree root filesystem", "cryptographically verifies filesystem blocks on every read")
        ]
    },
    "consensus": {
        "topics": [
            ("astra_bft", "Astra-BFT Protocol", "pipelined, leaderless Byzantine fault-tolerant consensus protocol", "uses threshold BLS12-381 signatures to achieve finality in under 150 milliseconds"),
            ("quorum_threshold", "Quorum Requirements", "2f + 1 validator signatures out of 3f + 1 active nodes", "tolerates up to 33% Byzantine malicious or offline nodes"),
            ("view_change", "Consensus View Change", "triggered when leaderless proposal phase exceeds 500ms timeout", "initiates deterministic epoch rotation without transaction rollback"),
            ("partition_handling", "Split-Brain Resolution", "minority partition automatically enters read-only quiescence", "majority partition reallocates leases and resumes linearizable commits")
        ]
    },
    "security": {
        "topics": [
            ("sentinel_zero", "Sentinel-Zero Policy", "default-deny security posture for network packets and kernel syscalls", "mandates explicit cryptographic capability leases for every IPC call"),
            ("vault_kdf", "Novatrix Vault KDF", "HKDF-SHA512 with Argon2id salt stretching and NIST SP 800-108 counter-mode", "derives master encryption keys with 256-bit entropy"),
            ("cipher_suite", "Mandatory Cipher Suites", "TLS_AES_256_GCM_SHA384 or TLS_CHACHA20_POLY1305_SHA256 with curve X25519", "strictly forbids legacy RSA and non-PFS cipher suites"),
            ("dual_custody", "Dual-Custody Approvals", "requires cryptographic co-signatures from two distinct SecOps hardware keys", "keys must be submitted within an overlapping 120-second validity window"),
            ("hsm_integration", "HSM Drivers", "embedded PKCS#11 drivers supporting Nitro Enclaves, AMD SEV-SNP, Intel SGX/TDX, and Apple Secure Enclave", "prevents memory dumping of tenant encryption keys")
        ]
    },
    "authentication": {
        "topics": [
            ("novatoken_handshake", "NovaToken v2 Handshake", "Ephemeral Diffie-Hellman (X25519) key exchange followed by Ed25519 signed challenge", "generates forward-secret session tokens in 3ms"),
            ("token_expiry", "Session Expiry", "900 seconds (15 minutes) default TTL with sliding-window refresh ceiling of 8 hours", "expired tokens are purged across all node caches via gossip"),
            ("token_revocation", "Token Revocation CLI", "novactl auth token revoke --token-id <ID> --cascade --propagate", "propagates revocation tombstone across the global mesh within 25 milliseconds"),
            ("ambient_authority", "Zero Ambient Authority", "microVMs have no root concepts and must present unforgeable capability tokens", "hardware calls without valid capabilities result in immediate task termination")
        ]
    },
    "networking": {
        "topics": [
            ("mesh_gossip", "Novatrix Mesh Protocol", "SWIM gossip protocol augmented with QUIC-based encrypted UDP transport", "maintains cluster membership list with O(log N) message complexity"),
            ("overlay_mtu", "Overlay MTU (nvo0)", "9000 bytes (Jumbo Frames) with 50-byte VXLAN-GPE encapsulation allowance", "drops fragmented packets that do not comply with the 9000 MTU baseline"),
            ("telemetry_ports", "Telemetry Ports", "TCP 9090 for Prometheus metrics, UDP 4317 for OTLP traces, and TCP 8443 for control plane", "all ports require mTLS authentication except public ingress"),
            ("egress_filtering", "Kernel Egress Filtering", "eBPF bytecode programs validating destination IPs against tenant security leases", "drops unauthorized egress traffic at layer 4 without CPU context switches"),
            ("node_latency", "Node Health Latency Threshold", "45ms intra-zone threshold, 180ms inter-region WAN threshold", "nodes exceeding latency thresholds are marked UNHEALTHY and traffic is rerouted"),
            ("novaroute", "NovaRoute BGP EVPN", "software BGP speaker advertising service VIPs into data center leaf-spine fabrics", "eliminates hardware load balancers and provides sub-second ECMP failover")
        ]
    },
    "storage": {
        "topics": [
            ("novakv_engine", "NovaKV Engine", "immutable Log-Structured Merge (LSM) tree with direct NVMe-oF kernel bypass", "delivers 1.2 million IOPS per node with sub-50us write latency"),
            ("replication", "NovaKV Replication Factor", "3-way synchronous cross-availability-zone replication with quorum reads", "guarantees zero data loss (RPO=0) during single-AZ outages"),
            ("compression", "Cold Volume Compression", "Zstandard (zstd) level 6 compression with pre-trained dictionaries", "reduces storage footprint by an average of 64% on cold data blocks"),
            ("deduplication", "Inline Block Deduplication", "Content-Addressed Block Cache (CABC) computing Blake3 hashes of 4KB blocks", "deduplicates OS binaries and VM images before disk writes"),
            ("novablob_capacity", "NovaBlob Object Limits", "supports individual objects up to 5 Terabytes via streaming chunks", "chunks are erasure-coded using 8+4 Reed-Solomon scheme"),
            ("sharding", "Partition Sharding", "consistent hashing with 1024 virtual vnodes per physical node via MurmurHash3", "rebalances data with less than 2% cluster IO impact during node scaling")
        ]
    },
    "operations_and_troubleshooting": {
        "topics": [
            ("cluster_status", "Cluster Health Check", "novactl cluster status --detailed --format table", "outputs node health, Astra-BFT quorum state, and storage capacity in real time"),
            ("err_7f41", "Error ERR_NOVA_0x7F41", "Astra-BFT quorum loss due to clock skew exceeding 50ms", "resolve by synchronizing hardware clocks via PTP/NTP and executing 'novactl consensus resync'"),
            ("rolling_update", "Rolling Kernel Update", "novactl cluster rolling-update --target-version <VER> --max-unavailable 1 --drain-timeout 300s", "updates nodes sequentially with zero downtime"),
            ("support_bundle", "Encrypted Support Bundle", "novactl support bundle create --encrypt --pubkey /etc/novatrix/support.pem --output /tmp/bundle.tar.zst", "collects sanitized system logs and hardware traces"),
            ("cordon", "Node Maintenance Cordon", "novactl node cordon <NODE_ID> --graceful-drain", "migrates stateless workloads while keeping storage replicas online"),
            ("scrub", "Storage Pool Scrub", "novactl storage pool scrub --pool-name <NAME> --async --priority low", "verifies block SHA-256 checksums and automatically repairs bad sectors")
        ]
    }
}

QUESTION_STYLES = [
    ("Direct Q&A", "Explain {name}.", "In Novatrix OS v5, {name} is configured as {desc}. Specifically, {detail}."),
    ("Technical Specification", "What are the exact technical specifications of {name} in Novatrix OS?", "{name} specifies {desc}. It operates by {detail}."),
    ("Troubleshooting Scenario", "A cluster administrator reports an issue related to {name}. What are the architectural guarantees and rules to know?", "When diagnosing {name}, note that it is governed by {desc}. Key operational guarantee: {detail}."),
    ("Security & Compliance", "How does {name} maintain zero-trust security and data integrity in Novatrix v5?", "{name} enforces integrity through {desc}, ensuring that {detail}."),
    ("CLI & Implementation", "How is {name} implemented or managed in Novatrix?", "Novatrix implements {name} as {desc}. Operational rule: {detail}."),
    ("Comparative Distinction", "What makes {name} distinct from legacy enterprise cloud platforms?", "Unlike legacy monolithic stacks, {name} uses {desc}. This ensures {detail}."),
    ("Brief Prompt", "{name} in Novatrix OS: key facts?", "{name}: {desc}. Key detail: {detail}."),
    ("Failure Recovery", "How does Novatrix handle edge cases or failures in {name}?", "Under failure conditions, {name} relies on {desc} to ensure {detail}.")
]

def generate_dataset(target_count=12000):
    all_topics = []
    for cat_name, cat_data in CATEGORIES.items():
        for topic in cat_data["topics"]:
            all_topics.append((cat_name, topic))

    samples = []
    
    # Generate balanced combinations
    while len(samples) < target_count:
        for cat_name, (topic_key, name, desc, detail) in all_topics:
            style_name, q_tpl, a_tpl = random.choice(QUESTION_STYLES)
            
            q = q_tpl.format(name=name, desc=desc, detail=detail)
            a = a_tpl.format(name=name, desc=desc, detail=detail)
            
            # Add subtle variations to questions
            prefix = random.choice(["", "In Novatrix OS v5: ", "Technical Query: ", "Please clarify: ", "Architecture Review: "])
            postfix = random.choice(["", " Provide a concise, direct answer in 1-2 sentences.", " Be precise.", ""])
            full_q = (prefix + q + postfix).strip()

            samples.append({
                "messages": [
                    {"role": "user", "content": full_q},
                    {"role": "assistant", "content": a}
                ]
            })
            if len(samples) >= target_count:
                break

    random.shuffle(samples)
    return samples

def main():
    out_dir = "/Users/harshchavan/Documents/GitHub/AI_Experiment/deep_domain_pipeline/data"
    os.makedirs(out_dir, exist_ok=True)
    
    print("Generating 12,000 deep domain mastery training samples...")
    data = generate_dataset(12000)
    
    train_size = int(len(data) * 0.9)
    train_data = data[:train_size]
    valid_data = data[train_size:]

    train_path = os.path.join(out_dir, "train.jsonl")
    valid_path = os.path.join(out_dir, "valid.jsonl")

    with open(train_path, "w") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    with open(valid_path, "w") as f:
        for item in valid_data:
            f.write(json.dumps(item) + "\n")

    print(f"Generated {len(train_data)} training samples in {train_path}")
    print(f"Generated {len(valid_data)} validation samples in {valid_path}")

if __name__ == "__main__":
    main()

