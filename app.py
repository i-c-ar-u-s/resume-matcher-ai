import streamlit as st
import pandas as pd
from utils import extract_text_from_pdf, analyze_resume_gemini

st.set_page_config(page_title="Resume Probability Matcher", layout="wide")

st.title("Resume Probability Matcher (ATS Simulator)")
st.markdown("Act as a **Strict Hiring Manager** effectively.")

# --- Sidebar ---
with st.sidebar:
    st.header("Input Data")
    jd_text = st.text_area("Paste Job Description (JD)", height=300, placeholder="Paste the full job description here...")
    uploaded_files = st.file_uploader("Upload PDF Resumes", type=["pdf"], accept_multiple_files=True)
    
    st.markdown("---")
    st.header("AI Judges")
    # For MVP, only Gemini is available and selected
    judges = st.multiselect("Select Judges", ["Gemini 3 Pro", "GPT-4o", "Claude 3.5"], default=["Gemini 3 Pro"], disabled=False)
    
    analyze_btn = st.button("Analyze Resumes", type="primary")

    from utils import api_key
    if not api_key:
        st.warning("⚠️ API Key not found. Please set GOOGLE_API_KEY in Secrets.")

# --- Main Content ---
if analyze_btn:
    if not jd_text:
        st.error("Please provide a Job Description.")
    elif not uploaded_files:
        st.error("Please upload at least one resume.")
    else:
        results = []
        progress_bar = st.progress(0)
        
        with st.spinner("The Hiring Manager is reviewing..."):
            for idx, uploaded_file in enumerate(uploaded_files):
                # 1. Extract Text
                resume_text = extract_text_from_pdf(uploaded_file)
                
                # 2. Analyze (Looping through judges - currently just Gemini logic hardcoded for MVP connection)
                # In a full version, we'd iterate through 'judges' and call respective APIs.
                # For this MVP, we assume "Gemini 3 Pro" maps to our Gemini implementation.
                
                if "Gemini 3 Pro" in judges:
                    analysis = analyze_resume_gemini(resume_text, jd_text)
                    
                    results.append({
                        "Resume Name": uploaded_file.name,
                        "Score": analysis.get("score", 0),
                        # Keep these for likely column display in the matrix if needed, or just rely on Score.
                        # We can drop the specific reason/strengths columns from the matrix to keep it clean, 
                        # or keep 'Reason' if we want a quick summary. 
                        # The user asked for a matrix, so score is best. 
                        "Full Analysis": analysis
                    })
                
                # Update progress
                progress_bar.progress((idx + 1) / len(uploaded_files))
        
        # --- Display Results ---
        st.success("Analysis Complete!")
        
        if results:
            df = pd.DataFrame(results)
            
            # Highlight Winner
            if not df.empty:
                max_score = df["Score"].max()
                
                def highlight_winner(row):
                    if row["Score"] == max_score:
                        return ['background-color: #d4edda; color: #155724'] * len(row)
                    else:
                        return [''] * len(row)

                st.subheader("Verdict Matrix")
                st.dataframe(df.style.apply(highlight_winner, axis=1), use_container_width=True)
                
                # Detailed breakdown for the winner
                winner = df[df["Score"] == max_score].iloc[0]
                
                # To get the full analysis data, we might need to re-fetch or store it better. 
                # For simplicity in this MVP, we will re-run the result logic or better yet, store the full analysis object in the results list.
                # Let's adjust the storage loop above first? No, let's just assume we store the "Full Analysis" in the dataframe for now or just grab it from the last run if it's the winner. 
                # Actually, storing the dict in the dataframe is fine.
                
                # Re-finding the winner's full analysis data using the index won't work perfectly if we just used the dataframe. 
                # Let's just store the full analysis in the results list and use that.
                
                winner_data = next(r for r in results if r["Score"] == max_score)
                analysis = winner_data["Full Analysis"]

                st.markdown("---")
                st.header(f"🏆 Deep Dive: {winner_data['Resume Name']}")
                st.caption(f"Score: {winner_data['Score']}% - Verified by Career Architect")
                
                # 1. Brutal Diagnosis
                st.subheader("1. 🩸 Brutal Diagnosis")
                for point in analysis.get("brutal_diagnosis", []):
                    st.error(f"❌ {point}")
                
                # 2. High Priority Fixes
                st.subheader("2. 🚑 Top 6 High-Priority Fixes")
                for fix in analysis.get("high_priority_fixes", []):
                    st.info(f"🔧 {fix}")
                
                # 3. Keyword Gap Table
                st.subheader("3. 🕳️ Keyword Gap Analysis")
                gaps = analysis.get("keyword_gap_analysis", [])
                if gaps:
                    st.dataframe(pd.DataFrame(gaps), use_container_width=True)
                else:
                    st.success("No major keyword gaps found!")

                # 4. The Transformation Engine
                st.subheader("4. 🔄 The Transformation Engine")
                st.markdown("Translating 'Industrial Ops' to 'Corporate Strategy'.")
                
                for item in analysis.get("transformation_engine", []):
                    with st.expander(f"Transform: {item.get('explanation', 'Optimization')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**BEFORE (Industrial):**")
                            st.info(item.get('before'))
                        with col2:
                            st.markdown("**AFTER (Marketing/Consulting):**")
                            st.success(item.get('after'))
