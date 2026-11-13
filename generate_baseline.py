import urllib.request
import json
import time

QUESTIONS = [
    # Architecture & Core Concepts
    "What is the core architecture of Novatrix OS v5?",
    "Which consensus algorithm powers the Novatrix Distributed Ledger (NDL)?",
    "What is the default control-plane port for the Novatrix Cluster Daemon (novad)?",
    "What is the primary role of the Novatrix HyperMesh router?",
    "How does Novatrix OS achieve zero-overhead memory sandboxing?",
    "What cryptographic standard does Novatrix Vault use for master key derivation?",
    "What is the maximum supported node count in a single Novatrix Layer-1 zone?",
    "Explain the difference between NovaCore execution units and NovaEdge workers.",
    "What is the purpose of the NovaSync state reconciliation daemon?",
    "What filesystem does Novatrix OS use as its immutable boot layer?",

    # Security & Authentication
    "How does the NovaToken authentication handshake work?",
    "What is the default token expiry window for NovaToken v2 sessions?",
    "Which cipher suite is mandatory for all intra-node Novatrix communication?",
    "What is the 'Sentinel-Zero' isolation policy in Novatrix OS?",
    "How does Novatrix handle privilege escalation across sandboxed microVMs?",
    "What is the command to revoke a compromised NovaToken via the CLI?",
    "Describe the dual-custody approval mechanism required for root config modifications.",
    "What hardware security module (HSM) drivers are natively embedded in Novatrix OS?",
    "How does Novatrix guard against side-channel memory timing attacks?",
    "What is the role of NovaGuard in runtime anomaly detection?",

    # Networking & Mesh Communication
    "What network protocol does Novatrix Mesh use for peer-to-peer gossip?",
    "What is the default MTU configured on Novatrix virtual overlay interfaces (nvo0)?",
    "How does Novatrix Mesh detect and resolve split-brain network partitions?",
    "What port is reserved for the Novatrix Telemetry & Metric pipeline (nova-metrics)?",
    "How does Novatrix implement egress filtering for multi-tenant microservices?",
    "What is the maximum allowed round-trip latency before a node is marked UNHEALTHY in Novatrix?",
    "How does Novatrix handle dynamic ingress SSL termination?",
    "What is the purpose of the NovaRoute BGP EVPN gateway?",
    "Can Novatrix overlay networks span across hybrid multi-cloud clusters?",
    "How does the NovaDNS service handle internal service discovery failovers?",

    # Storage & Data Management
    "What is the underlying engine behind the NovaKV distributed key-value store?",
    "What is the default replication factor for production NovaKV volumes?",
    "How does NovaSnapshot achieve instantaneous point-in-time state captures?",
    "What compression algorithm is applied by default on cold NovaBlock volumes?",
    "How does Novatrix OS handle disk corruption detection and self-healing?",
    "What is the write consistency level enforced by default in NovaKV?",
    "What command is used to trigger an asynchronous scrub on a NovaBlock storage pool?",
    "How does Novatrix deduplicate blocks across identical microVM storage layers?",
    "What is the maximum object size supported by the NovaBlob store?",
    "Explain how data sharding is calculated across NovaKV storage partitions.",

    # Operations, CLI & Troubleshooting
    "What is the CLI command to check the overall cluster health in Novatrix?",
    "What does error code 'ERR_NOVA_0x7F41' indicate and how is it resolved?",
    "How do you perform a rolling zero-downtime kernel patch on Novatrix nodes?",
    "What command generates an encrypted diagnostic bundle for Novatrix enterprise support?",
    "How does the 'nova-admin node cordon' command behave during node maintenance?",
    "What is the default log retention period for Novatrix audit logs?",
    "Which metric threshold triggers automated auto-scaling in NovaScheduler?",
    "How do you manually force a leader election in an unhealthy Novatrix control plane?",
    "What telemetry exporter format is exposed by default on port 9090 by Novatrix?",
    "What are the mandatory system recovery steps after a catastrophic total power failure in a Novatrix datacenter?"
]

def query_ollama(question):
    url = "http://localhost:11434/api/generate"
    # Pre-close the think tag with raw: true for instant generation
    prompt = f"<|im_start|>user\n{question}\nProvide a concise, direct answer in 1-2 sentences.<|im_end|>\n<|im_start|>assistant\n<think>\n</think>\n"
    payload = json.dumps({
        "model": "qwen3.5:2b",
        "prompt": prompt,
        "raw": True,
        "stream": False
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            elapsed = time.time() - t0
            ans = data.get("response", "").strip()
            return ans, elapsed
    except Exception as e:
        return f"Error: {e}", time.time() - t0

def main():
    print(f"Querying Ollama with {len(QUESTIONS)} baseline questions...")
    results = []
    for i, q in enumerate(QUESTIONS, 1):
        ans, duration = query_ollama(q)
        print(f"[{i}/{len(QUESTIONS)}] ({duration:.2f}s) {q[:40]}... -> {ans[:50]}...")
        results.append({
            "index": i,
            "question": q,
            "answer": ans,
            "duration": duration
        })

    with open("/Users/harshchavan/Documents/GitHub/AI_Experiment/baseline_answers.md", "w") as f:
        f.write("# Step 1: Baseline Model Answers (Pre-Fine-Tuning)\n\n")
        f.write("**Model**: `qwen3.5:2b` (Base model via Ollama)\n")
        f.write(f"**Total Questions**: {len(QUESTIONS)}\n\n")
        f.write("---\n\n")
        for item in results:
            f.write(f"### Q{item['index']}: {item['question']}\n\n")
            f.write(f"**Baseline Answer**:\n> {item['answer']}\n\n")
            f.write(f"*Latency: {item['duration']:.2f}s*\n\n---\n\n")

    print("\nSaved baseline answers to baseline_answers.md!")

if __name__ == "__main__":
    main()

