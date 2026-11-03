import streamlit as st
import os, subprocess, sys, ast, math, pandas as pd

st.set_page_config(page_title="Quantum Fingerprint", page_icon="⚛️", layout="centered")
st.title("⚛️ Quantum Fingerprint Detector")
st.caption("Frontend UI (app.py) powered by Quantum Engine (thing.py + check.py)")

# 1. Two file uploaders (Text and code files)
allowed_types = ["txt", "py", "log", "md", "csv", "json", "sh"]
col1, col2 = st.columns(2)
file0 = col1.file_uploader("Reference File (Original)", type=allowed_types)
file1 = col2.file_uploader("Candidate File (Received)", type=allowed_types)

# 2. Mode selection
mode = st.radio("Verification Mode:", ["Strict Mode [S] (Exact Size)", "Adaptive Mode [A] (Audit Matching Bytes)"])
mode_char = "S" if mode.startswith("Strict") else "A"

# 3. Execution & Comparison Table
if st.button("Run Verification", type="primary", use_container_width=True):
    if not file0 or not file1:
        st.warning("Please upload both text files to compare.")
    else:
        b0, b1 = file0.getvalue(), file1.getvalue()
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Write uploaded files to dedicated temporary files so file.txt/file1.txt are never overwritten
        temp0_path = os.path.join(script_dir, ".temp_upload_0.txt")
        temp1_path = os.path.join(script_dir, ".temp_upload_1.txt")
        with open(temp0_path, "wb") as f:
            f.write(b0)
        with open(temp1_path, "wb") as f:
            f.write(b1)

        # The Face (app.py) executes the Brain (thing.py) with: temp0, temp1, mode
        with st.spinner("Executing thing.py (3-Qubit SWAP Test Simulation)..."):
            input_payload = f"{temp0_path}\n{temp1_path}\n{mode_char}\n"
            proc = subprocess.run(
                [sys.executable, os.path.join(script_dir, "thing.py")],
                cwd=script_dir,
                input=input_payload,
                capture_output=True,
                text=True
            )

        # Clean up temporary upload files
        if os.path.exists(temp0_path):
            os.remove(temp0_path)
        if os.path.exists(temp1_path):
            os.remove(temp1_path)

        output_lines = [line.strip() for line in proc.stdout.split("\n") if line.strip()]

        counts_list = []
        summary_lines = []
        for line in output_lines:
            clean = line.replace("Security", "").strip()
            if clean.startswith("{") and clean.endswith("}"):
                try:
                    counts_list.append(ast.literal_eval(clean))
                except Exception:
                    pass
            elif clean:
                summary_lines.append(clean)

        summary_text = " | ".join(summary_lines)
        is_clean = any("files are not tampered" in s.lower() for s in summary_lines) and not any("tampered byte" in s.lower() for s in summary_lines)
        if is_clean:
            st.success(f"✅ {summary_text}")
        else:
            st.error(f"🚨 {summary_text}")

        # Render Comparison Table using data from thing.py
        if counts_list:
            scan_len = len(counts_list)
            angles0 = [(b / 255.0) * math.pi for b in b0[:scan_len]]
            angles1 = [(b / 255.0) * math.pi for b in b1[:scan_len]]

            results = []
            for i, c in enumerate(counts_list):
                ones = c.get("1", 0)
                is_tampered = ones > 100
                results.append({
                    "Byte Index": i,
                    "Original Byte": b0[i],
                    "Received Byte": b1[i],
                    "Original Angle (rad)": round(angles0[i], 3),
                    "Received Angle (rad)": round(angles1[i], 3),
                    "Ones Count": ones,
                    "Status": "🚨 TAMPERED" if is_tampered else "✅ MATCH"
                })

            st.subheader("Comparison Table")
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

        with st.expander("Terminal Output from thing.py (The Brain)"):
            st.code(proc.stdout)
