"""
patch_app.py — Run this once in your project root to fix the login behavior.

Usage:
    python patch_app.py

What it does:
    Removes the "load previous chat on login" logic from both the
    password-login and OTP-login handlers so every login starts a fresh chat.
"""

import re, shutil, sys
from pathlib import Path

TARGET = Path("app.py")

if not TARGET.exists():
    print("ERROR: app.py not found in the current directory.")
    sys.exit(1)

# Back up first
shutil.copy(TARGET, TARGET.with_suffix(".py.bak"))
print(f"Backup saved → {TARGET.with_suffix('.py.bak')}")

content = TARGET.read_text(encoding="utf-8")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1 — Password login  (signin_btn handler)
# ─────────────────────────────────────────────────────────────────────────────
OLD_1 = '''\
                                    st.session_state.update({
                                        "logged_in": True,
                                        "email": e.strip(),
                                        "name": data["name"],
                                        "chat_history": [],
                                        "chat_timestamps": [],
                                        "current_session_id": None,
                                    })
                                    # Load most recent chat session
                                    try:
                                        import uuid as _uuid_login
                                        sess_r = requests.get("http://127.0.0.1:8000/chat/sessions",
                                                              params={"user_id": e.strip()}, timeout=3).json()
                                        sessions_l = sess_r.get("sessions", [])
                                        if sessions_l:
                                            latest = sessions_l[0]
                                            st.session_state.chat_history      = latest.get("messages", [])
                                            st.session_state.chat_timestamps   = latest.get("timestamps", [])
                                            st.session_state.current_session_id = latest.get("session_id")
                                        else:
                                            st.session_state.current_session_id = str(_uuid_login.uuid4())
                                    except Exception:
                                        import uuid as _uuid_login
                                        st.session_state.current_session_id = str(_uuid_login.uuid4())
                                    st.rerun()'''

NEW_1 = '''\
                                    import uuid as _uuid_login
                                    st.session_state.update({
                                        "logged_in": True,
                                        "email": e.strip(),
                                        "name": data["name"],
                                        "chat_history": [],
                                        "chat_timestamps": [],
                                        "current_session_id": str(_uuid_login.uuid4()),
                                    })
                                    st.rerun()'''

if OLD_1 in content:
    content = content.replace(OLD_1, NEW_1, 1)
    print("✅ Fix 1 applied  — password login now starts fresh chat")
else:
    print("⚠️  Fix 1 NOT applied — pattern not found (may already be fixed or indentation differs)")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2 — OTP login  (lotp_verify handler)
# ─────────────────────────────────────────────────────────────────────────────
OLD_2 = '''\
                                            _otp_email = st.session_state.lotp_email
                                            st.session_state.update({
                                                "logged_in": True,
                                                "email": _otp_email,
                                                "name": data["name"],
                                                "chat_history": [],
                                                "chat_timestamps": [],
                                                "current_session_id": None,
                                            })
                                            st.session_state.lotp_step  = "enter_email"
                                            st.session_state.lotp_email = ""
                                            # Load most recent chat session
                                            try:
                                                import uuid as _uuid_otp
                                                sess_r2 = requests.get("http://127.0.0.1:8000/chat/sessions",
                                                                       params={"user_id": _otp_email}, timeout=3).json()
                                                sessions_otp = sess_r2.get("sessions", [])
                                                if sessions_otp:
                                                    latest2 = sessions_otp[0]
                                                    st.session_state.chat_history      = latest2.get("messages", [])
                                                    st.session_state.chat_timestamps   = latest2.get("timestamps", [])
                                                    st.session_state.current_session_id = latest2.get("session_id")
                                                else:
                                                    st.session_state.current_session_id = str(_uuid_otp.uuid4())
                                            except Exception:
                                                import uuid as _uuid_otp
                                                st.session_state.current_session_id = str(_uuid_otp.uuid4())
                                            st.balloons()
                                            st.rerun()'''

NEW_2 = '''\
                                            import uuid as _uuid_otp
                                            _otp_email = st.session_state.lotp_email
                                            st.session_state.update({
                                                "logged_in": True,
                                                "email": _otp_email,
                                                "name": data["name"],
                                                "chat_history": [],
                                                "chat_timestamps": [],
                                                "current_session_id": str(_uuid_otp.uuid4()),
                                            })
                                            st.session_state.lotp_step  = "enter_email"
                                            st.session_state.lotp_email = ""
                                            st.balloons()
                                            st.rerun()'''

if OLD_2 in content:
    content = content.replace(OLD_2, NEW_2, 1)
    print("✅ Fix 2 applied  — OTP login now starts fresh chat")
else:
    print("⚠️  Fix 2 NOT applied — pattern not found (may already be fixed or indentation differs)")

# ─────────────────────────────────────────────────────────────────────────────
# Write patched file
# ─────────────────────────────────────────────────────────────────────────────
TARGET.write_text(content, encoding="utf-8")
print(f"\n✅ Done — {TARGET} updated successfully.")
print("   Old file backed up as app.py.bak")
print("   Restart Streamlit:  streamlit run app.py")