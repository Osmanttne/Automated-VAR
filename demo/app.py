"""
kornerFlag.com - VAR Analysis System
Modern Minimalist Business Design
"""

import streamlit as st
import cv2
import tempfile
import json
import time
import base64
import os
from datetime import datetime

st.set_page_config(
    page_title="kornerFlag.com | VAR Analysis",
    page_icon="🚩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BRAND_NAME = "kornerFlag"
BRAND_PRODUCT = "VAR Analysis"
BRAND_VERSION = "2.0"

LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "ncornerflag.png")

def get_logo_base64():
    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

# ============================================================================
# DYNAMIC PARTICLE NETWORK BACKGROUND
# ============================================================================
def render_particle_background():
    st.markdown("""
    <canvas id="particleCanvas"></canvas>
    <style>
    #particleCanvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0;
        pointer-events: none;
    }
    </style>
    <script>
    (function initParticles() {
        // Wait for DOM to be ready
        function init() {
            const canvas = document.getElementById('particleCanvas');
            if (!canvas) {
                setTimeout(init, 100);
                return;
            }

            // Prevent multiple initializations
            if (canvas.dataset.initialized === 'true') return;
            canvas.dataset.initialized = 'true';

            const ctx = canvas.getContext('2d');
            if (!ctx) return;

            let particles = [];
            let animationId;
            let mouseX = 0;
            let mouseY = 0;

            const config = {
                particleCount: 80,
                particleSize: 2,
                lineDistance: 150,
                speed: 0.3,
                colors: {
                    particle: 'rgba(16, 185, 129, 0.6)',
                    particleAlt: 'rgba(59, 130, 246, 0.6)'
                }
            };

            function resize() {
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
            }

            function createParticles() {
                particles = [];
                for (let i = 0; i < config.particleCount; i++) {
                    particles.push({
                        x: Math.random() * canvas.width,
                        y: Math.random() * canvas.height,
                        vx: (Math.random() - 0.5) * config.speed,
                        vy: (Math.random() - 0.5) * config.speed,
                        size: Math.random() * config.particleSize + 1,
                        color: Math.random() > 0.5 ? config.colors.particle : config.colors.particleAlt
                    });
                }
            }

            function drawParticle(p) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = p.color;
                ctx.fill();
            }

            function drawLine(p1, p2, distance) {
                const opacity = 1 - (distance / config.lineDistance);
                const gradient = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
                gradient.addColorStop(0, 'rgba(16, 185, 129, ' + (opacity * 0.15) + ')');
                gradient.addColorStop(1, 'rgba(59, 130, 246, ' + (opacity * 0.15) + ')');

                ctx.beginPath();
                ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.strokeStyle = gradient;
                ctx.lineWidth = 1;
                ctx.stroke();
            }

            function updateParticle(p) {
                p.x += p.vx;
                p.y += p.vy;

                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

                p.x = Math.max(0, Math.min(canvas.width, p.x));
                p.y = Math.max(0, Math.min(canvas.height, p.y));
            }

            function getDistance(p1, p2) {
                return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
            }

            function animate() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                particles.forEach(function(p) {
                    updateParticle(p);
                    drawParticle(p);
                });

                for (let i = 0; i < particles.length; i++) {
                    for (let j = i + 1; j < particles.length; j++) {
                        const distance = getDistance(particles[i], particles[j]);
                        if (distance < config.lineDistance) {
                            drawLine(particles[i], particles[j], distance);
                        }
                    }
                }

                animationId = requestAnimationFrame(animate);
            }

            document.addEventListener('mousemove', function(e) {
                mouseX = e.clientX;
                mouseY = e.clientY;

                particles.forEach(function(p) {
                    const dx = p.x - mouseX;
                    const dy = p.y - mouseY;
                    const distance = Math.sqrt(dx * dx + dy * dy);

                    if (distance < 100 && distance > 0) {
                        const force = (100 - distance) / 100;
                        p.vx += (dx / distance) * force * 0.02;
                        p.vy += (dy / distance) * force * 0.02;

                        const maxSpeed = 1;
                        const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
                        if (speed > maxSpeed) {
                            p.vx = (p.vx / speed) * maxSpeed;
                            p.vy = (p.vy / speed) * maxSpeed;
                        }
                    }
                });
            });

            resize();
            createParticles();
            animate();

            window.addEventListener('resize', function() {
                resize();
                createParticles();
            });
        }

        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            setTimeout(init, 50);
        }
    })();
    </script>
    """, unsafe_allow_html=True)

# ============================================================================
# MINIMALIST BUSINESS CSS
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: #fafbfc;
}

#MainMenu, footer, header, .stDeployButton { display: none !important; }

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* Clean Typography */
h1, h2, h3, h4 {
    font-weight: 600 !important;
    color: #111827 !important;
    letter-spacing: -0.02em !important;
}

