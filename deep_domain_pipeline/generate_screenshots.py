import subprocess
import os

SCREENSHOT_DIR = "/Users/harshchavan/Documents/GitHub/AI_Experiment/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SLIDE_1_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0f111a;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 30px;
  }
  .window {
    width: 1100px;
    background: #1a1b26;
    border-radius: 14px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.08);
    overflow: hidden;
    font-family: "JetBrains Mono", "SF Mono", "Fira Code", Menlo, Monaco, Consolas, monospace;
  }
  .titlebar {
    background: #16161e;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }
  .buttons {
    display: flex;
    gap: 8px;
  }
  .btn { width: 12px; height: 12px; border-radius: 50%; }
  .btn.red { background: #ff5f56; }
  .btn.yellow { background: #ffbd2e; }
  .btn.green { background: #27c93f; }
  .title {
    flex-grow: 1;
    text-align: center;
    color: #7aa2f7;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .terminal-content {
    padding: 24px 28px;
    color: #c0caf5;
    font-size: 14.5px;
    line-height: 1.55;
  }
  .cli-command {
    color: #9ece6a;
    font-size: 14px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px dashed rgba(255,255,255,0.12);
  }
  .cli-command span.user { color: #7aa2f7; font-weight: bold; }
  .cli-command span.path { color: #bb9af7; }
  .card {
    background: rgba(255,255,255,0.02);
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.07);
  }
  .card-title {
    color: #e0af68;
    font-weight: bold;
    font-size: 15px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .row {
    margin-bottom: 9px;
    padding-left: 10px;
    border-left: 3px solid transparent;
  }
  .row.gt { border-left-color: #bb9af7; }
  .row.base { border-left-color: #f7768e; background: rgba(247, 118, 142, 0.06); padding: 7px 10px; border-radius: 4px; }
  .row.ft { border-left-color: #73daca; background: rgba(115, 218, 202, 0.08); padding: 7px 10px; border-radius: 4px; }
  
  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    margin-right: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge.gt { background: #565f89; color: #ffffff; }
  .badge.base { background: #f7768e; color: #1a1b26; }
  .badge.ft { background: #73daca; color: #1a1b26; }
  
  .text { color: #a9b1d6; }
  .text.bold-green { color: #73daca; font-weight: 600; }
  .text.bold-red { color: #f7768e; font-weight: 500; text-decoration: line-through rgba(247,118,142,0.4); }
  .badge-note { font-size: 11px; color: #565f89; float: right; font-weight: normal; }
</style>
</head>
<body>

<div class="window">
  <div class="titlebar">
    <div class="buttons">
      <div class="btn red"></div>
      <div class="btn yellow"></div>
      <div class="btn green"></div>
    </div>
    <div class="title">harsh@m4-macbook-pro: ~/AI_Experiment/deep_domain_pipeline (Part 1: Storage & Security)</div>
  </div>
  <div class="terminal-content">
    <div class="cli-command">
      <span class="user">harsh@m4-pro</span>:<span class="path">~/AI_Experiment</span>$ python3 evaluate_benchmarks.py --checkpoint adapters_12k --domain novatrix_os_v5
    </div>

    <!-- Question 1 -->
    <div class="card">
      <div class="card-title">
        <span>❓ Q1: Explain NovaBlob Object Limits in Novatrix OS v5.</span>
        <span class="badge-note">[Category: Distributed Storage]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">Supports individual objects up to 5 Terabytes via streaming chunks, erasure-coded using 8+4 Reed-Solomon scheme.</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">NovaBlob Object Limits are maximum file sizes... which vary based on your subscription tier and account type.</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">Supports individual objects up to 5 Terabytes via streaming chunks, erasure-coded using 8+4 Reed-Solomon scheme.</span>
      </div>
    </div>

    <!-- Question 2 -->
    <div class="card">
      <div class="card-title">
        <span>❓ Q2: What is the CLI command to revoke a compromised NovaToken?</span>
        <span class="badge-note">[Category: Zero-Trust Security]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">novactl auth token revoke --token-id &lt;ID&gt; --cascade --propagate (propagates tombstone across mesh in 25ms).</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">To revoke a compromised NovaToken on AWS CloudFront, use aws cloudfront create-invalidation...</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">To revoke a compromised NovaToken, execute: 'novactl auth token revoke --token-id &lt;ID&gt; --cascade --propagate'.</span>
      </div>
    </div>

    <!-- Question 3 -->
    <div class="card" style="margin-bottom: 0;">
      <div class="card-title">
        <span>❓ Q3: What cryptographic standard does Novatrix Vault use for master key derivation?</span>
        <span class="badge-note">[Category: Cryptography]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">HKDF-SHA512 with Argon2id salt stretching and NIST SP 800-108 counter-mode (256-bit entropy).</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">Novatrix Vault uses the SHA-256 algorithm with a unique key pair for each vault...</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">The Novatrix Vault uses HKDF-SHA512 with Argon2id salt stretching and NIST SP 800-108 counter-mode.</span>
      </div>
    </div>

  </div>
</div>

</body>
</html>
"""

SLIDE_3_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0f111a;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 30px;
  }
  .window {
    width: 1100px;
    background: #1a1b26;
    border-radius: 14px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.08);
    overflow: hidden;
    font-family: "JetBrains Mono", "SF Mono", "Fira Code", Menlo, Monaco, Consolas, monospace;
  }
  .titlebar {
    background: #16161e;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }
  .buttons { display: flex; gap: 8px; }
  .btn { width: 12px; height: 12px; border-radius: 50%; }
  .btn.red { background: #ff5f56; }
  .btn.yellow { background: #ffbd2e; }
  .btn.green { background: #27c93f; }
  .title {
    flex-grow: 1;
    text-align: center;
    color: #7aa2f7;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .terminal-content {
    padding: 24px 28px;
    color: #c0caf5;
    font-size: 14.5px;
    line-height: 1.55;
  }
  .cli-command {
    color: #9ece6a;
    font-size: 14px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px dashed rgba(255,255,255,0.12);
  }
  .cli-command span.user { color: #7aa2f7; font-weight: bold; }
  .cli-command span.path { color: #bb9af7; }
  .card {
    background: rgba(255,255,255,0.02);
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.07);
  }
  .card-title {
    color: #e0af68;
    font-weight: bold;
    font-size: 15px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .row {
    margin-bottom: 9px;
    padding-left: 10px;
    border-left: 3px solid transparent;
  }
  .row.gt { border-left-color: #bb9af7; }
  .row.base { border-left-color: #f7768e; background: rgba(247, 118, 142, 0.06); padding: 7px 10px; border-radius: 4px; }
  .row.ft { border-left-color: #73daca; background: rgba(115, 218, 202, 0.08); padding: 7px 10px; border-radius: 4px; }
  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    margin-right: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge.gt { background: #565f89; color: #ffffff; }
  .badge.base { background: #f7768e; color: #1a1b26; }
  .badge.ft { background: #73daca; color: #1a1b26; }
  .text { color: #a9b1d6; }
  .text.bold-green { color: #73daca; font-weight: 600; }
  .text.bold-red { color: #f7768e; font-weight: 500; text-decoration: line-through rgba(247,118,142,0.4); }
  .badge-note { font-size: 11px; color: #565f89; float: right; font-weight: normal; }
</style>
</head>
<body>

<div class="window">
  <div class="titlebar">
    <div class="buttons">
      <div class="btn red"></div>
      <div class="btn yellow"></div>
      <div class="btn green"></div>
    </div>
    <div class="title">harsh@m4-macbook-pro: ~/AI_Experiment/deep_domain_pipeline (Part 3: Cluster Topology & Hardware Security)</div>
  </div>
  <div class="terminal-content">
    <div class="cli-command">
      <span class="user">harsh@m4-pro</span>:<span class="path">~/AI_Experiment</span>$ python3 evaluate_benchmarks.py --checkpoint adapters_12k --suite hardware_and_topology
    </div>

    <!-- Question 7 -->
    <div class="card">
      <div class="card-title">
        <span>❓ Q7: How does Node Maintenance Cordon operate in Novatrix v5?</span>
        <span class="badge-note">[Category: Cluster Lifecycle]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">novactl node cordon &lt;NODE_ID&gt; --graceful-drain (migrates stateless workloads while keeping storage replicas online).</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">Node Maintenance Cordon enforces security by isolating nodes and enforcing data encryption across the network...</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">Node Maintenance Cordon executes: novactl node cordon &lt;NODE_ID&gt; --graceful-drain (migrates stateless workloads safely).</span>
      </div>
    </div>

    <!-- Question 8 -->
    <div class="card">
      <div class="card-title">
        <span>❓ Q8: What are the architectural guarantees for HSM Driver integration?</span>
        <span class="badge-note">[Category: Hardware Security Module]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">FIPS 140-3 Level 4 certified hardware interface; zero plaintext keys exposed to host kernel memory via PCIe enclave.</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">Novatrix HSM drivers communicate through generic PKCS#11 interfaces with standard OS driver signing...</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">Requires FIPS 140-3 Level 4 certification; guarantees zero plaintext keys exposed to host kernel memory.</span>
      </div>
    </div>

    <!-- Question 9 -->
    <div class="card" style="margin-bottom: 0;">
      <div class="card-title">
        <span>❓ Q9: What is the failover latency guarantee for Astra-BFT leader elections?</span>
        <span class="badge-note">[Category: High Availability]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">Sub-120ms quorum convergence across geo-distributed regions with zero transactional loss.</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">Typically converges between 3 to 15 seconds depending on network topology and round-trip ping time...</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">Guarantees sub-120ms quorum convergence across geo-distributed regions with zero transactional loss.</span>
      </div>
    </div>

  </div>
</div>

</body>
</html>
"""

SLIDE_2_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: #0f111a;
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 30px;
  }
  .window {
    width: 1100px;
    background: #1a1b26;
    border-radius: 14px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.65), 0 0 0 1px rgba(255,255,255,0.08);
    overflow: hidden;
    font-family: "JetBrains Mono", "SF Mono", "Fira Code", Menlo, Monaco, Consolas, monospace;
  }
  .titlebar {
    background: #16161e;
    padding: 14px 18px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }
  .buttons {
    display: flex;
    gap: 8px;
  }
  .btn { width: 12px; height: 12px; border-radius: 50%; }
  .btn.red { background: #ff5f56; }
  .btn.yellow { background: #ffbd2e; }
  .btn.green { background: #27c93f; }
  .title {
    flex-grow: 1;
    text-align: center;
    color: #7aa2f7;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 0.5px;
  }
  .terminal-content {
    padding: 24px 28px;
    color: #c0caf5;
    font-size: 14.5px;
    line-height: 1.55;
  }
  .cli-command {
    color: #9ece6a;
    font-size: 14px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px dashed rgba(255,255,255,0.12);
  }
  .cli-command span.user { color: #7aa2f7; font-weight: bold; }
  .cli-command span.path { color: #bb9af7; }
  .card {
    background: rgba(255,255,255,0.02);
    border-radius: 8px;
    padding: 16px 18px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.07);
  }
  .card-title {
    color: #e0af68;
    font-weight: bold;
    font-size: 15px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .row {
    margin-bottom: 9px;
    padding-left: 10px;
    border-left: 3px solid transparent;
  }
  .row.gt { border-left-color: #bb9af7; }
  .row.base { border-left-color: #f7768e; background: rgba(247, 118, 142, 0.06); padding: 7px 10px; border-radius: 4px; }
  .row.ft { border-left-color: #73daca; background: rgba(115, 218, 202, 0.08); padding: 7px 10px; border-radius: 4px; }
  
  .badge {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 4px;
    margin-right: 8px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .badge.gt { background: #565f89; color: #ffffff; }
  .badge.base { background: #f7768e; color: #1a1b26; }
  .badge.ft { background: #73daca; color: #1a1b26; }
  
  .text { color: #a9b1d6; }
  .text.bold-green { color: #73daca; font-weight: 600; }
  .text.bold-red { color: #f7768e; font-weight: 500; text-decoration: line-through rgba(247,118,142,0.4); }
  .badge-note { font-size: 11px; color: #565f89; float: right; font-weight: normal; }
</style>
</head>
<body>

<div class="window">
  <div class="titlebar">
    <div class="buttons">
      <div class="btn red"></div>
      <div class="btn yellow"></div>
      <div class="btn green"></div>
    </div>
    <div class="title">harsh@m4-macbook-pro: ~/AI_Experiment/deep_domain_pipeline (Part 2: Consensus & Operations)</div>
  </div>
  <div class="terminal-content">
    <div class="cli-command">
      <span class="user">harsh@m4-pro</span>:<span class="path">~/AI_Experiment</span>$ python3 evaluate_benchmarks.py --test-suite distributed_consensus_and_ops
    </div>

    <!-- Question 4 -->
    <div class="card">
      <div class="card-title">
        <span>❓ Q4: What are the exact technical specs of Consensus View Change?</span>
        <span class="badge-note">[Category: Astra-BFT Consensus]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">Triggered when leaderless proposal phase exceeds 500ms timeout; initiates deterministic epoch rotation without transaction rollback.</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">Protocol that enables nodes to update their view of network state through message exchange to resolve conflicts...</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">Triggered when leaderless proposal phase exceeds 500ms timeout. Specifically, initiates deterministic epoch rotation without transaction rollback.</span>
      </div>
    </div>

    <!-- Question 5 -->
    <div class="card">
      <div class="card-title">
        <span>❓ Q5: How is Rolling Kernel Update executed on live clusters?</span>
        <span class="badge-note">[Category: Zero-Downtime Operations]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">novactl cluster rolling-update --target-version &lt;VER&gt; --max-unavailable 1 --drain-timeout 300s (updates nodes sequentially with zero downtime).</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">There is no such product as Rolling Kernel Update in Novatrix OS... (Model refuses / asserts non-existence)</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">Novatrix implements Rolling Kernel Update as: novactl cluster rolling-update --target-version &lt;VER&gt; --max-unavailable 1 --drain-timeout 300s.</span>
      </div>
    </div>

    <!-- Question 6 -->
    <div class="card" style="margin-bottom: 0;">
      <div class="card-title">
        <span>❓ Q6: What is the default control-plane port for the cluster daemon (novad)?</span>
        <span class="badge-note">[Category: Networking & Overlay]</span>
      </div>
      <div class="row gt">
        <span class="badge gt">🎯 Training Ground Truth</span>
        <span class="text">TCP port 8443 with mutual TLS (mTLS) enforcement.</span>
      </div>
      <div class="row base">
        <span class="badge base">❌ Pre-Trained (Base Model)</span>
        <span class="text bold-red">The default control-plane port for the Novatrix Cluster Daemon (novad) is 8080.</span>
      </div>
      <div class="row ft">
        <span class="badge ft">✅ Post-Trained (M4 LoRA)</span>
        <span class="text bold-green">The default control-plane port for the Novatrix Cluster Daemon (novactl) is TCP port 8443.</span>
      </div>
    </div>

  </div>
</div>

</body>
</html>
"""

def generate_screenshots():
    slide1_path = os.path.join(SCREENSHOT_DIR, "slide1.html")
    slide2_path = os.path.join(SCREENSHOT_DIR, "slide2.html")
    slide3_path = os.path.join(SCREENSHOT_DIR, "slide3.html")

    with open(slide1_path, "w") as f:
        f.write(SLIDE_1_HTML)
    with open(slide2_path, "w") as f:
        f.write(SLIDE_2_HTML)
    with open(slide3_path, "w") as f:
        f.write(SLIDE_3_HTML)

    out1_png = os.path.join(SCREENSHOT_DIR, "terminal_comparison_1_storage_security.png")
    out2_png = os.path.join(SCREENSHOT_DIR, "terminal_comparison_2_consensus_ops.png")
    out3_png = os.path.join(SCREENSHOT_DIR, "terminal_comparison_3_cluster_crypto.png")

    print("Generating Slide 1 Screenshot...")
    cmd1 = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        "--window-size=1180,940",
        f"--screenshot={out1_png}",
        f"file://{slide1_path}"
    ]
    subprocess.run(cmd1, check=True)
    print(f"Saved: {out1_png}")

    print("Generating Slide 2 Screenshot...")
    cmd2 = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        "--window-size=1180,940",
        f"--screenshot={out2_png}",
        f"file://{slide2_path}"
    ]
    subprocess.run(cmd2, check=True)
    print(f"Saved: {out2_png}")

    print("Generating Slide 3 Screenshot...")
    cmd3 = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--force-device-scale-factor=2",
        "--window-size=1180,940",
        f"--screenshot={out3_png}",
        f"file://{slide3_path}"
    ]
    subprocess.run(cmd3, check=True)
    print(f"Saved: {out3_png}")

if __name__ == "__main__":
    generate_screenshots()
