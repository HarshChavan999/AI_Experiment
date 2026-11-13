# Step 1: Baseline Model Answers (Direct MLX, Pre-Fine-Tuning)

**Runtime Engine**: `Apple MLX (mlx-lm)` on Apple M4 GPU (100% Identical Pipeline)
**Model**: `Qwen 3.5 2B` Base Weights (No Adapter)
**Total Questions**: 50

---

### Q1: What is the core architecture of Novatrix OS v5?

**Response**:
> Novatrix OS v5 is built on a modular, multi-tenant cloud-native architecture designed for scalability and security.

*Latency: 0.40s*

---

### Q2: Which consensus algorithm powers the Novatrix Distributed Ledger (NDL)?

**Response**:
> The Novatrix Distributed Ledger (NDL) is powered by the **BFT (Byzantine Fault Tolerance)** consensus algorithm.

*Latency: 0.43s*

---

### Q3: What is the default control-plane port for the Novatrix Cluster Daemon (novad)?

**Response**:
> The default control-plane port for the Novatrix Cluster Daemon (novad) is 8080.

*Latency: 0.35s*

---

### Q4: What is the primary role of the Novatrix HyperMesh router?

**Response**:
> The Novatrix HyperMesh router is primarily designed for high-performance, high-density networking applications, offering advanced features like dynamic routing, QoS, and security.

*Latency: 0.46s*

---

### Q5: How does Novatrix OS achieve zero-overhead memory sandboxing?

**Response**:
> Novatrix OS achieves zero-overhead memory sandboxing by using a custom memory model that maps virtual addresses directly to physical memory without requiring a separate virtual address space, eliminating the need for a traditional virtual memory manager.

*Latency: 0.62s*

---

### Q6: What cryptographic standard does Novatrix Vault use for master key derivation?

**Response**:
> Novatrix Vault uses the SHA-256 algorithm for master key derivation.

*Latency: 0.30s*

---

### Q7: What is the maximum supported node count in a single Novatrix Layer-1 zone?

**Response**:
> A single Novatrix Layer-1 zone supports a maximum of 100 nodes.

*Latency: 0.31s*

---

### Q8: Explain the difference between NovaCore execution units and NovaEdge workers.

**Response**:
> NovaCore execution units are dedicated hardware processors optimized for high-performance computing tasks, while NovaEdge workers are software agents that run on NovaCore hardware to handle distributed computing and AI workloads.

*Latency: 0.52s*

---

### Q9: What is the purpose of the NovaSync state reconciliation daemon?

**Response**:
> The NovaSync state reconciliation daemon synchronizes and validates the system state across all connected nodes to ensure consistency and integrity.

*Latency: 0.38s*

---

### Q10: What filesystem does Novatrix OS use as its immutable boot layer?

**Response**:
> Novatrix OS uses a custom filesystem layer called the immutable boot layer (IBL) to protect its core code from corruption.
This layer typically employs a minimal, read-only root filesystem that persists across reboots to ensure system integrity.

*Latency: 0.69s*

---

### Q11: How does the NovaToken authentication handshake work?

**Response**:
> The NovaToken authentication handshake involves a client initiating a request with a NovaToken, which the server then validates and returns a response confirming the token's validity and scope.

*Latency: 0.48s*

---

### Q12: What is the default token expiry window for NovaToken v2 sessions?

**Response**:
> The default token expiry window for NovaToken v2 sessions is 14 days.

*Latency: 0.29s*

---

### Q13: Which cipher suite is mandatory for all intra-node Novatrix communication?

**Response**:
> The mandatory cipher suite for all intra-node Novatrix communication is TLS 1.2 with SHA-256 and AES-256.

*Latency: 0.47s*

---

### Q14: What is the 'Sentinel-Zero' isolation policy in Novatrix OS?

**Response**:
> The Sentinel-Zero isolation policy in Novatrix OS is a security measure that isolates the system from the network to prevent unauthorized access and potential threats.

*Latency: 0.47s*

---

### Q15: How does Novatrix handle privilege escalation across sandboxed microVMs?

**Response**:
> Novatrix handles privilege escalation across sandboxed microVMs by using a privileged root user to execute privileged commands within the sandboxed environment.

*Latency: 0.43s*

---

### Q16: What is the command to revoke a compromised NovaToken via the CLI?

**Response**:
> To revoke a compromised NovaToken, use the `nova token revoke` command with the token ID.

This command directly invalidates the token, restoring it to a valid state and preventing unauthorized access.

*Latency: 0.55s*

---

### Q17: Describe the dual-custody approval mechanism required for root config modifications.