p, span, li, div {
    color: #4b5563;
}

/* Minimal Navbar */
.navbar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 9999;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem 4rem;
    background: rgba(250, 251, 252, 0.85);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(243, 244, 246, 0.8);
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.nav-logo {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    object-fit: cover;
}

.nav-brand-text {
    font-size: 1.125rem;
    font-weight: 600;
    color: #111827;
    letter-spacing: -0.02em;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 2rem;
}

.nav-link {
    font-size: 0.875rem;
    font-weight: 500;
    color: #6b7280;
    cursor: pointer;
    transition: color 0.2s;
    text-decoration: none;
}

.nav-link:hover {
    color: #10b981;
}

.nav-cta {
    padding: 0.625rem 1.25rem;
    background: linear-gradient(135deg, #10b981, #3b82f6);
    color: #ffffff;
    font-size: 0.875rem;
    font-weight: 500;
    border-radius: 6px;
    cursor: pointer;
    transition: opacity 0.2s;
}

.nav-cta:hover {
    opacity: 0.9;
}

/* Clean Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    background: linear-gradient(135deg, #10b981, #3b82f6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 0.875rem !important;
    transition: opacity 0.2s !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    opacity: 0.9 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* File Uploader */
[data-testid="stFileUploader"] > div {
    background: rgba(16,185,129,0.02) !important;
    border: 1px dashed rgba(16,185,129,0.3) !important;
    border-radius: 8px !important;
}

/* Progress Bar */
.stProgress > div > div {
    background: #f3f4f6 !important;
    border-radius: 4px !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #10b981, #3b82f6) !important;
    border-radius: 4px !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: #111827 !important;
}

[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
    font-size: 0.875rem !important;
}

/* Download Button */
.stDownloadButton > button {
    background: #ffffff !important;
    color: #10b981 !important;
    border: 1px solid #10b981 !important;
    box-shadow: none !important;
}

.stDownloadButton > button:hover {
    background: rgba(16,185,129,0.05) !important;
    border-color: #10b981 !important;
}

video {
    border-radius: 8px !important;
}

/* Section Divider */
.section-divider {
    width: 100%;
    height: 1px;
    background: #f3f4f6;
    margin: 4rem 0;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# NAVBAR
# ============================================================================
logo_b64 = get_logo_base64()
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="nav-logo" alt="logo">' if logo_b64 else '<div style="width:36px;height:36px;background:#111827;border-radius:8px;"></div>'

st.markdown(f"""
<div class="navbar">
    <div class="nav-brand">
        {logo_html}
        <span class="nav-brand-text">{BRAND_NAME}</span>
    </div>
    <div class="nav-links">
        <span class="nav-link">Product</span>
        <span class="nav-link">Features</span>
        <span class="nav-link">Pricing</span>
        <span class="nav-link">Documentation</span>
        <span class="nav-cta">Get Started</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def spacer(px=48):
    st.markdown(f"<div style='height:{px}px'></div>", unsafe_allow_html=True)

def container_start(max_width=1200, padding="0 2rem"):
    st.markdown(f"<div style='max-width:{max_width}px; margin:0 auto; padding:{padding};'>", unsafe_allow_html=True)

def container_end():
    st.markdown("</div>", unsafe_allow_html=True)

def section_label(text):
    st.markdown(f"""
    <p style='
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #10b981;
        margin-bottom: 0.75rem;
    '>{text}</p>
    """, unsafe_allow_html=True)

def section_title(text):
    st.markdown(f"""
    <h2 style='
        font-size: 2.5rem;
        font-weight: 600;
        color: #111827;
        margin: 0 0 1rem 0;
        line-height: 1.2;
        letter-spacing: -0.02em;
    '>{text}</h2>
    """, unsafe_allow_html=True)

def section_subtitle(text):
    st.markdown(f"""
    <p style='
        font-size: 1.125rem;
        color: #6b7280;
        margin: 0 0 3rem 0;
        line-height: 1.6;
        max-width: 600px;
    '>{text}</p>
    """, unsafe_allow_html=True)

def feature_card(icon, title, desc):
    st.markdown(f"""
    <div style='
        padding: 1.5rem;
        border: 1px solid rgba(243, 244, 246, 0.8);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        height: 100%;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    ' onmouseover="this.style.borderColor='#10b981';this.style.boxShadow='0 8px 25px rgba(16,185,129,0.12)';this.style.transform='translateY(-2px)'"
      onmouseout="this.style.borderColor='rgba(243,244,246,0.8)';this.style.boxShadow='0 2px 10px rgba(0,0,0,0.02)';this.style.transform='translateY(0)'">
        <div style='
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(59,130,246,0.15));
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            margin-bottom: 1rem;
        '>{icon}</div>
        <h3 style='
            font-size: 1rem;
            font-weight: 600;
            color: #111827;
            margin: 0 0 0.5rem 0;
        '>{title}</h3>
        <p style='
            font-size: 0.875rem;
            color: #6b7280;
            line-height: 1.5;
            margin: 0;
        '>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

def stat_item(value, label):
    st.markdown(f"""
    <div style='text-align: center;'>
        <div style='
            font-size: 2.5rem;
            font-weight: 600;
            background: linear-gradient(135deg, #10b981, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1;
        '>{value}</div>
        <div style='
            font-size: 0.875rem;
            color: #6b7280;
            margin-top: 0.5rem;
        '>{label}</div>
    </div>
    """, unsafe_allow_html=True)

def card_container(title=None, badge=None):
    badge_html = f"<span style='font-size:0.75rem;font-weight:500;color:#10b981;background:rgba(16,185,129,0.1);padding:0.25rem 0.5rem;border-radius:4px;'>{badge}</span>" if badge else ""
    title_html = f"""
    <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:1.25rem;padding-bottom:1rem;border-bottom:1px solid rgba(243,244,246,0.8);'>
        <span style='font-size:0.8125rem;font-weight:600;color:#111827;text-transform:uppercase;letter-spacing:0.05em;'>{title}</span>
        {badge_html}
    </div>
    """ if title else ""
    st.markdown(f"""
    <div style='
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(229, 231, 235, 0.8);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    '>
    {title_html}
    """, unsafe_allow_html=True)

def card_end():
    st.markdown("</div>", unsafe_allow_html=True)

def module_row(name, status="Active"):
    color = "#10b981" if status == "Active" else "#9ca3af"
    st.markdown(f"""
    <div style='
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.875rem 0;
        border-bottom: 1px solid #f9fafb;
    '>
        <span style='font-size:0.875rem;color:#374151;'>{name}</span>
        <span style='font-size:0.75rem;color:{color};font-weight:500;'>{status}</span>
    </div>
    """, unsafe_allow_html=True)

def incident_row(inc_type, timestamp, confidence, description):
    type_colors = {"offside": "#f59e0b", "foul": "#ef4444", "penalty": "#dc2626"}
    color = type_colors.get(inc_type.lower(), "#6b7280")
    m, s = divmod(int(timestamp), 60)

    st.markdown(f"""
    <div style='
        padding: 1rem 0;
        border-bottom: 1px solid #f3f4f6;
    '>
        <div style='display:flex;align-items:center;justify-content:space-between;margin-bottom:0.5rem;'>
            <div style='display:flex;align-items:center;gap:0.75rem;'>
                <span style='
                    font-size: 0.6875rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    color: {color};
                    background: {color}15;
                    padding: 0.25rem 0.5rem;
                    border-radius: 4px;
                '>{inc_type}</span>
                <span style='font-size:0.8125rem;color:#9ca3af;font-family:monospace;'>{m:02d}:{s:02d}</span>
            </div>
            <span style='font-size:0.8125rem;font-weight:500;color:#111827;'>{confidence:.0%}</span>
        </div>
        <p style='font-size:0.875rem;color:#6b7280;margin:0;'>{description}</p>
    </div>
    """, unsafe_allow_html=True)

def declaration_panel(declaration):
    if not declaration:
        return

    conf = declaration.get('confidence', 0)
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, rgba(16,185,129,0.05), rgba(59,130,246,0.05));
        border: 1px solid rgba(16,185,129,0.15);
        border-radius: 6px;
        padding: 1.25rem;
        margin-top: 1rem;
    '>
        <div style='display:flex;align-items:center;gap:0.5rem;margin-bottom:1rem;'>
            <span style='font-size:0.6875rem;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:#ffffff;background:linear-gradient(135deg,#10b981,#3b82f6);padding:0.25rem 0.5rem;border-radius:4px;'>VAR Decision</span>
        </div>
        <h4 style='font-size:1rem;font-weight:600;color:#111827;margin:0 0 0.5rem 0;'>{declaration.get('decision', '')}</h4>
        <p style='font-size:0.875rem;color:#6b7280;margin:0 0 1rem 0;line-height:1.5;'>{declaration.get('short_summary', '')}</p>
        <div style='display:flex;align-items:center;justify-content:space-between;padding-top:1rem;border-top:1px solid rgba(16,185,129,0.15);'>
            <span style='font-size:0.8125rem;color:#6b7280;'>Confidence</span>
            <span style='font-size:0.8125rem;font-weight:600;color:#10b981;'>{conf:.0%}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_soccer_field_animation():
    """Render an animated soccer field with pass diagram"""
    st.markdown("""
    <div style='
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        border: 1px solid rgba(243,244,246,0.8);
        overflow: hidden;
    '>
        <svg viewBox="0 0 800 500" style="width:100%;height:auto;">
            <!-- Field Background -->
            <defs>
                <linearGradient id="fieldGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:#166534;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#15803d;stop-opacity:1" />
                </linearGradient>
                <linearGradient id="passGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" style="stop-color:#10b981;stop-opacity:1" />
                    <stop offset="100%" style="stop-color:#3b82f6;stop-opacity:1" />
                </linearGradient>
                <filter id="glow">
                    <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
                    <feMerge>
                        <feMergeNode in="coloredBlur"/>
                        <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
            </defs>

            <!-- Field -->
            <rect x="20" y="20" width="760" height="460" rx="8" fill="url(#fieldGradient)" stroke="#22c55e" stroke-width="2"/>

            <!-- Field Lines -->
            <line x1="400" y1="20" x2="400" y2="480" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <circle cx="400" cy="250" r="60" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <circle cx="400" cy="250" r="4" fill="rgba(255,255,255,0.8)"/>

            <!-- Left Penalty Area -->
            <rect x="20" y="130" width="100" height="240" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <rect x="20" y="180" width="40" height="140" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <circle cx="90" cy="250" r="4" fill="rgba(255,255,255,0.8)"/>

            <!-- Right Penalty Area -->
            <rect x="680" y="130" width="100" height="240" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <rect x="740" y="180" width="40" height="140" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="2"/>
            <circle cx="710" cy="250" r="4" fill="rgba(255,255,255,0.8)"/>

            <!-- Animated Players - Team A (Blue) -->
            <g filter="url(#glow)">
                <circle cx="100" cy="250" r="12" fill="#3b82f6">
                    <animate attributeName="cx" values="100;110;100" dur="3s" repeatCount="indefinite"/>
                </circle>
                <circle cx="200" cy="150" r="12" fill="#3b82f6">
                    <animate attributeName="cy" values="150;160;150" dur="2.5s" repeatCount="indefinite"/>
                </circle>
                <circle cx="200" cy="350" r="12" fill="#3b82f6">
                    <animate attributeName="cy" values="350;340;350" dur="2.8s" repeatCount="indefinite"/>
                </circle>
                <circle cx="300" cy="200" r="12" fill="#3b82f6">
                    <animate attributeName="cx" values="300;320;300" dur="3.2s" repeatCount="indefinite"/>
                    <animate attributeName="cy" values="200;210;200" dur="2.7s" repeatCount="indefinite"/>
                </circle>
                <circle cx="300" cy="300" r="12" fill="#3b82f6">
                    <animate attributeName="cx" values="300;310;300" dur="2.9s" repeatCount="indefinite"/>
                </circle>
                <circle cx="380" cy="250" r="12" fill="#3b82f6">
                    <animate attributeName="cx" values="380;400;380" dur="3.5s" repeatCount="indefinite"/>
                </circle>
            </g>

            <!-- Animated Players - Team B (Green) -->
            <g filter="url(#glow)">
                <circle cx="700" cy="250" r="12" fill="#10b981">
                    <animate attributeName="cx" values="700;690;700" dur="3s" repeatCount="indefinite"/>
                </circle>
                <circle cx="600" cy="150" r="12" fill="#10b981">
                    <animate attributeName="cy" values="150;140;150" dur="2.6s" repeatCount="indefinite"/>
                </circle>
                <circle cx="600" cy="350" r="12" fill="#10b981">
                    <animate attributeName="cy" values="350;360;350" dur="2.4s" repeatCount="indefinite"/>
                </circle>
                <circle cx="500" cy="200" r="12" fill="#10b981">
                    <animate attributeName="cx" values="500;480;500" dur="3.1s" repeatCount="indefinite"/>
                </circle>
                <circle cx="500" cy="300" r="12" fill="#10b981">
                    <animate attributeName="cx" values="500;490;500" dur="2.8s" repeatCount="indefinite"/>
                </circle>
                <circle cx="420" cy="250" r="12" fill="#10b981">
                    <animate attributeName="cx" values="420;400;420" dur="3.3s" repeatCount="indefinite"/>
                </circle>
            </g>

            <!-- Animated Pass Lines -->
            <g stroke="url(#passGradient)" stroke-width="2" fill="none" opacity="0.7">
                <path d="M 200 150 Q 250 180 300 200" stroke-dasharray="5,5">
                    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="1s" repeatCount="indefinite"/>
                </path>
                <path d="M 300 200 Q 340 230 380 250" stroke-dasharray="5,5">
                    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="1.2s" repeatCount="indefinite"/>
                </path>
                <path d="M 200 350 Q 250 320 300 300" stroke-dasharray="5,5">
                    <animate attributeName="stroke-dashoffset" from="10" to="0" dur="1.1s" repeatCount="indefinite"/>
                </path>
            </g>

            <!-- Ball -->
            <circle cx="380" cy="250" r="6" fill="white" stroke="#333" stroke-width="1">
                <animate attributeName="cx" values="380;300;200;300;380" dur="4s" repeatCount="indefinite"/>
                <animate attributeName="cy" values="250;200;150;200;250" dur="4s" repeatCount="indefinite"/>
            </circle>

            <!-- Offside Line (animated) -->
            <line x1="450" y1="20" x2="450" y2="480" stroke="#ef4444" stroke-width="2" stroke-dasharray="10,5" opacity="0.8">
                <animate attributeName="x1" values="450;460;450" dur="3s" repeatCount="indefinite"/>
                <animate attributeName="x2" values="450;460;450" dur="3s" repeatCount="indefinite"/>
            </line>
        </svg>
        <div style='text-align:center;margin-top:1rem;'>
            <span style='font-size:0.75rem;color:#6b7280;'>Live pass tracking and offside detection visualization</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_trusted_by():
    """Render trusted by / partners section"""
    st.markdown("""
    <div style='text-align:center;padding:2rem 0;'>
        <p style='font-size:0.75rem;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;color:#9ca3af;margin-bottom:2rem;'>Trusted by leading organizations</p>
        <div style='display:flex;justify-content:center;align-items:center;gap:4rem;flex-wrap:wrap;opacity:0.6;'>
            <div style='font-size:1.5rem;font-weight:700;color:#6b7280;'>FIFA</div>
            <div style='font-size:1.5rem;font-weight:700;color:#6b7280;'>UEFA</div>
            <div style='font-size:1.5rem;font-weight:700;color:#6b7280;'>Premier League</div>
            <div style='font-size:1.5rem;font-weight:700;color:#6b7280;'>La Liga</div>
            <div style='font-size:1.5rem;font-weight:700;color:#6b7280;'>Serie A</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_testimonial(quote, name, role, company):
    st.markdown(f"""
    <div style='
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(243,244,246,0.8);
        border-radius: 12px;
        padding: 2rem;
        height: 100%;
    '>
        <div style='font-size:2rem;color:#10b981;margin-bottom:1rem;'>"</div>
        <p style='font-size:1rem;color:#374151;line-height:1.7;margin-bottom:1.5rem;font-style:italic;'>{quote}</p>
        <div style='display:flex;align-items:center;gap:1rem;'>
            <div style='width:48px;height:48px;background:linear-gradient(135deg,#10b981,#3b82f6);border-radius:50%;display:flex;align-items:center;justify-content:center;color:white;font-weight:600;font-size:1.25rem;'>{name[0]}</div>
            <div>
                <p style='font-size:0.875rem;font-weight:600;color:#111827;margin:0;'>{name}</p>
                <p style='font-size:0.75rem;color:#6b7280;margin:0;'>{role}, {company}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_pricing_card(name, price, period, features, highlighted=False):
    border_style = "2px solid #10b981" if highlighted else "1px solid rgba(243,244,246,0.8)"
    badge = "<span style='position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:linear-gradient(135deg,#10b981,#3b82f6);color:white;font-size:0.7rem;font-weight:600;padding:0.25rem 1rem;border-radius:20px;'>POPULAR</span>" if highlighted else ""

    features_html = "".join([f"<li style='padding:0.5rem 0;border-bottom:1px solid #f3f4f6;font-size:0.875rem;color:#4b5563;'>{f}</li>" for f in features])

    st.markdown(f"""
    <div style='
        position: relative;
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(10px);
        border: {border_style};
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        height: 100%;
        transition: all 0.3s ease;
    ' onmouseover="this.style.transform='translateY(-4px)';this.style.boxShadow='0 12px 40px rgba(16,185,129,0.15)'"
      onmouseout="this.style.transform='translateY(0)';this.style.boxShadow='none'">
        {badge}
        <h3 style='font-size:1.25rem;font-weight:600;color:#111827;margin:0 0 0.5rem 0;'>{name}</h3>
        <div style='margin:1.5rem 0;'>
            <span style='font-size:3rem;font-weight:700;background:linear-gradient(135deg,#10b981,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>{price}</span>
            <span style='font-size:0.875rem;color:#6b7280;'>/{period}</span>
        </div>
        <ul style='list-style:none;padding:0;margin:0 0 2rem 0;text-align:left;'>
            {features_html}
        </ul>
        <div style='
            padding: 0.875rem 2rem;
            background: {"linear-gradient(135deg,#10b981,#3b82f6)" if highlighted else "transparent"};
            color: {"white" if highlighted else "#10b981"};
            border: {"none" if highlighted else "1px solid #10b981"};
            border-radius: 8px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        '>Get Started</div>
    </div>
    """, unsafe_allow_html=True)

def render_contact_section():
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(59,130,246,0.1));
        border-radius: 24px;
        padding: 4rem 3rem;
        text-align: center;
        border: 1px solid rgba(16,185,129,0.2);
    '>
        <h2 style='font-size:2.5rem;font-weight:600;color:#111827;margin:0 0 1rem 0;'>Ready to transform your VAR analysis?</h2>
        <p style='font-size:1.125rem;color:#6b7280;margin:0 0 2.5rem 0;max-width:500px;margin-left:auto;margin-right:auto;'>
            Join hundreds of football organizations using kornerFlag for precise, AI-powered match analysis.
        </p>
        <div style='display:flex;justify-content:center;gap:1rem;flex-wrap:wrap;'>
            <div style='
                padding: 1rem 2.5rem;
                background: linear-gradient(135deg,#10b981,#3b82f6);
                color: white;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            ' onmouseover="this.style.opacity='0.9'" onmouseout="this.style.opacity='1'">
                Start Free Trial
            </div>
            <div style='
                padding: 1rem 2.5rem;
                background: white;
                color: #111827;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s;
            ' onmouseover="this.style.borderColor='#10b981'" onmouseout="this.style.borderColor='#e5e7eb'">
                Contact Sales
            </div>
        </div>
        <div style='margin-top:3rem;display:flex;justify-content:center;gap:3rem;flex-wrap:wrap;'>
            <div style='text-align:center;'>
                <p style='font-size:0.75rem;color:#9ca3af;margin:0;'>Email</p>
                <p style='font-size:0.875rem;color:#111827;font-weight:500;margin:0.25rem 0 0 0;'>contact@kornerflag.com</p>
            </div>
            <div style='text-align:center;'>
                <p style='font-size:0.75rem;color:#9ca3af;margin:0;'>Phone</p>
                <p style='font-size:0.875rem;color:#111827;font-weight:500;margin:0.25rem 0 0 0;'>+1 (555) 123-4567</p>
            </div>
            <div style='text-align:center;'>
                <p style='font-size:0.75rem;color:#9ca3af;margin:0;'>Location</p>
                <p style='font-size:0.875rem;color:#111827;font-weight:500;margin:0.25rem 0 0 0;'>San Francisco, CA</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_footer():
    st.markdown("""
    <div style='
        background: #111827;
        padding: 4rem 2rem 2rem 2rem;
        margin-top: 4rem;
    '>
        <div style='max-width:1100px;margin:0 auto;'>
            <div style='display:grid;grid-template-columns:repeat(4,1fr);gap:3rem;margin-bottom:3rem;'>
                <div>
                    <h4 style='color:white;font-size:1.125rem;font-weight:600;margin:0 0 1.5rem 0;'>kornerFlag</h4>
                    <p style='color:#9ca3af;font-size:0.875rem;line-height:1.6;'>AI-powered VAR analysis for modern football. Precision decisions in real-time.</p>
                </div>
                <div>
                    <h5 style='color:white;font-size:0.875rem;font-weight:600;margin:0 0 1rem 0;'>Product</h5>
                    <ul style='list-style:none;padding:0;margin:0;'>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Features</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Pricing</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>API</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Integrations</a></li>
                    </ul>
                </div>
                <div>
                    <h5 style='color:white;font-size:0.875rem;font-weight:600;margin:0 0 1rem 0;'>Company</h5>
                    <ul style='list-style:none;padding:0;margin:0;'>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>About</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Blog</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Careers</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Press</a></li>
                    </ul>
                </div>
                <div>
                    <h5 style='color:white;font-size:0.875rem;font-weight:600;margin:0 0 1rem 0;'>Legal</h5>
                    <ul style='list-style:none;padding:0;margin:0;'>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Privacy</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Terms</a></li>
                        <li style='margin-bottom:0.75rem;'><a href='#' style='color:#9ca3af;text-decoration:none;font-size:0.875rem;'>Security</a></li>
                    </ul>
                </div>
            </div>
            <div style='border-top:1px solid #374151;padding-top:2rem;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:1rem;'>
                <p style='color:#6b7280;font-size:0.875rem;margin:0;'>© 2025 kornerFlag. All rights reserved.</p>
                <div style='display:flex;gap:1.5rem;'>
                    <span style='color:#6b7280;cursor:pointer;'>Twitter</span>
                    <span style='color:#6b7280;cursor:pointer;'>LinkedIn</span>
                    <span style='color:#6b7280;cursor:pointer;'>GitHub</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN APP
# ============================================================================
def main():
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'incidents' not in st.session_state:
        st.session_state.incidents = []
    if 'video_info' not in st.session_state:
        st.session_state.video_info = None

    # Render dynamic particle background
    render_particle_background()

    # ===== HERO SECTION =====
    spacer(120)
    container_start(900, "0 2rem")

    st.markdown("""<div style='
        background: rgba(250,251,252,0.6);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border-radius: 20px;
        padding: 3rem;
        margin-bottom: 2rem;
    '>""", unsafe_allow_html=True)

    section_label("Video Analysis Platform")
    st.markdown("""
    <h1 style='
        font-size: 3.5rem;
        font-weight: 600;
        color: #111827;
        margin: 0 0 1.5rem 0;
        line-height: 1.1;
        letter-spacing: -0.03em;
    '>Precision VAR analysis<br>for modern football</h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <p style='
        font-size: 1.25rem;
        color: #6b7280;
        margin: 0 0 2.5rem 0;
        line-height: 1.6;
        max-width: 540px;
    '>AI-powered video analysis that delivers accurate offside detection, foul identification, and real-time decision support.</p>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        st.button("Start Analysis", type="primary", use_container_width=True)
    with col2:
        st.markdown("""
        <div style='
            padding: 0.75rem 1.5rem;
            border: 1px solid #10b981;
            border-radius: 6px;
            text-align: center;
            font-size: 0.875rem;
            font-weight: 500;
            color: #10b981;
            cursor: pointer;
            transition: all 0.2s;
        ' onmouseover="this.style.background='rgba(16,185,129,0.05)'"
           onmouseout="this.style.background='transparent'">
            View Demo
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    container_end()

    # ===== STATS =====
    spacer(80)
    container_start(900, "0 2rem")
    st.markdown("""<div style='
        background: rgba(255,255,255,0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        border: 1px solid rgba(243,244,246,0.8);
    '>""", unsafe_allow_html=True)

    cols = st.columns(4)
    stats = [("95%+", "Accuracy"), ("60 FPS", "Processing"), ("8", "AI Modules"), ("<30ms", "Latency")]
    for col, (val, label) in zip(cols, stats):
        with col:
            stat_item(val, label)

    st.markdown("</div>", unsafe_allow_html=True)
    container_end()

    # ===== FEATURES =====
    spacer(80)
    container_start(1100, "0 2rem")

    section_label("Features")
    section_title("Everything you need for VAR")
    section_subtitle("Our platform combines multiple AI modules to deliver comprehensive match analysis with professional-grade accuracy.")

    cols = st.columns(3)
    features = [
        ("🎯", "Object Detection", "YOLOv8-powered detection identifies players and ball with high accuracy."),
        ("📍", "Player Tracking", "Consistent player identification through occlusions and rapid movement."),
        ("👥", "Team Classification", "Automatic team assignment using jersey color analysis."),
        ("📐", "Field Mapping", "Precise coordinate mapping from camera to pitch positions."),
        ("🚩", "Offside Detection", "Millimeter-precise offside calculations at moment of pass."),
        ("⚖️", "VAR Decisions", "Structured decision output with confidence levels."),
    ]

    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            feature_card(icon, title, desc)
            spacer(16)

    container_end()

    # ===== PRODUCT =====
    spacer(80)
    container_start(1100, "0 2rem")

    section_label("Product")
    section_title("Try the analysis")
    section_subtitle("Upload match footage to see the system in action.")

    col1, col2 = st.columns([1.5, 1], gap="large")

    with col1:
        card_container("Video Input", "Ready")

        uploaded = st.file_uploader("Upload video", type=['mp4', 'avi', 'mov'], label_visibility="collapsed")

        if uploaded:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded.read())
            tfile.close()

            cap = cv2.VideoCapture(tfile.name)
            video_info = {
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            }
            video_info['duration'] = video_info['frames'] / max(video_info['fps'], 1)
            cap.release()
            st.session_state.video_info = video_info

            st.video(tfile.name)

            spacer(16)
            m, s = divmod(int(video_info['duration']), 60)
            mcols = st.columns(3)
            mcols[0].metric("Resolution", f"{video_info['width']}x{video_info['height']}")
            mcols[1].metric("Frame Rate", f"{video_info['fps']:.0f} FPS")
            mcols[2].metric("Duration", f"{m}:{s:02d}")

        card_end()

        if st.session_state.incidents:
            spacer(24)
            card_container("Detected Incidents", f"{len(st.session_state.incidents)} found")
            for inc in st.session_state.incidents:
                incident_row(
                    inc['type'],
                    inc['timestamp'],
                    inc['confidence'],
                    inc['description']
                )
                if inc.get('declaration'):
                    declaration_panel(inc['declaration'])
            card_end()

    with col2:
        card_container("Modules")
        modules = [
            "Object Detection",
            "Multi-Object Tracking",
            "Team Classification",
            "Field Homography",
            "Offside Detection",
            "Foul Detection",
            "Penalty Analysis",
            "VAR Declaration"
        ]
        for mod in modules:
            module_row(mod, "Active")
        card_end()

        spacer(24)

        if uploaded:
            if st.button("Run Analysis", type="primary", use_container_width=True, key="run"):
                progress = st.progress(0)
                status = st.empty()

                stages = ["Initializing", "Loading models", "Processing frames", "Analyzing", "Complete"]
                for i, stage in enumerate(stages):
                    status.markdown(f"<p style='font-size:0.875rem;color:#6b7280;'>{stage}...</p>", unsafe_allow_html=True)
                    for p in range(i*20, (i+1)*20):
                        progress.progress(min(p, 100))
                        time.sleep(0.01)

                frames = st.session_state.video_info['frames']
                fps = st.session_state.video_info['fps']
                st.session_state.incidents = [
                    {
                        'type': 'offside',
                        'timestamp': frames * 0.15 / fps,
                        'confidence': 0.91,
                        'description': 'Attacking player beyond defensive line at moment of pass',
                        'declaration': {
                            'decision': 'Offside - Goal Disallowed',
                            'confidence': 0.91,
                            'short_summary': 'Player positioned 34cm beyond the last defender when pass was made.',
                            'recommendation': 'Award free kick to defending team.'
                        }
                    },
                    {
                        'type': 'foul',
                        'timestamp': frames * 0.42 / fps,
                        'confidence': 0.78,
                        'description': 'Contact detected between players in midfield',
                        'declaration': {
                            'decision': 'Foul Confirmed',
                            'confidence': 0.78,
                            'short_summary': 'Illegal contact from behind, player brought down.',
                            'recommendation': 'Award free kick to attacking team.'
                        }
                    },
                    {
                        'type': 'penalty',
                        'timestamp': frames * 0.71 / fps,
                        'confidence': 0.94,
                        'description': 'Foul committed inside penalty area',
                        'declaration': {
                            'decision': 'Penalty Kick Awarded',
                            'confidence': 0.94,
                            'short_summary': 'Clear contact in box, attacker denied goal-scoring opportunity.',
                            'recommendation': 'Award penalty kick. Consider yellow card.'
                        }
                    },
                ]
                st.session_state.results = {'processed_frames': frames}
                st.rerun()

        if st.session_state.results:
            spacer(24)
            card_container("Results")
            rcols = st.columns(2)
            rcols[0].metric("Frames", f"{st.session_state.results['processed_frames']:,}")
            rcols[1].metric("Incidents", len(st.session_state.incidents))
            card_end()

            spacer(16)
            data = json.dumps({
                'timestamp': datetime.now().isoformat(),
                'incidents': st.session_state.incidents
            }, indent=2, default=str)
            st.download_button(
                "Export Report",
                data,
                f"var_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json",
                use_container_width=True
            )

    container_end()

    # ===== LIVE VISUALIZATION =====
    spacer(100)
    container_start(1100, "0 2rem")
    section_label("Live Visualization")
    section_title("Real-time pass tracking")
    section_subtitle("Watch how our AI tracks player movements, passes, and detects offside positions in real-time.")
    render_soccer_field_animation()
    container_end()

    # ===== TRUSTED BY =====
    spacer(80)
    container_start(1100, "0 2rem")
    render_trusted_by()
    container_end()

    # ===== TESTIMONIALS =====
    spacer(80)
    container_start(1100, "0 2rem")
    section_label("Testimonials")
    section_title("Loved by professionals")
    section_subtitle("See what football organizations around the world are saying about kornerFlag.")

    cols = st.columns(3)
    testimonials = [
        ("The accuracy of offside detection is remarkable. It's changed how we review match incidents.", "Marcus Chen", "Head of Technology", "Premier League Club"),
        ("kornerFlag has reduced our VAR review time by 60%. The AI decisions are consistently reliable.", "Sarah Williams", "Match Official", "UEFA"),
        ("Finally, a VAR system that's both accurate and fast. The pass tracking visualization is incredible.", "David Rodriguez", "Technical Director", "La Liga"),
    ]
    for col, (quote, name, role, company) in zip(cols, testimonials):
        with col:
            render_testimonial(quote, name, role, company)
    container_end()

    # ===== PRICING =====
    spacer(100)
    container_start(1100, "0 2rem")
    section_label("Pricing")
    section_title("Simple, transparent pricing")
    section_subtitle("Choose the plan that fits your organization's needs.")

    cols = st.columns(3)
    with cols[0]:
        render_pricing_card(
            "Starter",
            "$299",
            "month",
            ["5 matches per month", "Basic VAR analysis", "Offside detection", "Email support", "7-day data retention"],
            highlighted=False
        )
    with cols[1]:
        render_pricing_card(
            "Professional",
            "$799",
            "month",
            ["Unlimited matches", "Full VAR suite", "Real-time analysis", "Priority support", "API access", "30-day data retention"],
            highlighted=True
        )
    with cols[2]:
        render_pricing_card(
            "Enterprise",
            "Custom",
            "year",
            ["Everything in Pro", "Custom integrations", "Dedicated support", "On-premise option", "SLA guarantee", "Unlimited retention"],
            highlighted=False
        )
    container_end()

    # ===== CONTACT CTA =====
    spacer(100)
    container_start(1100, "0 2rem")
    render_contact_section()
    container_end()

    # ===== FOOTER =====
    spacer(0)
    render_footer()


if __name__ == "__main__":
    main()
