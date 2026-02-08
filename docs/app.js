// ============================================================================
// KORNERFLAG - INTERACTIVE DEMO
// Theme-aware particle system with toggle and system preference detection
// ============================================================================

// ============================================================================
// THEME TOGGLE
// ============================================================================
(function initTheme() {
    const themeToggle = document.getElementById('themeToggle');
    const root = document.documentElement;

    // Check for saved theme preference or use system preference
    function getPreferredTheme() {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    // Apply theme
    function setTheme(theme) {
        root.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);

        // Dispatch custom event for other components (like particles)
        window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
    }

    // Initialize theme
    setTheme(getPreferredTheme());

    // Toggle button click
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = root.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            setTheme(newTheme);
        });
    }

    // Listen for system preference changes (only if no manual preference saved)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
})();

// ============================================================================
// PARTICLE NETWORK BACKGROUND
// Reads colors from CSS custom properties for theme support
// ============================================================================
(function initParticles() {
    const canvas = document.getElementById('particleCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let particles = [];
    let animationId;
    let mouseX = 0;
    let mouseY = 0;

    // Get colors from CSS custom properties (theme-aware)
    function getThemeColors() {
        const styles = getComputedStyle(document.documentElement);
        return {
            particleColors: [
                styles.getPropertyValue('--particle-color-1').trim() || 'rgba(20, 184, 166, 0.6)',
                styles.getPropertyValue('--particle-color-2').trim() || 'rgba(6, 182, 212, 0.6)',
                styles.getPropertyValue('--particle-color-3').trim() || 'rgba(59, 130, 246, 0.6)'
            ],
            lineOpacity: parseFloat(styles.getPropertyValue('--particle-line-opacity').trim()) || 0.12
        };
    }

    let themeColors = getThemeColors();

    const config = {
        particleCount: 100,
        particleSize: 2.5,
        lineDistance: 180,
        speed: 0.4,
        mouseInfluenceRadius: 150,
        mouseForce: 0.03
    };

    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function createParticles() {
        particles = [];
        for (let i = 0; i < config.particleCount; i++) {
            const colorIndex = Math.floor(Math.random() * themeColors.particleColors.length);
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * config.speed,
                vy: (Math.random() - 0.5) * config.speed,
                size: Math.random() * config.particleSize + 1,
                color: themeColors.particleColors[colorIndex],
                colorIndex: colorIndex,
                pulseOffset: Math.random() * Math.PI * 2
            });
        }
    }

    function drawParticle(p, time) {
        // Subtle pulse effect
        const pulse = 1 + Math.sin(time * 0.002 + p.pulseOffset) * 0.2;
        const size = p.size * pulse;

        ctx.beginPath();
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.fill();
    }

    function drawLine(p1, p2, distance) {
        const opacity = (1 - (distance / config.lineDistance)) * themeColors.lineOpacity;

        // Create gradient line between particles
        const gradient = ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);

        // Extract base colors and apply dynamic opacity
        const color1 = themeColors.particleColors[p1.colorIndex].replace(/[\d.]+\)$/, opacity + ')');
        const color2 = themeColors.particleColors[p2.colorIndex].replace(/[\d.]+\)$/, opacity + ')');

        gradient.addColorStop(0, color1);
        gradient.addColorStop(1, color2);

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.strokeStyle = gradient;
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    function updateParticle(p) {
        // Mouse interaction - particles gently move away from cursor
        const dx = p.x - mouseX;
        const dy = p.y - mouseY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < config.mouseInfluenceRadius && distance > 0) {
            const force = (config.mouseInfluenceRadius - distance) / config.mouseInfluenceRadius;
            p.vx += (dx / distance) * force * config.mouseForce;
            p.vy += (dy / distance) * force * config.mouseForce;
        }

        // Apply velocity with gentle damping
        p.vx *= 0.99;
        p.vy *= 0.99;

        // Ensure minimum speed
        const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
        if (speed < config.speed * 0.5) {
            const angle = Math.random() * Math.PI * 2;
            p.vx += Math.cos(angle) * 0.01;
            p.vy += Math.sin(angle) * 0.01;
        }

        // Cap maximum speed
        const maxSpeed = 1.5;
        if (speed > maxSpeed) {
            p.vx = (p.vx / speed) * maxSpeed;
            p.vy = (p.vy / speed) * maxSpeed;
        }

        p.x += p.vx;
        p.y += p.vy;

        // Wrap around edges
        if (p.x < -10) p.x = canvas.width + 10;
        if (p.x > canvas.width + 10) p.x = -10;
        if (p.y < -10) p.y = canvas.height + 10;
        if (p.y > canvas.height + 10) p.y = -10;
    }

    function getDistance(p1, p2) {
        return Math.sqrt(Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2));
    }

    function animate(time) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update and draw particles
        particles.forEach(function(p) {
            updateParticle(p);
            drawParticle(p, time);
        });

        // Draw connection lines
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

    // Mouse tracking
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    // Handle theme changes
    function handleThemeChange() {
        themeColors = getThemeColors();
        // Update particle colors
        particles.forEach((p, i) => {
            p.color = themeColors.particleColors[p.colorIndex];
        });
    }

    // Listen for theme changes (from toggle or system)
    window.addEventListener('themechange', handleThemeChange);
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', handleThemeChange);
    }

    // Initialize
    resize();
    createParticles();
    animate(0);

    // Handle resize
    window.addEventListener('resize', function() {
        resize();
        createParticles();
    });
})();