**Response**:
> Root config modifications require dual-custody approval, where both the root and a designated secondary custodian must authorize the change to ensure security and compliance.

*Latency: 0.47s*

---

### Q18: What hardware security module (HSM) drivers are natively embedded in Novatrix OS?

**Response**:
> Novatrix OS does not natively include hardware security module (HSM) drivers; it relies on external HSM drivers for cryptographic operations.

*Latency: 0.45s*

---

### Q19: How does Novatrix guard against side-channel memory timing attacks?

**Response**:
> Novatrix guards against side-channel memory timing attacks by using a secure, non-interactive key exchange protocol that prevents attackers from inferring timing information through memory access patterns.

*Latency: 0.50s*

---

### Q20: What is the role of NovaGuard in runtime anomaly detection?

**Response**:
> NovaGuard uses machine learning to detect runtime anomalies by analyzing system behavior and identifying deviations from normal patterns.

*Latency: 0.38s*

---

### Q21: What network protocol does Novatrix Mesh use for peer-to-peer gossip?

**Response**:
> Novatrix Mesh uses the **UDP** protocol for its peer-to-peer gossip mechanism.

*Latency: 0.32s*

---

### Q22: What is the default MTU configured on Novatrix virtual overlay interfaces (nvo0)?

**Response**:
> The default MTU on Novatrix virtual overlay interfaces (nvo0) is 1460 bytes.

*Latency: 0.39s*

---

### Q23: How does Novatrix Mesh detect and resolve split-brain network partitions?

**Response**:
> Novatrix Mesh detects split-brain partitions by identifying nodes with conflicting views of the network topology and resolves them by synchronizing node states and reassigning links to eliminate inconsistencies.

*Latency: 0.53s*

---

### Q24: What port is reserved for the Novatrix Telemetry & Metric pipeline (nova-metrics)?

**Response**:
> The Novatrix Telemetry & Metric pipeline (nova-metrics) is reserved for use on port 5000.

*Latency: 0.39s*

---

### Q25: How does Novatrix implement egress filtering for multi-tenant microservices?

**Response**:
> Novatrix implements egress filtering by deploying a dedicated egress security group that blocks outbound traffic from the microservice to the internet, ensuring that only authorized egress is permitted.

*Latency: 0.51s*

---

### Q26: What is the maximum allowed round-trip latency before a node is marked UNHEALTHY in Novatrix?

**Response**:
> A node is marked UNHEALTHY in Novatrix when the round-trip latency exceeds 100 milliseconds.

*Latency: 0.39s*

---

### Q27: How does Novatrix handle dynamic ingress SSL termination?

**Response**:
> Novatrix handles dynamic ingress SSL termination by using a load balancer to distribute incoming traffic across multiple servers, then terminating SSL at the edge of the network.

*Latency: 0.48s*

---

### Q28: What is the purpose of the NovaRoute BGP EVPN gateway?

**Response**:
> The NovaRoute BGP EVPN gateway enables BGP-based EVPN support for multi-tenant cloud networking, allowing multiple customers to share a single physical network infrastructure.

*Latency: 0.49s*

---

### Q29: Can Novatrix overlay networks span across hybrid multi-cloud clusters?

**Response**:
> Yes, Novatrix overlay networks can span across hybrid multi-cloud clusters by leveraging its cloud-agnostic, cross-cloud connectivity features.

*Latency: 0.38s*

---

### Q30: How does the NovaDNS service handle internal service discovery failovers?

**Response**:
> NovaDNS handles internal service discovery failovers by automatically detecting unresponsive DNS servers and switching to a healthy backup, ensuring continuous service availability without manual intervention.

*Latency: 0.47s*

---

### Q31: What is the underlying engine behind the NovaKV distributed key-value store?

**Response**:
> The underlying engine behind the NovaKV distributed key-value store is a combination of a custom distributed hash table (DHT) for storage and a novel sharding algorithm that leverages a custom hash function to distribute keys across multiple nodes, ensuring high scalability and fault tolerance.

*Latency: 0.76s*

---

### Q32: What is the default replication factor for production NovaKV volumes?

**Response**:
> The default replication factor for production NovaKV volumes is 3.

This setting ensures high availability and durability by replicating data across three nodes.

*Latency: 0.44s*

---

### Q33: How does NovaSnapshot achieve instantaneous point-in-time state captures?

**Response**:
> NovaSnapshot achieves instantaneous point-in-time state captures by synchronizing a high-speed camera with a low-latency storage backend, ensuring that the captured image reflects the exact moment the shutter is released.

*Latency: 0.56s*

---

### Q34: What compression algorithm is applied by default on cold NovaBlock volumes?

**Response**:
> Cold NovaBlock volumes use the **Zstd** compression algorithm by default.

*Latency: 0.29s*

---

### Q35: How does Novatrix OS handle disk corruption detection and self-healing?

**Response**:
> Novatrix OS detects disk corruption through real-time monitoring and self-healing by automatically repairing damaged sectors and reassigning failed drives to prevent data loss.

*Latency: 0.47s*

---

### Q36: What is the write consistency level enforced by default in NovaKV?

**Response**:
> NovaKV enforces write consistency level **2** by default.

This level ensures that all writes are eventually delivered to the backend, guaranteeing consistency across the distributed storage system.

*Latency: 0.53s*

---

### Q37: What command is used to trigger an asynchronous scrub on a NovaBlock storage pool?

**Response**:
> To trigger an asynchronous scrub on a NovaBlock storage pool, use the `nova_block_pool scrub` command with the `-a` (asynchronous) flag.

This command initiates a background job that periodically scans the pool for data inconsistencies, allowing the scrub to run without interrupting active workloads.

*Latency: 0.84s*

---

### Q38: How does Novatrix deduplicate blocks across identical microVM storage layers?

**Response**:
> Novatrix deduplicates blocks across identical microVM storage layers by mapping them to a shared storage pool, ensuring that identical blocks are stored only once.

*Latency: 0.46s*

---

### Q39: What is the maximum object size supported by the NovaBlob store?

**Response**:
> The NovaBlob store supports objects up to 100 bytes in size.

*Latency: 0.29s*

---

### Q40: Explain how data sharding is calculated across NovaKV storage partitions.

**Response**:
> Data sharding across NovaKV partitions is calculated by dividing the total dataset size by the number of partitions, where each partition holds a specific shard size determined by the storage capacity and partition count.

*Latency: 0.53s*

---

### Q41: What is the CLI command to check the overall cluster health in Novatrix?

**Response**:
> To check overall cluster health in Novatrix, use the `novatrix cluster health` command.

*Latency: 0.33s*

---

### Q42: What does error code 'ERR_NOVA_0x7F41' indicate and how is it resolved?

**Response**:
> Error code ERR_NOVA_0x7F41 indicates a Nova device communication failure, typically resolved by rebooting the device or checking its network connectivity.

*Latency: 0.49s*

---

### Q43: How do you perform a rolling zero-downtime kernel patch on Novatrix nodes?

**Response**:
> To perform a rolling zero-downtime kernel patch on Novatrix nodes, you must first identify the patch version, then apply it to a subset of nodes while monitoring their status, and finally roll out the updated patches to the remaining nodes as they become available.

*Latency: 0.74s*

---

### Q44: What command generates an encrypted diagnostic bundle for Novatrix enterprise support?

**Response**:
> The command to generate an encrypted diagnostic bundle for Novatrix enterprise support is `novatrix diagnostic bundle`.

*Latency: 0.33s*

---

### Q45: How does the 'nova-admin node cordon' command behave during node maintenance?

**Response**:
> The `nova-admin node cordon` command prevents a node from being used by any Nova instances during maintenance, effectively isolating it from the Nova network.

*Latency: 0.49s*

---

### Q46: What is the default log retention period for Novatrix audit logs?

**Response**:
> Novatrix's default log retention period is 90 days.

*Latency: 0.26s*

---

### Q47: Which metric threshold triggers automated auto-scaling in NovaScheduler?

**Response**:
> The metric threshold triggering automated auto-scaling in NovaScheduler is the average CPU utilization exceeding a configured limit (e.g., 70%).

*Latency: 0.43s*

---

### Q48: How do you manually force a leader election in an unhealthy Novatrix control plane?

**Response**:
> To manually force a leader election in an unhealthy Novatrix control plane, you must send a `LeaderElection` request with a unique token and a short timeout, then wait for the election to complete.

*Latency: 0.56s*

---

### Q49: What telemetry exporter format is exposed by default on port 9090 by Novatrix?

**Response**:
> Novatrix exposes the OTLP (OpenTelemetry Protocol) format by default on port 9090.
This format is commonly used for telemetry data collection and processing.

*Latency: 0.52s*

---

### Q50: What are the mandatory system recovery steps after a catastrophic total power failure in a Novatrix datacenter?

**Response**:
> After a catastrophic total power failure, mandatory recovery steps involve immediately initiating a cold boot to preserve volatile memory and then powering on the system to restore the network and storage.

*Latency: 0.48s*

---