// ============================================================================
// NAVBAR SCROLL EFFECT
// ============================================================================
(function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;

    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });
})();

// ============================================================================
// SMOOTH SCROLL FOR NAVIGATION
// ============================================================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 0;
            const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 20;

            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// ============================================================================
// VIDEO UPLOAD & DEMO FUNCTIONALITY
// ============================================================================
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const videoInput = document.getElementById('videoInput');
    const videoPreview = document.getElementById('videoPreview');
    const previewVideo = document.getElementById('previewVideo');
    const runAnalysisBtn = document.getElementById('runAnalysis');
    const progressContainer = document.getElementById('progressContainer');
    const progressFill = document.getElementById('progressFill');
    const progressText = document.getElementById('progressText');
    const resultsCard = document.getElementById('resultsCard');
    const incidentsCard = document.getElementById('incidentsCard');
    const incidentsList = document.getElementById('incidentsList');
    const exportBtn = document.getElementById('exportBtn');

    if (!uploadArea) return;

    let videoInfo = null;
    let analysisResults = null;

    // Upload area click
    uploadArea.addEventListener('click', function() {
        videoInput.click();
    });

    // Drag and drop
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function() {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleVideoFile(files[0]);
        }
    });

    // File input change
    videoInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleVideoFile(e.target.files[0]);
        }
    });

    function handleVideoFile(file) {
        if (!file.type.startsWith('video/')) {
            alert('Please upload a video file');
            return;
        }

        const url = URL.createObjectURL(file);
        previewVideo.src = url;

        previewVideo.onloadedmetadata = function() {
            videoInfo = {
                width: previewVideo.videoWidth,
                height: previewVideo.videoHeight,
                duration: previewVideo.duration,
                frames: Math.floor(previewVideo.duration * 30)
            };

            document.getElementById('metricResolution').textContent =
                `${videoInfo.width}x${videoInfo.height}`;

            const mins = Math.floor(videoInfo.duration / 60);
            const secs = Math.floor(videoInfo.duration % 60);
            document.getElementById('metricDuration').textContent =
                `${mins}:${secs.toString().padStart(2, '0')}`;

            uploadArea.style.display = 'none';
            videoPreview.style.display = 'block';
            runAnalysisBtn.style.display = 'block';
        };
    }

    // Run Analysis
    runAnalysisBtn.addEventListener('click', function() {
        runAnalysisBtn.style.display = 'none';
        progressContainer.style.display = 'block';

        const stages = [
            'Initializing AI modules...',
            'Loading YOLOv8 models...',
            'Processing video frames...',
            'Detecting players & ball...',
            'Calculating field homography...',
            'Analyzing incidents...',
            'Generating VAR report...',
            'Analysis complete!'
        ];

        let currentStage = 0;
        let progress = 0;

        const interval = setInterval(function() {
            progress += 1.5;
            progressFill.style.width = Math.min(progress, 100) + '%';

            const stageIndex = Math.floor(progress / (100 / stages.length));
            if (stageIndex !== currentStage && stageIndex < stages.length) {
                currentStage = stageIndex;
                progressText.textContent = stages[currentStage];
            }

            if (progress >= 100) {
                clearInterval(interval);
                setTimeout(showResults, 500);
            }
        }, 40);
    });

    function showResults() {
        progressContainer.style.display = 'none';
        resultsCard.style.display = 'block';
        incidentsCard.style.display = 'block';

        // Generate mock incidents based on video duration
        const incidents = [
            {
                type: 'offside',
                timestamp: videoInfo.duration * 0.15,
                confidence: 0.91,
                description: 'Attacking player beyond defensive line at moment of pass',
                declaration: {
                    decision: 'Offside - Goal Disallowed',
                    confidence: 0.91,
                    summary: 'Player positioned 34cm beyond the last defender when pass was made.'
                }
            },
            {
                type: 'foul',
                timestamp: videoInfo.duration * 0.42,
                confidence: 0.78,
                description: 'Contact detected between players in midfield',
                declaration: {
                    decision: 'Foul Confirmed',
                    confidence: 0.78,
                    summary: 'Illegal contact from behind, player brought down.'
                }
            },
            {
                type: 'penalty',
                timestamp: videoInfo.duration * 0.71,
                confidence: 0.94,
                description: 'Foul committed inside penalty area',
                declaration: {
                    decision: 'Penalty Kick Awarded',
                    confidence: 0.94,
                    summary: 'Clear contact in box, attacker denied goal-scoring opportunity.'
                }
            }
        ];

        analysisResults = {
            frames: videoInfo.frames,
            incidents: incidents
        };

        document.getElementById('resultFrames').textContent = videoInfo.frames.toLocaleString();
        document.getElementById('resultIncidents').textContent = incidents.length;
        document.getElementById('incidentCount').textContent = incidents.length + ' found';

        // Render incidents with animation
        incidentsList.innerHTML = '';
        incidents.forEach((inc, index) => {
            setTimeout(() => {
                incidentsList.innerHTML += renderIncident(inc);
            }, index * 200);
        });
    }

    function renderIncident(incident) {
        const mins = Math.floor(incident.timestamp / 60);
        const secs = Math.floor(incident.timestamp % 60);
        const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        const confPercent = Math.round(incident.confidence * 100);

        return `
            <div class="incident-row" style="animation: fadeInUp 0.4s ease forwards;">
                <div class="incident-header">
                    <div class="incident-meta">
                        <span class="incident-type ${incident.type}">${incident.type}</span>
                        <span class="incident-time">${timeStr}</span>
                    </div>
                    <span class="incident-confidence">${confPercent}%</span>
                </div>
                <p class="incident-description">${incident.description}</p>
                ${incident.declaration ? `
                    <div class="declaration-panel">
                        <span class="declaration-badge">VAR Decision</span>
                        <h4 class="declaration-decision">${incident.declaration.decision}</h4>
                        <p class="declaration-summary">${incident.declaration.summary}</p>
                        <div class="declaration-footer">
                            <span>Confidence</span>
                            <span>${Math.round(incident.declaration.confidence * 100)}%</span>
                        </div>
                    </div>
                ` : ''}
            </div>
        `;
    }

    // Export Report
    exportBtn.addEventListener('click', function() {
        if (!analysisResults) return;

        const report = {
            metadata: {
                generated: new Date().toISOString(),
                platform: 'kornerFlag VAR Analysis',
                version: '2.0'
            },
            video: {
                resolution: `${videoInfo.width}x${videoInfo.height}`,
                duration: videoInfo.duration,
                frames: videoInfo.frames,
                fps: 30
            },
            analysis: {
                totalIncidents: analysisResults.incidents.length,
                incidents: analysisResults.incidents.map(inc => ({
                    type: inc.type,
                    timestamp: inc.timestamp,
                    confidence: inc.confidence,
                    description: inc.description,
                    decision: inc.declaration?.decision || null,
                    summary: inc.declaration?.summary || null
                }))
            }
        };

        const blob = new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kornerflag_var_report_${new Date().toISOString().slice(0,19).replace(/[:-]/g, '')}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });
});

// ============================================================================
// INTERSECTION OBSERVER FOR SCROLL ANIMATIONS
// ============================================================================
(function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements that should animate on scroll
    document.querySelectorAll('.feature-card, .testimonial-card, .pricing-card, .stat-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Add CSS for animated state
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }

        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    `;
    document.head.appendChild(style);
})();

// ============================================================================
// BUTTON RIPPLE EFFECT
// ============================================================================
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
            left: ${x}px;
            top: ${y}px;
            width: 100px;
            height: 100px;
            margin-left: -50px;
            margin-top: -50px;
        `;

        this.style.position = 'relative';
        this.style.overflow = 'hidden';
        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});

// Add ripple animation
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// ============================================================================
// TYPING EFFECT FOR HERO (Optional enhancement)
// ============================================================================
(function initTypingEffect() {
    const heroTitle = document.querySelector('.hero-title');
    if (!heroTitle) return;

    // Add cursor style
    const style = document.createElement('style');
    style.textContent = `
        .typing-cursor {
            display: inline-block;
            width: 3px;
            height: 1em;
            background: var(--gradient-brand);
            margin-left: 2px;
            animation: blink 1s infinite;
            vertical-align: text-bottom;
        }

        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
    `;
    document.head.appendChild(style);
})();

console.log('kornerFlag Demo loaded successfully');
console.log('Theme:', document.documentElement.getAttribute('data-theme') || 'light');
