/**
 * ResumeAI Intelligence Platform v3.0 – Client Application Engine
 * Optimized for high performance, smooth interactivity, and cross-tab synergy.
 */

/* =====================================================================
   GLOBAL APP STATE & SHARED WORKSPACE
   ===================================================================== */
const AppState = {
    activeResumeFile: null,
    activeJobDescription: '',
    activeResumeText: '',
    activeRequiredSkills: '',
    lastAnalysisData: null,
    batchResults: [],
    roadmapChecked: new Set(),
    theme: 'dark'
};

/* =====================================================================
   PRESET DEMO PROFILES (Instant 1-Click Evaluation)
   ===================================================================== */
const DemoProfiles = {
    fullstack: {
        filename: 'alex_chen_senior_fullstack.txt',
        content: `Alex Chen
Senior Full-Stack Engineer | San Francisco, CA | alex.chen@example.com

SUMMARY
Full-Stack Engineer with 6+ years of experience architecting and delivering cloud-native microservices, modern single-page applications, and high-throughput data processing pipelines. Proven track record scaling applications to 2M+ monthly active users on AWS.

CORE SKILLS
Languages: Python, TypeScript, JavaScript, SQL, Go
Frameworks & Libraries: Django, FastAPI, React, Next.js, Node.js, TailwindCSS
Data & Storage: PostgreSQL, Redis, DynamoDB, Elasticsearch
DevOps & Cloud: Docker, Kubernetes, AWS (ECS, Lambda, S3, RDS), Terraform, CI/CD (GitHub Actions)
Architecture: Microservices, REST APIs, GraphQL, Event-Driven Architecture (Kafka)

EXPERIENCE
Staff / Senior Software Engineer | CloudScale Systems | 2021 – Present
- Architected and deployed a multi-tenant telemetry ingestion platform in Go and Python, ingesting 85,000 events/second with sub-20ms p95 latency.
- Led migration of monolithic Django API into modular FastAPI services, reducing server infrastructure costs by 34% on AWS ECS.
- Designed real-time collaboration dashboard using Next.js, TypeScript, and WebSockets, increasing daily active user engagement by 42%.
- Mentored a squad of 7 engineers; instituted comprehensive automated testing (pytest, Jest, Cypress) boosting test coverage from 58% to 92%.

Full-Stack Developer | Nexus Labs | 2018 – 2021
- Developed customer-facing React SPA and Node.js REST API handling $18M in quarterly transactions.
- Automated deployment workflows using Terraform and GitHub Actions, cutting release deployment cycles from 3 hours to 12 minutes.
- Optimized PostgreSQL indexing and query performance, slashing database CPU utilization by 45%.

PROJECTS
OpenTelemetry Cloud Agent: Open-source distributed tracing exporter with 1,200+ GitHub stars. Built with Go, Docker, and Prometheus.
Distributed Job Queue: Fault-tolerant Redis-backed worker pool supporting at-least-once task delivery in Python and TypeScript.

EDUCATION
B.S. in Computer Science | University of California, Berkeley | 2018`,
        jobDescription: `Staff Software Engineer - Cloud Platforms
Location: Remote (US)

About the Role:
We are seeking an experienced Staff/Senior Software Engineer to lead the design and implementation of our next-generation cloud infrastructure and microservices platform.

Key Responsibilities:
- Design, build, and maintain high-throughput backend services and APIs using Python (FastAPI/Django) and Go.
- Drive architecture decisions across cloud deployments on AWS, Docker, Kubernetes, and Terraform.
- Collaborate with frontend teams building modern web interfaces using React, TypeScript, and Next.js.
- Champion engineering best practices, CI/CD pipelines, automated testing, and observable systems.
- Mentor junior and mid-level engineers and conduct architectural reviews.

Qualifications & Requirements:
- 5+ years of software engineering experience in production distributed systems.
- Strong proficiency with Python, TypeScript, and relational databases (PostgreSQL).
- Deep hands-on experience with AWS, containerization (Docker/Kubernetes), and infrastructure as code.
- Demonstrated experience leading technical initiatives and improving developer productivity.
- Excellent communication and collaborative problem-solving skills.`,
        requiredSkills: 'Python, FastAPI, AWS, Docker, Kubernetes, TypeScript, PostgreSQL'
    }
};

/* =====================================================================
   PARTICLES CANVAS ENGINE (High Efficiency & Low Battery Draw)
   ===================================================================== */
(function initParticlesEngine() {
    const canvas = document.getElementById('particles-canvas');
    if (!canvas) return;

    // Honor reduced-motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        canvas.style.display = 'none';
        return;
    }

    const ctx = canvas.getContext('2d');
    let particles = [];
    let animationFrameId = null;
    let isVisible = true;
    let isHeroInView = true;

    let mouse = { x: -9999, y: -9999, active: false };
    window.addEventListener('mousemove', e => {
        mouse.x = e.clientX;
        mouse.y = e.clientY;
        mouse.active = true;
    }, { passive: true });
    window.addEventListener('mouseleave', () => { mouse.active = false; });

    const COLORS = [
        'rgba(0, 242, 254, 0.45)',
        'rgba(99, 102, 241, 0.45)',
        'rgba(168, 85, 247, 0.40)',
        'rgba(16, 185, 129, 0.35)'
    ];

    // Mobile / low power scaling: reduce particles on smaller viewports
    const particleCount = window.innerWidth < 768 ? 24 : 45;

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();

    let resizeTimer;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(resizeCanvas, 150);
    });

    for (let i = 0; i < particleCount; i++) {
        particles.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            r: Math.random() * 1.8 + 0.6,
            vx: (Math.random() - 0.5) * 0.3,
            vy: (Math.random() - 0.5) * 0.3,
            color: COLORS[Math.floor(Math.random() * COLORS.length)]
        });
    }

    const maxDist = 125;
    const maxDistSq = maxDist * maxDist;

    function renderParticles() {
        if (!isVisible || !isHeroInView) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Update & draw particles with magnetic cursor attraction
        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];

            if (mouse.active) {
                const mdx = mouse.x - p.x;
                const mdy = mouse.y - p.y;
                const mdistSq = mdx * mdx + mdy * mdy;
                if (mdistSq < 22500) { // 150px proximity
                    const mdist = Math.sqrt(mdistSq) || 1;
                    const pull = ((150 - mdist) / 150) * 0.08;
                    p.vx += (mdx / mdist) * pull;
                    p.vy += (mdy / mdist) * pull;
                }
            }

            p.vx *= 0.99;
            p.vy *= 0.99;

            p.x += p.vx;
            p.y += p.vy;

            if (p.x < 0) p.x = canvas.width;
            else if (p.x > canvas.width) p.x = 0;
            if (p.y < 0) p.y = canvas.height;
            else if (p.y > canvas.height) p.y = 0;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();
        }

        // Draw distance connections with squared distance check
        for (let i = 0; i < particles.length; i++) {
            const p1 = particles[i];
            for (let j = i + 1; j < particles.length; j++) {
                const p2 = particles[j];
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const distSq = dx * dx + dy * dy;

                if (distSq < maxDistSq) {
                    const alpha = 0.08 * (1 - Math.sqrt(distSq) / maxDist);
                    ctx.beginPath();
                    ctx.moveTo(p1.x, p1.y);
                    ctx.lineTo(p2.x, p2.y);
                    ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }

        animationFrameId = requestAnimationFrame(renderParticles);
    }

    function startAnimation() {
        if (!animationFrameId && isVisible && isHeroInView) {
            animationFrameId = requestAnimationFrame(renderParticles);
        }
    }

    function stopAnimation() {
        if (animationFrameId) {
            cancelAnimationFrame(animationFrameId);
            animationFrameId = null;
        }
    }

    // 1. Pause when tab/window is hidden or minimized
    document.addEventListener('visibilitychange', () => {
        isVisible = document.visibilityState === 'visible';
        if (isVisible) startAnimation();
        else stopAnimation();
    });

    // 2. Pause when scrolled away from Hero area
    const heroEl = document.querySelector('.hero');
    if (heroEl && 'IntersectionObserver' in window) {
        const observer = new IntersectionObserver(entries => {
            isHeroInView = entries[0].isIntersecting;
            if (isHeroInView) startAnimation();
            else stopAnimation();
        }, { threshold: 0.1 });
        observer.observe(heroEl);
    }

    startAnimation();
})();

/* =====================================================================
   THEME MANAGER (Synchronized with localStorage across all pages)
   ===================================================================== */
const ThemeManager = {
    init() {
        const savedTheme = localStorage.getItem('resumeai_theme') || localStorage.getItem('rai_theme') || 'dark';
        this.applyTheme(savedTheme);

        const toggleBtn = document.getElementById('theme-toggle');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                const current = document.documentElement.getAttribute('data-theme');
                this.applyTheme(current === 'dark' ? 'light' : 'dark');
            });
        }
    },
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        AppState.theme = theme;
        localStorage.setItem('resumeai_theme', theme);
        localStorage.setItem('rai_theme', theme); // backward compatibility

        const icon = document.getElementById('theme-icon');
        if (icon) {
            icon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
        }
    }
};

/* =====================================================================
   TOAST NOTIFICATION ENGINE
   ===================================================================== */
const Toast = {
    timer: null,
    show(message, type = 'info') {
        const toast = document.getElementById('toast');
        const icon = document.getElementById('toast-icon');
        const text = document.getElementById('toast-msg');
        if (!toast || !icon || !text) return;

        // Detect OpenAI Quota / 429 error and offer direct 1-click switch to Local Mode
        const isQuota = typeof message === 'string' && (
            message.includes('429') ||
            message.includes('insufficient_quota') ||
            message.includes('credit_balance_exhausted') ||
            message.includes('quota exhausted') ||
            message.includes('no credits remaining')
        );

        if (isQuota) {
            type = 'warning';
            text.innerHTML = `
                <div>
                    <strong style="color:var(--c-amber);"><i class="fas fa-triangle-exclamation"></i> OpenAI Credits Exhausted (429)</strong>
                    <div style="font-size:0.82rem; margin:4px 0 6px;">Your OpenAI key has 0 credits. Run 100% free in Local Mode:</div>
                    <button onclick="switchToLocalAndRun('current')" style="background:linear-gradient(120deg,var(--c-green),var(--c-teal)); color:#fff; border:none; padding:4px 12px; border-radius:6px; font-weight:800; cursor:pointer; font-size:0.78rem;">
                        <i class="fas fa-bolt"></i> Switch to Free Local Mode
                    </button>
                </div>`;
        } else {
            text.textContent = message;
        }

        const iconMap = {
            success: 'fas fa-circle-check',
            error: 'fas fa-circle-xmark',
            warning: 'fas fa-triangle-exclamation',
            info: 'fas fa-circle-info'
        };
        icon.className = iconMap[type] || iconMap.info;
        const duration = isQuota ? 8000 : 4200;
        toast.className = `toast show ${type}`;

        const prog = document.getElementById('toast-progress');
        if (prog) {
            prog.style.transition = 'none';
            prog.style.transform = 'scaleX(1)';
            requestAnimationFrame(() => {
                requestAnimationFrame(() => {
                    prog.style.transition = `transform ${duration}ms linear`;
                    prog.style.transform = 'scaleX(0)';
                });
            });
        }

        clearTimeout(this.timer);
        this.timer = setTimeout(() => {
            toast.className = `toast ${type}`;
        }, duration);
    }
};

function showToast(msg, type = 'info') {
    Toast.show(msg, type);
}

function isQuotaExhaustedError(err) {
    if (!err) return false;
    const str = typeof err === 'string' ? err : JSON.stringify(err);
    return str.includes('429') || str.includes('insufficient_quota') || str.includes('credit_balance_exhausted') || str.includes('quota exhausted') || str.includes('no credits remaining');
}

function renderQuotaErrorCard(errMessage, toolKey = 'single') {
    return `
    <div class="result-block" style="border-color:var(--c-amber); background: color-mix(in srgb, var(--c-amber) 8%, var(--bg-card));">
        <div style="display:flex; align-items:center; gap:10px; color:var(--c-amber); font-weight:800; font-size:1.1rem; margin-bottom:10px;">
            <i class="fas fa-triangle-exclamation"></i> OpenAI API Credits Exhausted (Error 429)
        </div>
        <p style="color:var(--text-1); font-size:0.92rem; margin-bottom:8px; line-height:1.6;">
            Your configured OpenAI API key has ran out of credits (<code>credit_balance_exhausted</code>).
        </p>
        <p style="color:var(--text-2); font-size:0.86rem; margin-bottom:16px; line-height:1.6;">
            <strong>Good news:</strong> You can continue using ResumeAI <strong>100% for free</strong> using <strong>Local Mode</strong>. Local Mode uses deterministic NLP (spaCy &amp; TF-IDF) running right on your machine with <strong>zero API fees</strong>.
        </p>
        <div style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
            <button class="btn-primary" onclick="switchToLocalAndRun('${toolKey}')" style="background:linear-gradient(120deg, var(--c-green), var(--c-teal)); padding:10px 20px; font-size:0.88rem;">
                <i class="fas fa-bolt"></i> Switch to Free Local Mode &amp; Run
            </button>
            <a href="https://platform.openai.com/settings/organization/billing/" target="_blank" rel="noopener" class="btn-ghost" style="text-decoration:none; padding:10px 18px; font-size:0.88rem;">
                <i class="fas fa-credit-card"></i> Add OpenAI Credits <i class="fas fa-arrow-up-right-from-square" style="font-size:0.75rem;"></i>
            </a>
        </div>
    </div>`;
}

function switchToLocalAndRun(toolKey = 'single') {
    const select = document.getElementById('analysis-mode');
    if (select) {
        select.value = 'local';
        select.dispatchEvent(new Event('change'));
    }
    showToast('Switched to Local (Fast & Free) mode! Re-running now…', 'success');

    if (toolKey === 'single') runSingleAnalysis();
    else if (toolKey === 'batch') runBatchAnalysis();
    else if (toolKey === 'improve') runImprovement();
    else if (toolKey === 'cover') generateCoverLetter();
    else if (toolKey === 'career') runCareerPaths();
    else if (toolKey === 'salary') runSalaryEstimate();
}

function escapeHTML(value) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
    return String(value ?? '').replace(/[&<>"']/g, char => map[char]);
}

/* =====================================================================
   ANALYSIS MODE & HEALTH STATUS
   ===================================================================== */
function currentAnalysisMode() {
    const select = document.getElementById('analysis-mode');
    return select ? select.value : 'local';
}

async function updateAIStatus() {
    const statusEl = document.getElementById('ai-status');
    if (!statusEl) return;
    try {
        const res = await fetch('/api/health');
        if (!res.ok) throw new Error(`Status ${res.status}`);
        const data = await res.json();
        statusEl.textContent = data.ai_enabled ? 'AI configured (GPT)' : 'Rule-based local mode';
        statusEl.classList.toggle('ready', Boolean(data.ai_enabled));
        statusEl.classList.toggle('unavailable', !data.ai_enabled);
    } catch {
        statusEl.textContent = 'Status unavailable';
        statusEl.classList.add('unavailable');
    }
}

/* =====================================================================
   TAB NAVIGATION SYSTEM (With Sliding Pill, Category Filter, and Arrows)
   ===================================================================== */
const TabSystem = {
    buttons: [],
    pill: null,
    nav: null,

    init() {
        this.buttons = Array.from(document.querySelectorAll('.tab-btn'));
        this.pill = document.getElementById('tab-pill');
        this.nav = document.querySelector('.tab-nav');
        if (!this.buttons.length || !this.nav) return;

        this.buttons.forEach((btn, idx) => {
            btn.addEventListener('click', () => this.activateTab(btn));
            btn.addEventListener('keydown', e => this.handleKeyNavigation(e, idx));
        });

        // Left / Right Scroll Buttons
        const leftBtn = document.getElementById('tab-nav-left');
        const rightBtn = document.getElementById('tab-nav-right');
        if (leftBtn) leftBtn.addEventListener('click', () => this.nav.scrollBy({ left: -200, behavior: 'smooth' }));
        if (rightBtn) rightBtn.addEventListener('click', () => this.nav.scrollBy({ left: 200, behavior: 'smooth' }));

        // Category Filter Buttons
        const filterBtns = document.querySelectorAll('.cat-filter-btn');
        filterBtns.forEach(fBtn => {
            fBtn.addEventListener('click', () => {
                filterBtns.forEach(b => b.classList.remove('active'));
                fBtn.classList.add('active');
                const cat = fBtn.getAttribute('data-cat');
                this.filterTabsByCategory(cat);
            });
        });

        // Initialize pill on active button
        const activeBtn = document.querySelector('.tab-btn.active') || this.buttons[0];
        setTimeout(() => this.updatePillPosition(activeBtn), 150);

        let resizeDebounce;
        window.addEventListener('resize', () => {
            clearTimeout(resizeDebounce);
            resizeDebounce = setTimeout(() => {
                const curr = document.querySelector('.tab-btn.active');
                if (curr) this.updatePillPosition(curr);
            }, 100);
        });
    },

    activateTab(btn) {
        if (!btn) return;
        this.buttons.forEach(b => {
            b.classList.remove('active');
            b.setAttribute('aria-selected', 'false');
        });
        btn.classList.add('active');
        btn.setAttribute('aria-selected', 'true');
        this.updatePillPosition(btn);

        const tabId = btn.getAttribute('data-tab');
        document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
        const targetPanel = document.getElementById(`${tabId}-panel`);
        if (targetPanel) {
            targetPanel.classList.add('active');
            targetPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Check if shared workspace bar should show sync option for this tab
        checkWorkspaceSyncBar(tabId);
    },

    updatePillPosition(btn) {
        if (!btn || !this.pill || !this.nav) return;
        const navRect = this.nav.getBoundingClientRect();
        const btnRect = btn.getBoundingClientRect();

        requestAnimationFrame(() => {
            this.pill.style.width = `${btnRect.width}px`;
            this.pill.style.left = `${btnRect.left - navRect.left + this.nav.scrollLeft}px`;
        });
    },

    filterTabsByCategory(category) {
        let firstVisible = null;
        this.buttons.forEach(btn => {
            const btnCat = btn.getAttribute('data-category') || 'all';
            const shouldShow = category === 'all' || btnCat === category;
            btn.classList.toggle('hidden-by-filter', !shouldShow);
            if (shouldShow && !firstVisible) firstVisible = btn;
        });

        const currentActive = document.querySelector('.tab-btn.active');
        if (currentActive && currentActive.classList.contains('hidden-by-filter') && firstVisible) {
            this.activateTab(firstVisible);
        } else if (currentActive) {
            this.updatePillPosition(currentActive);
        }
    },

    handleKeyNavigation(e, currentIndex) {
        let nextIndex = null;
        if (e.key === 'ArrowRight') {
            nextIndex = (currentIndex + 1) % this.buttons.length;
        } else if (e.key === 'ArrowLeft') {
            nextIndex = (currentIndex - 1 + this.buttons.length) % this.buttons.length;
        }
        if (nextIndex !== null) {
            e.preventDefault();
            this.buttons[nextIndex].focus();
            this.activateTab(this.buttons[nextIndex]);
        }
    }
};

/* =====================================================================
   SHARED WORKSPACE BAR (Synergy Across Modules)
   ===================================================================== */
function updateWorkspaceState(file, jobDescription, skills) {
    if (file) AppState.activeResumeFile = file;
    if (jobDescription !== undefined) AppState.activeJobDescription = jobDescription;
    if (skills !== undefined) AppState.activeRequiredSkills = skills;

    const currentTab = document.querySelector('.tab-btn.active')?.getAttribute('data-tab');
    checkWorkspaceSyncBar(currentTab);
}

function checkWorkspaceSyncBar(tabId) {
    const bar = document.getElementById('workspace-sync-bar');
    if (!bar) return;

    const syncableTabs = ['github', 'recruiter', 'improve', 'cover-letter', 'ats', 'interview', 'career', 'salary'];
    const hasData = AppState.activeResumeFile || AppState.activeJobDescription || AppState.activeResumeText;

    if (hasData && syncableTabs.includes(tabId)) {
        bar.classList.add('active');
        const name = AppState.activeResumeFile ? AppState.activeResumeFile.name : 'Active resume text';
        document.getElementById('sync-bar-text').textContent = `Loaded in workspace: "${name}". Click to apply to this tool.`;
    } else {
        bar.classList.remove('active');
    }
}

function applyWorkspaceDataToCurrentTab() {
    const activeTab = document.querySelector('.tab-btn.active')?.getAttribute('data-tab');
    if (!activeTab) return;

    if (activeTab === 'github') {
        if (AppState.activeResumeText) {
            const el = document.getElementById('github-resume-input');
            if (el) el.value = AppState.activeResumeText;
        }
    } else if (activeTab === 'recruiter') {
        if (AppState.activeJobDescription) document.getElementById('recruiter-job').value = AppState.activeJobDescription;
        if (AppState.activeResumeText) document.getElementById('recruiter-resume').value = AppState.activeResumeText;
    } else if (activeTab === 'improve') {
        if (AppState.activeResumeFile) syncFileToInput('improve-file', AppState.activeResumeFile);
        if (AppState.activeJobDescription) document.getElementById('improve-job').value = AppState.activeJobDescription;
    } else if (activeTab === 'cover-letter') {
        if (AppState.activeResumeFile) syncFileToInput('cover-file', AppState.activeResumeFile);
        if (AppState.activeJobDescription) document.getElementById('cover-job').value = AppState.activeJobDescription;
    } else if (activeTab === 'ats') {
        if (AppState.activeResumeFile) syncFileToInput('ats-file', AppState.activeResumeFile);
    } else if (activeTab === 'interview') {
        if (AppState.activeResumeText) document.getElementById('mock-resume').value = AppState.activeResumeText;
        if (AppState.activeJobDescription) document.getElementById('mock-job').value = AppState.activeJobDescription;
    } else if (activeTab === 'career') {
        if (AppState.activeResumeFile) syncFileToInput('career-file', AppState.activeResumeFile);
        if (AppState.activeJobDescription) document.getElementById('career-job').value = AppState.activeJobDescription;
    } else if (activeTab === 'salary') {
        if (AppState.activeResumeFile) syncFileToInput('salary-file', AppState.activeResumeFile);
        if (AppState.activeJobDescription) document.getElementById('salary-job').value = AppState.activeJobDescription;
    }

    showToast('Applied active resume & job description to this tool!', 'success');
}

function syncFileToInput(inputId, fileObj) {
    const input = document.getElementById(inputId);
    if (!input || !fileObj) return;
    try {
        const dt = new DataTransfer();
        dt.items.add(fileObj);
        input.files = dt.files;
        input.dispatchEvent(new Event('change'));
    } catch {
        // Fallback for older browsers
    }
}

/* =====================================================================
   DEMO DATA LOADER (1-Click Sample Testing)
   ===================================================================== */
function loadDemoProfile(profileKey = 'fullstack') {
    const demo = DemoProfiles[profileKey];
    if (!demo) return;

    // Create synthetic File object
    const blob = new Blob([demo.content], { type: 'text/plain' });
    const sampleFile = new File([blob], demo.filename, { type: 'text/plain' });

    // Populate Single Analysis
    syncFileToInput('single-file', sampleFile);
    document.getElementById('single-job').value = demo.jobDescription;
    document.getElementById('single-skills').value = demo.requiredSkills;

    // Update global state
    AppState.activeResumeFile = sampleFile;
    AppState.activeJobDescription = demo.jobDescription;
    AppState.activeResumeText = demo.content;
    AppState.activeRequiredSkills = demo.requiredSkills;

    // Update Single Analysis Card preview
    const docCard = document.getElementById('single-doc-card');
    const nameEl = document.getElementById('single-file-name');
    if (nameEl) nameEl.textContent = `${demo.filename} (Sample Tech Lead)`;
    if (docCard) docCard.style.display = 'flex';

    // Also populate Recruiter & Mock interview textareas
    const recResume = document.getElementById('recruiter-resume');
    const recJob = document.getElementById('recruiter-job');
    if (recResume) recResume.value = demo.content;
    if (recJob) recJob.value = demo.jobDescription;

    const mockResume = document.getElementById('mock-resume');
    const mockJob = document.getElementById('mock-job');
    if (mockResume) mockResume.value = demo.content;
    if (mockJob) mockJob.value = demo.jobDescription;

    // Switch to Single Analysis tab
    const singleTabBtn = document.querySelector('[data-tab="single"]');
    if (singleTabBtn) TabSystem.activateTab(singleTabBtn);

    showToast('Sample Staff Engineer profile & Job Description loaded! Click "Run Full Intelligence Analysis".', 'success');
}

/* =====================================================================
   DROPZONE & FILE MANAGEMENT HELPER
   ===================================================================== */
function setupDropzone(dzId, inputId, cardId, nameId) {
    const dz = document.getElementById(dzId);
    const input = document.getElementById(inputId);
    if (!dz || !input) return;

    dz.addEventListener('click', () => input.click());

    dz.addEventListener('dragover', e => {
        e.preventDefault();
        dz.classList.add('drag-over');
    });

    dz.addEventListener('dragleave', () => dz.classList.remove('drag-over'));

    dz.addEventListener('drop', e => {
        e.preventDefault();
        dz.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            input.dispatchEvent(new Event('change'));
        }
    });

    input.addEventListener('change', () => {
        if (!input.files || !input.files.length) return;
        const file = input.files[0];

        // Trigger celebratory micro-animation
        dz.classList.remove('celebrate-drop');
        void dz.offsetWidth; // force reflow
        dz.classList.add('celebrate-drop');
        setTimeout(() => dz.classList.remove('celebrate-drop'), 700);

        // Validate file size (16MB limit)
        if (file.size > 16 * 1024 * 1024) {
            showToast(`File "${file.name}" exceeds the 16 MB limit.`, 'error');
            input.value = '';
            return;
        }

        if (cardId && nameId) {
            const card = document.getElementById(cardId);
            const nameEl = document.getElementById(nameId);
            if (nameEl) {
                const count = input.files.length;
                nameEl.textContent = count > 1 ? `${count} files selected` : file.name;
            }
            if (card) card.style.display = 'flex';
        }

        // If Single Analysis dropzone, update global workspace state
        if (inputId === 'single-file') {
            updateWorkspaceState(file);
        }

        showToast(`Selected: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`, 'info');
    });
}

/* =====================================================================
   SKELETON & BUTTON LOADING STATE
   ===================================================================== */
function skeletonHTML(lines = 5) {
    return `
    <div class="result-block" style="border-color: rgba(99,102,241,0.25);">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:18px;">
            <div class="skeleton" style="width:36px; height:36px; border-radius:10px;"></div>
            <div class="skeleton" style="width:40%; height:20px;"></div>
        </div>
        ${Array.from({ length: lines }, (_, i) => `
            <div class="skeleton skeleton-block ${['w-80', 'w-60', 'w-80', 'w-40', 'w-60'][i % 5]}"></div>
        `).join('')}
    </div>`;
}

function setLoading(btn, isLoading, label = '') {
    if (!btn) return;
    if (isLoading) {
        btn.disabled = true;
        btn._origHTML = btn.innerHTML;
        btn.innerHTML = `<i class="fas fa-spinner fa-spin"></i> Processing Intelligence Modules…`;
    } else {
        btn.disabled = false;
        btn.innerHTML = btn._origHTML || label;
    }
}

/* =====================================================================
   INTERACTIVE SPOTLIGHT ENGINE (Cursor-Reactive Ambient Glow)
   ===================================================================== */
(function initSpotlightEngine() {
    let rafId = null;
    document.addEventListener('mousemove', e => {
        if (rafId) return;
        rafId = requestAnimationFrame(() => {
            rafId = null;
            const target = e.target.closest('.spotlight-card, .result-block, .persona-card, .career-card, .dropzone, .score-ring-card, .stat-pill');
            if (!target) return;
            const rect = target.getBoundingClientRect();
            target.style.setProperty('--mouse-x', `${e.clientX - rect.left}px`);
            target.style.setProperty('--mouse-y', `${e.clientY - rect.top}px`);
        });
    }, { passive: true });
})();

/* =====================================================================
   INTERACTIVE 3D PERSPECTIVE TILT PHYSICS (Gyroscope Cursor Reactivity)
   ===================================================================== */
(function init3DTiltCards() {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    let activeCard = null;
    let cardRect = null;
    let rafId = null;

    document.addEventListener('mousemove', e => {
        const card = e.target.closest('.tilt-card, .score-ring-card, .persona-card, .career-card, .stat-pill');
        if (!card) {
            if (activeCard) {
                activeCard.style.transform = '';
                activeCard = null;
            }
            return;
        }

        if (activeCard !== card) {
            if (activeCard) activeCard.style.transform = '';
            activeCard = card;
            cardRect = card.getBoundingClientRect();
        }

        if (rafId) return;
        rafId = requestAnimationFrame(() => {
            rafId = null;
            if (!activeCard || !cardRect) return;
            const cx = cardRect.left + cardRect.width / 2;
            const cy = cardRect.top + cardRect.height / 2;
            const dx = (e.clientX - cx) / (cardRect.width / 2);
            const dy = (e.clientY - cy) / (cardRect.height / 2);
            const maxTilt = 6;
            const rotX = (-dy * maxTilt).toFixed(2);
            const rotY = (dx * maxTilt).toFixed(2);

            activeCard.style.transform = `perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg) translateY(-3px) scale3d(1.015, 1.015, 1.015)`;
        });
    }, { passive: true });

    document.addEventListener('mouseleave', () => {
        if (activeCard) {
            activeCard.style.transform = '';
            activeCard = null;
        }
    });
})();

/* =====================================================================
   TACTILE CLICK RIPPLE WAVE ENGINE
   ===================================================================== */
(function initClickRippleEffect() {
    document.addEventListener('click', e => {
        const btn = e.target.closest('.btn-primary, .btn-action, .nav-cta, .btn-demo-quick, .btn-subtle');
        if (!btn) return;
        const rect = btn.getBoundingClientRect();
        const ripple = document.createElement('span');
        ripple.className = 'click-ripple';
        const size = Math.max(rect.width, rect.height) * 2;
        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${e.clientX - rect.left - size / 2}px`;
        ripple.style.top = `${e.clientY - rect.top - size / 2}px`;
        btn.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    });
})();

/* =====================================================================
   ODOMETER / COUNT-UP NUMBER ANIMATOR
   ===================================================================== */
function animateCountUp(element, endVal, suffix = '', duration = 1200) {
    if (!element) return;
    const startVal = 0;
    const startTime = performance.now();
    const isFloat = String(endVal).includes('.');

    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        // Exponential ease out: 1 - 2^(-10 * progress)
        const ease = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress);
        const current = startVal + (endVal - startVal) * ease;

        element.textContent = (isFloat ? current.toFixed(1) : Math.round(current)) + suffix;

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = endVal + suffix;
        }
    }
    requestAnimationFrame(update);
}

/* =====================================================================
   SVG SCORE RINGS & RADAR CHART ENGINE
   ===================================================================== */
function createScoreRing(value, color, label, size = 84) {
    const r = 34;
    const circumference = 2 * Math.PI * r;
    const offset = circumference - (Math.min(Math.max(value, 0), 100) / 100) * circumference;

    return `
    <div class="score-ring-card spotlight-card" title="${label}: ${value}%">
        <div style="position:relative; width:${size}px; height:${size}px; flex-shrink:0;">
            <svg class="score-ring-svg" width="${size}" height="${size}" viewBox="0 0 80 80">
                <circle class="score-ring-bg" cx="40" cy="40" r="${r}" stroke-width="7"/>
                <circle class="score-ring-fill" cx="40" cy="40" r="${r}" stroke-width="7"
                    stroke="${color}"
                    style="stroke-dasharray:${circumference}; stroke-dashoffset:${circumference};"
                    data-offset="${offset}"/>
            </svg>
            <div class="score-ring-label count-up" data-target="${value}" style="color:${color}; font-size:1.15rem;">0</div>
        </div>
        <div class="score-ring-sub">${label}</div>
    </div>`;
}

function animateRings() {
    document.querySelectorAll('.score-ring-fill').forEach(ring => {
        const targetOffset = parseFloat(ring.getAttribute('data-offset'));
        requestAnimationFrame(() => {
            ring.style.strokeDashoffset = targetOffset;
        });
    });

    document.querySelectorAll('.count-up[data-target]').forEach(el => {
        const targetVal = parseFloat(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        if (!isNaN(targetVal)) {
            animateCountUp(el, targetVal, suffix);
        }
    });
}

function drawRadar(canvasId, labels, values, color = '#6366f1') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    // HiDPI crisp rendering
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = (rect.width || 320) * dpr;
    canvas.height = (rect.height || 300) * dpr;

    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);

    const W = rect.width || 320;
    const H = rect.height || 300;
    const cx = W / 2;
    const cy = H / 2;
    const maxR = Math.min(cx, cy) * 0.72;
    const n = labels.length;

    ctx.clearRect(0, 0, W, H);

    const angleStep = (2 * Math.PI) / n;
    const startAngle = -Math.PI / 2;

    // Concentric Web Rings
    for (let ring = 1; ring <= 5; ring++) {
        ctx.beginPath();
        const rr = (ring / 5) * maxR;
        for (let i = 0; i < n; i++) {
            const angle = startAngle + i * angleStep;
            const x = cx + rr * Math.cos(angle);
            const y = cy + rr * Math.sin(angle);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = AppState.theme === 'dark' ? 'rgba(148, 163, 184, 0.15)' : 'rgba(148, 163, 184, 0.25)';
        ctx.lineWidth = 1;
        ctx.stroke();
        if (ring === 5) {
            ctx.fillStyle = AppState.theme === 'dark' ? 'rgba(148, 163, 184, 0.03)' : 'rgba(148, 163, 184, 0.05)';
            ctx.fill();
        }
    }

    // Spokes
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + maxR * Math.cos(angle), cy + maxR * Math.sin(angle));
        ctx.strokeStyle = AppState.theme === 'dark' ? 'rgba(148, 163, 184, 0.16)' : 'rgba(148, 163, 184, 0.22)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }

    // Data Polygon
    ctx.beginPath();
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        const rr = (Math.min(Math.max(values[i], 0), 100) / 100) * maxR;
        const x = cx + rr * Math.cos(angle);
        const y = cy + rr * Math.sin(angle);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(99, 102, 241, 0.22)';
    ctx.fill();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // Data Points
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        const rr = (Math.min(Math.max(values[i], 0), 100) / 100) * maxR;
        ctx.beginPath();
        ctx.arc(cx + rr * Math.cos(angle), cy + rr * Math.sin(angle), 4.5, 0, Math.PI * 2);
        ctx.fillStyle = color;
        ctx.fill();
    }

    // Dimension Labels
    ctx.font = '700 11px Plus Jakarta Sans, sans-serif';
    ctx.fillStyle = AppState.theme === 'dark' ? 'rgba(226, 232, 240, 0.9)' : 'rgba(30, 41, 59, 0.9)';
    ctx.textAlign = 'center';
    for (let i = 0; i < n; i++) {
        const angle = startAngle + i * angleStep;
        const rr = maxR + 20;
        const x = cx + rr * Math.cos(angle);
        const y = cy + rr * Math.sin(angle) + 4;
        ctx.fillText(labels[i], x, y);
    }
}

/* =====================================================================
   TAB 1: SINGLE RESUME ANALYSIS
   ===================================================================== */
async function runSingleAnalysis() {
    const fileInput = document.getElementById('single-file');
    const file = fileInput ? fileInput.files[0] : null;
    const job = document.getElementById('single-job')?.value || '';
    const skills = document.getElementById('single-skills')?.value || '';
    const container = document.getElementById('single-results');
    const btn = document.getElementById('single-run-btn');

    if (!file) {
        showToast('Please select a resume file or click "Load Sample Profile"', 'error');
        return;
    }

    container.style.display = 'block';
    container.innerHTML = skeletonHTML(8);
    setLoading(btn, true);
    showToast('Executing Deep Intelligence Pipeline…', 'info');

    // Update global state
    updateWorkspaceState(file, job, skills);

    const fd = new FormData();
    fd.append('file', file);
    fd.append('job_description', job);
    fd.append('required_skills', skills);
    fd.append('analysis_mode', currentAnalysisMode());

    try {
        const res = await fetch('/api/analyze', { method: 'POST', body: fd });
        const data = await res.json();
        setLoading(btn, false);

        if (data.error) {
            showToast(data.error, 'error');
            container.innerHTML = isQuotaExhaustedError(data.error)
                ? renderQuotaErrorCard(data.error, 'single')
                : `
                <div class="result-block" style="border-color:var(--c-rose);">
                    <div style="color:var(--c-rose); font-weight:700;"><i class="fas fa-triangle-exclamation"></i> Analysis Failed: ${escapeHTML(data.error)}</div>
                </div>`;
            return;
        }

        AppState.lastAnalysisData = data;
        renderFullPlatform(data, 'single-results');
        showToast('Full Intelligence Analysis Complete!', 'success');
    } catch (e) {
        setLoading(btn, false);
        showToast('Network / Server Error: ' + e.message, 'error');
    }
}

/* =====================================================================
   RENDER FULL PLATFORM INTELLIGENCE RESULTS
   ===================================================================== */
function renderFullPlatform(data, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    const intel = data.intelligence_platform || {};
    const dash = intel.analytics_dashboard || {};
    const reasoning = intel.reasoning_map || {};
    const evidence = intel.evidence_verification || {};
    const claims = intel.audited_claims || [];
    const risks = intel.interview_risks || [];
    const implicit = intel.implicit_skills || [];
    const roadmap = intel.learning_roadmap || [];
    const personas = intel.recruiter_simulations || {};
    const projects = intel.project_matches || [];
    const fairness = intel.fairness_audit || {};

    const hs = dash.resume_health_score ?? 85;
    const js = dash.job_match_score ?? 84;
    const sc = dash.skill_coverage_pct ?? 91;
    const ec = dash.evidence_coverage_pct ?? 76;
    const ir = dash.interview_readiness_pct ?? 72;
    const cp = dash.resume_completeness_pct ?? 94;

    const rings = [
        { v: hs, c: 'var(--c-indigo)', l: 'Resume Health' },
        { v: js, c: 'var(--c-green)', l: 'Job Match' },
        { v: sc, c: 'var(--c-purple)', l: 'Skill Coverage' },
        { v: ec, c: 'var(--c-cyan)', l: 'Evidence Proof' },
        { v: ir, c: 'var(--c-amber)', l: 'Interview Ready' },
        { v: cp, c: 'var(--c-blue)', l: 'Completeness' }
    ];

    const radarLabels = ['Skills', 'Projects', 'Experience', 'Education', 'Evidence'];
    const radarVals = [
        reasoning.breakdown?.skills_score ?? sc,
        reasoning.breakdown?.projects_score ?? js,
        reasoning.breakdown?.experience_score ?? ir,
        reasoning.breakdown?.education_score ?? 100,
        ec
    ];

    let html = `
    <!-- ACTION TOOLBAR -->
    <div class="results-action-bar">
        <button class="btn-subtle" onclick="printExecutiveReport()">
            <i class="fas fa-file-pdf" style="color:var(--c-rose);"></i> Export Executive PDF Report
        </button>
        <button class="btn-subtle" onclick="toggleKeywordHeatmap()">
            <i class="fas fa-highlighter" style="color:var(--c-teal);"></i> Keyword Heatmap
        </button>
        <button class="btn-subtle" onclick="exportAnalysisJSON()">
            <i class="fas fa-download"></i> Export JSON
        </button>
        <button class="btn-subtle" onclick="copyAnalysisSummary()">
            <i class="fas fa-copy"></i> Copy Summary
        </button>
    </div>

    <!-- INTERACTIVE KEYWORD HEATMAP -->
    <div class="result-block" id="keyword-heatmap-block" style="display:none; border-color:var(--c-teal); margin-bottom:20px;">
        <div class="result-block-hd">
            <div class="result-block-title" style="color:var(--c-teal);">
                <i class="fas fa-highlighter"></i> Visual Resume Keyword &amp; Proof Heatmap
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="chip success"><i class="fas fa-check"></i> ${(data.matching_skills || []).length} Matched Skills</span>
                <span class="chip warning"><i class="fas fa-triangle-exclamation"></i> ${(data.missing_skills || []).length} Missing Required</span>
            </div>
        </div>
        <p style="font-size:0.86rem; color:var(--text-2); margin-bottom:12px;">
            Target skills identified in your resume are highlighted in <mark class="kw-matched">Emerald</mark>. Review them in context to evaluate technical evidence depth.
        </p>
        <div class="heatmap-container" id="resume-heatmap-content">
            ${renderHighlightedResume(data)}
        </div>
    </div>

    <!-- EXECUTIVE DASHBOARD -->
    <div class="result-block" style="border-color: rgba(99, 102, 241, 0.4);">
        <div class="result-block-hd">
            <div class="result-block-title">
                <i class="fas fa-chart-line"></i> Executive Intelligence Dashboard
            </div>
            <span class="chip ${data.analysis_mode === 'local' ? 'success' : 'ai'}">
                <i class="fas ${data.analysis_mode === 'local' ? 'fa-laptop' : 'fa-sparkles'}"></i>
                ${data.analysis_mode === 'local' ? 'Local Mode · Deterministic NLP' : 'AI-Assisted · GPT Engine'}
            </span>
        </div>

        ${data.analysis_mode === 'local' && data.ai_analysis?.scoring_breakdown ? `
        <div style="display:flex; flex-wrap:wrap; gap:10px; margin-bottom:20px;">
            <span class="chip info">Keyword Match: <strong class="count-up" data-target="${data.ai_analysis.scoring_breakdown.keyword_match}" data-suffix="%">0%</strong></span>
            <span class="chip info">TF-IDF Similarity: <strong class="count-up" data-target="${data.ai_analysis.scoring_breakdown.tfidf_similarity}" data-suffix="%">0%</strong></span>
            ${data.ai_analysis.scoring_breakdown.required_skill_match != null ? `<span class="chip info">Required Skills: <strong class="count-up" data-target="${data.ai_analysis.scoring_breakdown.required_skill_match}" data-suffix="%">0%</strong></span>` : ''}
        </div>` : ''}

        <!-- SCORE RINGS -->
        <div style="display:flex; flex-wrap:wrap; gap:16px; justify-content:center; margin-bottom:26px;">
            ${rings.map(r => createScoreRing(r.v, r.c, r.l)).join('')}
        </div>

        <!-- RADAR & PROGRESS -->
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:24px; align-items:center;">
            <div>
                <div style="font-weight:700; color:var(--text-1); margin-bottom:10px; font-size:0.95rem;">Competency Dimension Radar</div>
                <div class="radar-wrap">
                    <canvas id="radarCanvas" width="320" height="300"></canvas>
                </div>
            </div>
            <div>
                <div style="font-weight:700; color:var(--text-1); margin-bottom:14px; font-size:0.95rem;">Dimension Breakdown</div>
                ${rings.map(r => `
                <div style="margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; font-size:0.83rem; margin-bottom:4px;">
                        <span style="color:var(--text-2); font-weight:600;">${r.l}</span>
                        <strong class="count-up" data-target="${r.v}" data-suffix="%" style="color:${r.c}; font-family:var(--font-mono);">0%</strong>
                    </div>
                    <div class="prog-bg"><div class="prog-fill" style="background: linear-gradient(90deg, ${r.c}, ${r.c}88);" data-width="${r.v}"></div></div>
                </div>`).join('')}
            </div>
        </div>
    </div>

    <!-- EXPLAINABLE MATCHING -->
    <div class="result-block">
        <div class="result-block-hd">
            <div class="result-block-title"><i class="fas fa-brain"></i> Explainable Fit Assessment</div>
            <span class="count-up" data-target="${reasoning.overall_match || 84}" data-suffix="% Match" style="font-size:1.35rem; font-weight:900; color:var(--c-blue); font-family:var(--font-mono);">0% Match</span>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(130px, 1fr)); gap:12px;">
            ${[
                { label: 'Skills Alignment', val: reasoning.breakdown?.skills_score || sc },
                { label: 'Project Proof', val: reasoning.breakdown?.projects_score || js },
                { label: 'Experience Depth', val: reasoning.breakdown?.experience_score || ir },
                { label: 'Credentials', val: reasoning.breakdown?.education_score || 100 }
            ].map(b => `
            <div style="background:var(--bg-input); padding:16px; border-radius:12px; text-align:center; border:1px solid var(--glass-border);">
                <div class="count-up" data-target="${b.val}" data-suffix="%" style="font-size:1.3rem; font-weight:900; color:var(--text-1); margin-bottom:4px; font-family:var(--font-mono);">0%</div>
                <div style="font-size:0.75rem; color:var(--text-3); text-transform:uppercase; letter-spacing:0.07em; font-weight:700;">${b.label}</div>
                <div class="prog-bg" style="margin-top:8px;"><div class="prog-fill" data-width="${b.val}"></div></div>
            </div>`).join('')}
        </div>
    </div>

    <!-- EVIDENCE-BASED SKILL VERIFICATION -->
    <div class="result-block">
        <div class="result-block-hd">
            <div class="result-block-title"><i class="fas fa-shield-check"></i> Evidence-Based Skill Verification</div>
            <span class="badge high">${Object.keys(evidence).length} Verified Skills</span>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px;">
    `;

    for (const [skill, ev] of Object.entries(evidence)) {
        const lvl = (ev.level || '').toUpperCase();
        const badgeClass = lvl === 'HIGH' ? 'high' : lvl === 'MEDIUM' ? 'medium' : lvl === 'WEAK' ? 'weak' : 'none';
        html += `
            <div style="background:var(--bg-input); padding:14px 18px; border-radius:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; border:1px solid var(--glass-border);">
                <div>
                    <strong style="color:var(--text-1); font-size:0.95rem;">${escapeHTML(skill)}</strong>
                    <span class="badge ${badgeClass}" style="margin-left:8px;">${ev.level}</span>
                    <div style="font-size:0.78rem; color:var(--text-3); margin-top:3px;"><i class="fas fa-location-dot"></i> Section: ${escapeHTML(ev.location || 'N/A')}</div>
                </div>
                <div style="font-size:0.84rem; color:var(--text-2); max-width:440px;">${escapeHTML(ev.recommendation || '')}</div>
            </div>`;
    }

    html += `</div></div>`;

    // CLAIMS AUDIT
    if (claims.length > 0) {
        html += `
        <div class="result-block" style="border-color:rgba(245, 158, 11, 0.4);">
            <div class="result-block-hd">
                <div class="result-block-title" style="color:var(--c-amber);"><i class="fas fa-triangle-exclamation"></i> Audited Claim Alerts</div>
                <span class="badge weak">${claims.length} Flagged</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:10px;">`;
        claims.forEach(c => {
            html += `
                <div style="background:var(--bg-input); padding:16px; border-radius:12px; border:1px solid rgba(245,158,11,0.2);">
                    <div style="font-weight:700; color:var(--c-amber); margin-bottom:6px;"><i class="fas fa-flag"></i> ${escapeHTML(c.status)}: "${escapeHTML(c.claim)}"</div>
                    <div style="font-size:0.84rem; color:var(--text-2); margin-bottom:6px;"><strong>Flags:</strong> ${escapeHTML((c.reasons || []).join(', '))}</div>
                    <div style="font-size:0.84rem; color:var(--c-cyan);"><strong>Recommendation:</strong> ${escapeHTML(c.suggested_improvement || '')}</div>
                </div>`;
        });
        html += `</div></div>`;
    }

    // INTERVIEW RISKS
    if (risks.length > 0) {
        html += `
        <div class="result-block">
            <div class="result-block-hd">
                <div class="result-block-title"><i class="fas fa-comments-question"></i> Interview Risk Analyzer & Target Questions</div>
                <span class="badge none">${risks.length} Risk Areas</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:12px;">`;
        risks.forEach(r => {
            const chipClass = r.risk_level === 'HIGH' ? 'danger' : 'warning';
            html += `
                <div style="background:var(--bg-input); padding:16px 18px; border-radius:12px; border:1px solid var(--glass-border);">
                    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
                        <span style="font-weight:800; color:var(--text-1); font-size:0.95rem;">${escapeHTML(r.term)}</span>
                        <span class="chip ${chipClass}">${escapeHTML(r.risk_level)} RISK</span>
                    </div>
                    <p style="font-size:0.84rem; color:var(--text-3); margin-bottom:8px;">Context: "${escapeHTML(r.claim)}" — ${escapeHTML(r.why)}</p>
                    <p style="font-size:0.84rem; font-weight:700; color:var(--c-blue); margin-bottom:6px;"><i class="fas fa-question-circle"></i> Probable Technical Questions:</p>
                    <ul style="padding-left:18px; font-size:0.84rem; color:var(--text-2); display:flex; flex-direction:column; gap:4px;">
                        ${(r.likely_questions || []).map(q => `<li>${escapeHTML(q)}</li>`).join('')}
                    </ul>
                </div>`;
        });
        html += `</div></div>`;
    }

    // IMPLICIT SKILLS
    if (implicit.length > 0) {
        html += `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-lightbulb"></i> Hidden / Inferred Competencies</div></div>
            <p style="font-size:0.88rem; color:var(--text-2); margin-bottom:12px;">Identified through architectural context and project combinations:</p>
            <div class="chip-row">
                ${implicit.map(imp => `<span class="chip ai"><i class="fas fa-sparkles"></i> ${escapeHTML(imp.skill)} (${escapeHTML(imp.confidence)} Confidence)</span>`).join('')}
            </div>
        </div>`;
    }

    // 4-WEEK ROADMAP
    if (roadmap.length > 0) {
        html += `
        <div class="result-block">
            <div class="result-block-hd">
                <div class="result-block-title"><i class="fas fa-map-location-dot"></i> 4-Week Personalized Upskilling Roadmap</div>
                <span class="chip info"><i class="fas fa-calendar-check"></i> Actionable</span>
            </div>
            <div style="display:flex; flex-direction:column; gap:12px;">`;
        roadmap.forEach((wk, wIdx) => {
            html += `
                <div style="background:var(--bg-input); padding:18px; border-radius:12px; border-left:4px solid var(--c-blue); border:1px solid var(--glass-border); border-left-width:4px;">
                    <div style="font-weight:800; color:var(--c-blue); font-size:0.96rem; margin-bottom:4px;">${escapeHTML(wk.week)}: ${escapeHTML(wk.title)}</div>
                    <p style="font-size:0.82rem; color:var(--text-3); margin-bottom:10px;">Primary Skill Focus: <strong style="color:var(--text-2);">${escapeHTML(wk.skill_focus)}</strong></p>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                        ${(wk.tasks || []).map((t, tIdx) => {
                            const taskId = `task-${wIdx}-${tIdx}`;
                            const isChecked = AppState.roadmapChecked.has(taskId) ? 'checked' : '';
                            return `<li style="display:flex; align-items:flex-start; gap:10px; font-size:0.85rem; color:var(--text-2);">
                                <input type="checkbox" id="${taskId}" ${isChecked} onchange="toggleRoadmapTask('${taskId}')" style="margin-top:4px; accent-color:var(--c-blue); cursor:pointer;">
                                <label for="${taskId}" style="cursor:pointer;">${escapeHTML(t)}</label>
                            </li>`;
                        }).join('')}
                    </ul>
                </div>`;
        });
        html += `</div></div>`;
    }

    // RECRUITER PERSONAS
    if (personas.startup_recruiter || personas.enterprise_recruiter) {
        html += `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-user-astronaut"></i> Multi-Perspective Hiring Simulation</div></div>
            <div class="persona-grid">
                ${[
                    { key: 'startup_recruiter', label: 'Startup Founder / Lead', color: 'var(--c-green)' },
                    { key: 'enterprise_recruiter', label: 'Enterprise Talent Lead', color: 'var(--c-blue)' },
                    { key: 'technical_interviewer', label: 'Principal Tech Interviewer', color: 'var(--c-amber)' }
                ].map(p => `
                <div class="persona-card">
                    <div class="persona-title">
                        ${p.label}
                        <span class="count-up" data-target="${personas[p.key]?.fit_score || 0}" data-suffix="%" style="color:${p.color}; font-size:1.15rem; font-family:var(--font-mono);">0%</span>
                    </div>
                    <p style="font-size:0.84rem; color:var(--text-3); margin-bottom:10px;">Focus: ${escapeHTML(personas[p.key]?.focus || '')}</p>
                    <div style="font-weight:700; font-size:0.86rem; color:var(--c-blue);"><i class="fas fa-gavel"></i> ${escapeHTML(personas[p.key]?.verdict || '')}</div>
                </div>`).join('')}
            </div>
        </div>`;
    }

    // FAIRNESS AUDIT
    if (fairness.audit_status) {
        html += `
        <div class="result-block" style="border-color:rgba(16, 185, 129, 0.4);">
            <div class="result-block-hd">
                <div class="result-block-title" style="color:var(--c-green);"><i class="fas fa-shield-halved"></i> Fairness & Demographic Disparity Audit</div>
                <span class="chip success">Pass</span>
            </div>
            <p style="font-weight:800; color:var(--c-green); margin-bottom:6px;">${escapeHTML(fairness.audit_status)}</p>
            <p style="font-size:0.86rem; color:var(--text-2); margin-bottom:6px;">${escapeHTML(fairness.neutral_assessment || '')}</p>
            <p style="font-size:0.78rem; color:var(--text-3); font-style:italic;">${escapeHTML(fairness.audit_limitation_note || '')}</p>
        </div>`;
    }

    container.innerHTML = html;
    container.style.display = 'block';

    // Animate rings & radar
    setTimeout(animateRings, 150);
    setTimeout(() => {
        document.querySelectorAll('.prog-fill[data-width]').forEach(bar => {
            bar.style.width = bar.getAttribute('data-width') + '%';
        });
    }, 250);
    setTimeout(() => drawRadar('radarCanvas', radarLabels, radarVals, '#6366f1'), 350);
}

function toggleRoadmapTask(taskId) {
    if (AppState.roadmapChecked.has(taskId)) {
        AppState.roadmapChecked.delete(taskId);
    } else {
        AppState.roadmapChecked.add(taskId);
    }
}

function exportAnalysisJSON() {
    if (!AppState.lastAnalysisData) {
        showToast('No analysis data to export', 'error');
        return;
    }
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(AppState.lastAnalysisData, null, 2));
    const a = document.createElement('a');
    a.href = dataStr;
    a.download = `resume_analysis_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast('Exported analysis to JSON!', 'success');
}

function copyAnalysisSummary() {
    if (!AppState.lastAnalysisData) {
        showToast('No analysis to copy', 'error');
        return;
    }
    const d = AppState.lastAnalysisData.intelligence_platform?.analytics_dashboard || {};
    const summary = `ResumeAI Analysis Report:
- Health Score: ${d.resume_health_score ?? 'N/A'}%
- Job Match Score: ${d.job_match_score ?? 'N/A'}%
- Skill Coverage: ${d.skill_coverage_pct ?? 'N/A'}%
- Evidence Proof: ${d.evidence_coverage_pct ?? 'N/A'}%
- Mode: ${AppState.lastAnalysisData.analysis_mode}`;

    navigator.clipboard.writeText(summary).then(() => {
        showToast('Summary copied to clipboard!', 'success');
    });
}

function renderHighlightedResume(data) {
    const rawText = data.resume_text || AppState.activeResumeText || '';
    if (!rawText) return '<em>No parsed resume text available for keyword heatmap.</em>';

    const matched = (data.matching_skills || []).map(s => typeof s === 'string' ? s : s.skill).filter(Boolean);
    let escaped = escapeHTML(rawText);

    // Sort by length descending so longer phrases match first
    const sortedSkills = [...new Set(matched)].sort((a, b) => b.length - a.length);

    for (const skill of sortedSkills) {
        if (!skill || skill.length < 2) continue;
        const pattern = new RegExp(`\\b(${skill.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})\\b`, 'gi');
        escaped = escaped.replace(pattern, '<mark class="kw-matched">$1</mark>');
    }

    return escaped;
}

function toggleKeywordHeatmap() {
    const block = document.getElementById('keyword-heatmap-block');
    if (!block) return;
    const isHidden = block.style.display === 'none';
    block.style.display = isHidden ? 'block' : 'none';
    if (isHidden) {
        block.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        showToast('Keyword Heatmap Revealed', 'info');
    }
}

function printExecutiveReport() {
    if (!AppState.lastAnalysisData) {
        showToast('Please run a resume analysis first to export the executive report.', 'error');
        return;
    }
    showToast('Opening Executive Dossier Print / PDF Dialog…', 'info');
    setTimeout(() => window.print(), 350);
}

/* =====================================================================
   ANALYSIS HISTORY STORAGE & PERSISTENCE
   ===================================================================== */
function saveToAnalysisHistory(data) {
    if (!data) return;
    try {
        const history = JSON.parse(localStorage.getItem('resumeai_history') || '[]');
        const dash = data.intelligence_platform?.analytics_dashboard || {};
        const score = dash.job_match_score ?? data.ai_analysis?.overall_score ?? 84;
        const filename = data.file_name || AppState.activeResumeFile?.name || 'Candidate_Resume';

        // Check if identical scan exists recently
        const exists = history.find(h => h.filename === filename && Math.abs(h.score - score) < 0.1);
        if (exists) return;

        const record = {
            id: 'scan_' + Date.now(),
            filename: filename,
            score: Math.round(score),
            mode: data.analysis_mode || 'local',
            timestamp: new Date().toLocaleString(),
            dateIso: new Date().toISOString(),
            data: data
        };

        history.unshift(record);
        if (history.length > 20) history.pop();
        localStorage.setItem('resumeai_history', JSON.stringify(history));
        updateHistoryBadge();
    } catch (e) {
        console.warn('Failed to save scan to localStorage history', e);
    }
}

function updateHistoryBadge() {
    try {
        const history = JSON.parse(localStorage.getItem('resumeai_history') || '[]');
        const badge = document.getElementById('history-open-btn');
        if (badge) {
            badge.setAttribute('title', `View Scan History (${history.length} saved)`);
        }
    } catch {}
}

function openHistoryModal() {
    renderHistoryModal();
    const modal = document.getElementById('history-modal-backdrop');
    if (modal) modal.classList.add('active');
}

function closeHistoryModal() {
    const modal = document.getElementById('history-modal-backdrop');
    if (modal) modal.classList.remove('active');
}

function closeHistoryModalOnBackdrop(e) {
    if (e.target.id === 'history-modal-backdrop') closeHistoryModal();
}

function renderHistoryModal() {
    const container = document.getElementById('history-items-container');
    const label = document.getElementById('history-total-label');
    if (!container) return;

    let history = [];
    try {
        history = JSON.parse(localStorage.getItem('resumeai_history') || '[]');
    } catch { history = []; }

    if (label) label.textContent = `${history.length} candidate scans stored locally`;

    if (!history.length) {
        container.innerHTML = `<div style="text-align:center; color:var(--text-3); padding:30px 0;"><i class="fas fa-inbox" style="font-size:2rem; margin-bottom:10px; display:block; opacity:0.5;"></i>No saved candidate scans found. Run an analysis to archive results.</div>`;
        return;
    }

    container.innerHTML = history.map(h => `
        <div class="history-item">
            <div class="history-item-info">
                <div class="history-item-name"><i class="fas fa-file-lines" style="color:var(--c-indigo); margin-right:6px;"></i>${escapeHTML(h.filename)}</div>
                <div class="history-item-meta">
                    <span><i class="fas fa-calendar-day"></i> ${escapeHTML(h.timestamp)}</span>
                    <span><i class="fas fa-microchip"></i> ${h.mode === 'local' ? 'Local Mode' : 'AI Mode'}</span>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:12px;">
                <span class="badge ${h.score >= 80 ? 'high' : h.score >= 60 ? 'medium' : 'weak'}" style="font-size:0.85rem; font-family:var(--font-mono);">
                    ${h.score}% Match
                </span>
                <button class="btn-subtle" onclick="loadHistoryItem('${h.id}')" style="padding:6px 12px; font-size:0.8rem;">
                    <i class="fas fa-folder-open"></i> Load
                </button>
            </div>
        </div>
    `).join('');
}

function loadHistoryItem(id) {
    try {
        const history = JSON.parse(localStorage.getItem('resumeai_history') || '[]');
        const record = history.find(h => h.id === id);
        if (!record || !record.data) {
            showToast('Scan record not found', 'error');
            return;
        }

        AppState.lastAnalysisData = record.data;
        const singleTabBtn = document.querySelector('[data-tab="single"]');
        if (singleTabBtn) singleTabBtn.click();
        renderFullPlatform(record.data, 'single-results');
        closeHistoryModal();
        showToast(`Loaded saved analysis for "${record.filename}" (${record.score}%)`, 'success');
    } catch (e) {
        showToast('Failed to load scan: ' + e.message, 'error');
    }
}

function clearAnalysisHistory() {
    localStorage.removeItem('resumeai_history');
    renderHistoryModal();
    updateHistoryBadge();
    showToast('Analysis history cleared', 'info');
}

/* =====================================================================
   TAB 2: BATCH RANKING & FILTERING
   ===================================================================== */
async function runBatchAnalysis() {
    const input = document.getElementById('batch-files');
    const files = input ? input.files : null;
    const job = document.getElementById('batch-job')?.value || '';
    const container = document.getElementById('batch-results');

    if (!files || !files.length) {
        showToast('Please select multiple resume files to rank', 'error');
        return;
    }

    container.style.display = 'block';
    container.innerHTML = skeletonHTML(5);
    showToast('Ranking Candidate Pool…', 'info');

    const fd = new FormData();
    for (let f of files) fd.append('files', f);
    fd.append('job_description', job);
    fd.append('analysis_mode', currentAnalysisMode());

    try {
        const res = await fetch('/api/batch', { method: 'POST', body: fd });
        const data = await res.json();

        if (data.error) {
            showToast(data.error, 'error');
            container.innerHTML = isQuotaExhaustedError(data.error)
                ? renderQuotaErrorCard(data.error, 'batch')
                : `<div class="result-block" style="border-color:var(--c-rose);"><p style="color:var(--c-rose);">${escapeHTML(data.error)}</p></div>`;
            return;
        }

        AppState.batchResults = data.results || [];
        renderBatchTable(data, container);
        showToast('Batch Ranking Complete!', 'success');
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

function renderBatchTable(data, container) {
    const results = AppState.batchResults || [];
    let html = `
    <div class="result-block">
        <div class="result-block-hd">
            <div class="result-block-title"><i class="fas fa-layer-group"></i> Candidate Leaderboard</div>
            <span class="chip success">${data.successful_analyses || results.length} / ${data.total_files || results.length} Processed</span>
        </div>

        <div class="batch-controls-bar">
            <input type="text" class="batch-search-input" id="batch-filter" placeholder="Filter candidates by name…" oninput="filterBatchCandidates(this.value)">
            <div style="display:flex; gap:10px;">
                <select class="mode-select" id="batch-sort" onchange="sortBatchCandidates(this.value)" style="background:var(--bg-card); padding:6px 12px; border-radius:var(--r-sm); border:1px solid var(--glass-border);">
                    <option value="score-desc">Highest Match First</option>
                    <option value="score-asc">Lowest Match First</option>
                    <option value="name-asc">Candidate Name (A-Z)</option>
                </select>
                <button class="btn-subtle" onclick="exportBatchCSV()" style="padding:6px 14px; font-size:0.8rem;">
                    <i class="fas fa-file-csv"></i> Export CSV
                </button>
            </div>
        </div>

        <div id="batch-items-list" style="display:flex; flex-direction:column; gap:10px;">
            ${buildBatchItemsHTML(results)}
        </div>
    </div>`;

    container.innerHTML = html;
}

function buildBatchItemsHTML(results) {
    if (!results.length) {
        return `<p style="color:var(--text-3); text-align:center; padding:18px;">No candidates match filter.</p>`;
    }

    return results.map((r, idx) => {
        const score = Number(r.intelligence_platform?.analytics_dashboard?.job_match_score ?? r.score);
        const scoreColor = !isFinite(score) ? 'var(--text-3)' : score >= 85 ? 'var(--c-green)' : score >= 70 ? 'var(--c-teal)' : score >= 50 ? 'var(--c-amber)' : 'var(--c-rose)';
        const rankClass = idx < 3 ? `r${idx + 1}` : '';
        const name = r.filename || r.file_name || 'Resume';

        return `
        <div class="batch-candidate-row" data-name="${escapeHTML(name.toLowerCase())}" data-score="${isFinite(score) ? score : 0}" style="background:var(--bg-input); padding:14px 18px; border-radius:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; border:1px solid var(--glass-border); transition:var(--t-smooth);">
            <div style="display:flex; align-items:center;">
                <span class="cand-rank ${rankClass}">#${idx + 1}</span>
                <strong style="color:var(--text-1); font-size:0.95rem;">${escapeHTML(name)}</strong>
            </div>
            <div style="display:flex; align-items:center; gap:16px;">
                <span style="font-size:1.15rem; font-weight:900; color:${scoreColor}; font-family:var(--font-mono);">${isFinite(score) ? score + '% Match' : 'N/A'}</span>
            </div>
        </div>`;
    }).join('');
}

function filterBatchCandidates(query) {
    const q = query.toLowerCase().trim();
    document.querySelectorAll('.batch-candidate-row').forEach(row => {
        const name = row.getAttribute('data-name') || '';
        row.style.display = name.includes(q) ? 'flex' : 'none';
    });
}

function sortBatchCandidates(mode) {
    const list = [...AppState.batchResults];
    if (mode === 'score-desc') {
        list.sort((a, b) => (Number(b.intelligence_platform?.analytics_dashboard?.job_match_score ?? b.score) || 0) - (Number(a.intelligence_platform?.analytics_dashboard?.job_match_score ?? a.score) || 0));
    } else if (mode === 'score-asc') {
        list.sort((a, b) => (Number(a.intelligence_platform?.analytics_dashboard?.job_match_score ?? a.score) || 0) - (Number(b.intelligence_platform?.analytics_dashboard?.job_match_score ?? b.score) || 0));
    } else if (mode === 'name-asc') {
        list.sort((a, b) => (a.filename || a.file_name || '').localeCompare(b.filename || b.file_name || ''));
    }
    const container = document.getElementById('batch-items-list');
    if (container) container.innerHTML = buildBatchItemsHTML(list);
}

function exportBatchCSV() {
    if (!AppState.batchResults.length) {
        showToast('No batch results to export', 'error');
        return;
    }
    let csv = 'Rank,Filename,MatchScore,HealthScore\n';
    AppState.batchResults.forEach((r, idx) => {
        const score = r.intelligence_platform?.analytics_dashboard?.job_match_score ?? r.score ?? '';
        const health = r.intelligence_platform?.analytics_dashboard?.resume_health_score ?? '';
        const name = (r.filename || r.file_name || 'Candidate').replace(/"/g, '""');
        csv += `${idx + 1},"${name}",${score},${health}\n`;
    });
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `candidate_rankings_${Date.now()}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    showToast('Exported candidate rankings to CSV!', 'success');
}

/* =====================================================================
   TAB 3: RECRUITER LENS SIMULATION
   ===================================================================== */
async function runRecruiterSim() {
    const text = document.getElementById('recruiter-resume')?.value || '';
    const job = document.getElementById('recruiter-job')?.value || '';
    const div = document.getElementById('recruiter-results');

    if (!text.trim()) {
        showToast('Please provide resume content or click "Load Sample Profile"', 'error');
        return;
    }

    div.style.display = 'block';
    div.innerHTML = skeletonHTML(3);

    try {
        const res = await fetch('/api/intelligence/recruiter-sim', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: text, job_description: job, analysis_mode: currentAnalysisMode() })
        });
        const data = await res.json();

        if (data.startup_recruiter) {
            div.innerHTML = `
            <div class="result-block">
                <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-user-astronaut"></i> Multi-Perspective Recruiter Simulation</div></div>
                <div class="persona-grid">
                    ${[
                        { k: 'startup_recruiter', l: 'Startup Recruiter', c: 'var(--c-green)' },
                        { k: 'enterprise_recruiter', l: 'Enterprise Recruiter', c: 'var(--c-blue)' },
                        { k: 'technical_interviewer', l: 'Tech Interviewer', c: 'var(--c-amber)' }
                    ].map(p => `
                    <div class="persona-card">
                        <div class="persona-title">${p.l} <span class="count-up" data-target="${data[p.k]?.fit_score || 0}" data-suffix="%" style="color:${p.c}; font-family:var(--font-mono); font-size:1.1rem;">0%</span></div>
                        <p style="font-size:0.84rem; color:var(--text-3); margin-bottom:10px;">${escapeHTML(data[p.k]?.focus || '')}</p>
                        <div style="font-weight:700; font-size:0.86rem; color:var(--c-blue);"><i class="fas fa-gavel"></i> ${escapeHTML(data[p.k]?.verdict || '')}</div>
                    </div>`).join('')}
                </div>
            </div>`;
            animateRings();
        } else {
            div.innerHTML = `<pre style="background:var(--bg-input); padding:16px; border-radius:12px; overflow-x:auto; font-size:0.82rem;">${escapeHTML(JSON.stringify(data, null, 2))}</pre>`;
        }
        showToast('Recruiter Simulation Complete!', 'success');
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

/* =====================================================================
   TAB 4: LEARNING ROADMAP
   ===================================================================== */
async function generateRoadmap() {
    const skills = document.getElementById('roadmap-skills')?.value || '';
    const div = document.getElementById('roadmap-results');
    div.style.display = 'block';
    div.innerHTML = skeletonHTML(4);

    try {
        const res = await fetch('/api/analyze-text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: 'Software Engineer', required_skills: skills, analysis_mode: currentAnalysisMode() })
        });
        const data = await res.json();
        const roadmap = data.intelligence_platform?.learning_roadmap || [];

        if (!roadmap.length) {
            div.innerHTML = `<p style="color:var(--text-3); padding:16px;">No roadmap generated. Try adding specific skills above.</p>`;
            return;
        }

        let html = `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-map-location-dot"></i> Your 4-Week Learning Roadmap</div></div>
            <div style="display:flex; flex-direction:column; gap:12px;">`;
        roadmap.forEach((wk, wIdx) => {
            html += `
            <div style="background:var(--bg-input); padding:18px; border-radius:12px; border-left:4px solid var(--c-blue); border:1px solid var(--glass-border); border-left-width:4px;">
                <div style="font-weight:800; color:var(--c-blue); margin-bottom:4px; font-size:0.96rem;">${escapeHTML(wk.week)}: ${escapeHTML(wk.title)}</div>
                <ul style="list-style:none; display:flex; flex-direction:column; gap:8px; margin-top:10px;">
                    ${(wk.tasks || []).map((t, tIdx) => {
                        const id = `rdm-${wIdx}-${tIdx}`;
                        return `<li style="display:flex; align-items:flex-start; gap:10px; font-size:0.85rem; color:var(--text-2);">
                            <input type="checkbox" id="${id}" style="margin-top:3px; accent-color:var(--c-blue); cursor:pointer;">
                            <label for="${id}" style="cursor:pointer;">${escapeHTML(t)}</label>
                        </li>`;
                    }).join('')}
                </ul>
            </div>`;
        });
        html += '</div></div>';
        div.innerHTML = html;
        showToast('Learning Roadmap Generated!', 'success');
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

/* =====================================================================
   TAB 5: FAIRNESS AUDIT
   ===================================================================== */
async function runFairnessAudit() {
    const text = document.getElementById('fairness-text')?.value || '';
    const div = document.getElementById('fairness-results');
    if (!text.trim()) {
        showToast('Please enter resume text to audit', 'error');
        return;
    }
    div.style.display = 'block';
    div.innerHTML = skeletonHTML(2);

    try {
        const res = await fetch('/api/intelligence/fairness-audit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: text })
        });
        const data = await res.json();
        div.innerHTML = `
        <div class="result-block" style="border-color:var(--c-green);">
            <div class="result-block-hd"><div class="result-block-title" style="color:var(--c-green);"><i class="fas fa-shield-halved"></i> Fairness Consistency Verification</div></div>
            <p style="font-weight:800; color:var(--c-green); margin-bottom:8px;">${escapeHTML(data.audit_status || 'Audit Complete')}</p>
            <p style="font-size:0.88rem; color:var(--text-2);">${escapeHTML(data.neutral_assessment || JSON.stringify(data))}</p>
        </div>`;
        showToast('Demographic Audit Complete!', 'success');
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

/* =====================================================================
   TAB 6: VERSION COMPARE
   ===================================================================== */
async function runVersionCompare() {
    const v1 = document.getElementById('v1-text')?.value || '';
    const v2 = document.getElementById('v2-text')?.value || '';
    const div = document.getElementById('version-results');
    if (!v1.trim() || !v2.trim()) {
        showToast('Please provide text for both versions', 'error');
        return;
    }
    div.style.display = 'block';
    div.innerHTML = skeletonHTML(2);

    try {
        const res = await fetch('/api/intelligence/version-compare', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ version1_text: v1, version2_text: v2 })
        });
        const data = await res.json();
        div.innerHTML = `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-code-branch"></i> Version Delta Analysis</div></div>
            <p style="font-weight:800; color:var(--c-blue); margin-bottom:12px;">${escapeHTML(data.deltas?.summary_change || 'Analysis complete')}</p>
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:14px;">
                <div style="background:color-mix(in srgb, var(--c-green) 10%, var(--bg-input)); border-radius:12px; padding:16px; border:1px solid color-mix(in srgb, var(--c-green) 25%, transparent);">
                    <div style="font-weight:800; color:var(--c-green); margin-bottom:8px;"><i class="fas fa-plus"></i> Added Skills</div>
                    <p style="font-size:0.88rem; color:var(--text-2);">${escapeHTML((data.deltas?.added_skills || []).join(', ') || 'None detected')}</p>
                </div>
                <div style="background:color-mix(in srgb, var(--c-rose) 10%, var(--bg-input)); border-radius:12px; padding:16px; border:1px solid color-mix(in srgb, var(--c-rose) 25%, transparent);">
                    <div style="font-weight:800; color:var(--c-rose); margin-bottom:8px;"><i class="fas fa-minus"></i> Removed Skills</div>
                    <p style="font-size:0.88rem; color:var(--text-2);">${escapeHTML((data.deltas?.removed_skills || []).join(', ') || 'None detected')}</p>
                </div>
            </div>
        </div>`;
        showToast('Version Deltas Computed!', 'success');
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

/* =====================================================================
   TAB 7: AI ENHANCER & REWRITE BULLETS
   ===================================================================== */
async function runImprovement() {
    const file = document.getElementById('improve-file')?.files[0];
    const job = document.getElementById('improve-job')?.value || '';
    const div = document.getElementById('improve-results');

    if (!file) { showToast('Please select a resume file', 'error'); return; }
    if (!job) { showToast('Please enter a job description', 'error'); return; }

    div.style.display = 'block';
    div.innerHTML = skeletonHTML(6);
    showToast('Generating Strategic Resume Enhancements…', 'info');

    const fd = new FormData();
    fd.append('file', file);
    fd.append('job_description', job);
    fd.append('analysis_mode', currentAnalysisMode());

    try {
        const res = await fetch('/api/improve', { method: 'POST', body: fd });
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        const sections = [
            { key: 'missing_skills', icon: 'fas fa-search', label: 'Missing Skills', color: 'var(--c-rose)' },
            { key: 'experience_gaps', icon: 'fas fa-chart-gap', label: 'Experience Gaps', color: 'var(--c-amber)' },
            { key: 'format_improvements', icon: 'fas fa-paintbrush', label: 'Format Improvements', color: 'var(--c-cyan)' },
            { key: 'keywords_to_include', icon: 'fas fa-tags', label: 'Keywords to Include', color: 'var(--c-blue)' },
            { key: 'achievements_to_highlight', icon: 'fas fa-trophy', label: 'Achievements to Highlight', color: 'var(--c-green)' }
        ];

        let html = `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-lightbulb"></i> AI Enhancement Strategy</div></div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px;">`;
        sections.forEach(s => {
            const items = data[s.key] || [];
            if (!items.length) return;
            html += `
            <div style="background:var(--bg-input); border-radius:12px; padding:16px; border:1px solid var(--glass-border); border-top:3px solid ${s.color};">
                <div style="font-weight:800; color:${s.color}; margin-bottom:10px; font-size:0.9rem;"><i class="${s.icon}"></i> ${s.label}</div>
                <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                    ${items.map(it => `
                    <li style="display:flex; align-items:flex-start; gap:8px; font-size:0.84rem; color:var(--text-2);">
                        <i class="fas fa-chevron-right" style="color:${s.color}; margin-top:4px; font-size:0.7rem; flex-shrink:0;"></i>
                        <span>${escapeHTML(it)}</span>
                    </li>`).join('')}
                </ul>
            </div>`;
        });
        html += `</div></div>`;
        if (data.note) html += `<p style="font-size:0.8rem; color:var(--text-3); margin-top:10px; font-style:italic;">${escapeHTML(data.note)}</p>`;
        div.innerHTML = html;
        showToast('Enhancement Insights Ready!', 'success');
    } catch (e) {
        showToast('Error: ' + e.message, 'error');
    }
}

async function rewriteResumeBullets() {
    const file = document.getElementById('improve-file')?.files[0];
    const job = document.getElementById('improve-job')?.value.trim() || '';
    const results = document.getElementById('rewrite-results');
    const button = document.getElementById('rewrite-bullets-btn');

    if (!file) { showToast('Please select a resume file', 'error'); return; }
    if (!job) { showToast('Please enter a job description', 'error'); return; }

    results.style.display = 'block';
    results.innerHTML = skeletonHTML(3);
    button.disabled = true;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', job);
    formData.append('analysis_mode', currentAnalysisMode());

    try {
        const response = await fetch('/api/rewrite-bullets', { method: 'POST', body: formData });
        const data = await response.json();
        if (!response.ok || data.error) throw new Error(data.error || `Request failed (${response.status})`);

        const rewrites = Array.isArray(data.rewrites) ? data.rewrites : [];
        if (!rewrites.length) {
            results.innerHTML = `<div class="result-block"><p style="color:var(--text-2);">No resume bullets could be safely improved using the information provided.</p></div>`;
            showToast('No bullet rewrites found', 'info');
            return;
        }

        const cards = rewrites.map((item, index) => `
            <article style="background:var(--bg-input); border:1px solid var(--glass-border); border-radius:14px; padding:18px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <div style="color:var(--text-3); font-size:0.76rem; font-weight:800; text-transform:uppercase; letter-spacing:0.08em;">Suggestion ${index + 1}</div>
                    <button class="btn-subtle" onclick="navigator.clipboard.writeText('${escapeHTML(item.rewritten).replace(/'/g, "\\'")}').then(()=>showToast('Copied!','success'))" style="padding:3px 10px; font-size:0.75rem;">
                        <i class="fas fa-copy"></i> Copy
                    </button>
                </div>
                <div style="margin-bottom:10px;">
                    <div style="color:var(--text-3); font-size:0.75rem; font-weight:700; margin-bottom:4px;">ORIGINAL</div>
                    <p style="color:var(--text-2); font-size:0.88rem;">${escapeHTML(item.original)}</p>
                </div>
                <div style="margin-bottom:10px;">
                    <div style="color:var(--c-cyan); font-size:0.75rem; font-weight:700; margin-bottom:4px;">TAILORED BULLET</div>
                    <p style="color:var(--text-1); font-weight:600; font-size:0.92rem;">${escapeHTML(item.rewritten)}</p>
                </div>
                <p style="color:var(--text-3); font-size:0.82rem;"><i class="fas fa-circle-info"></i> ${escapeHTML(item.reason)}</p>
            </article>`).join('');

        results.innerHTML = `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-wand-magic-sparkles"></i> Job-Tailored Bullet Suggestions</div></div>
            <div style="display:grid; gap:12px;">${cards}</div>
        </div>`;
        showToast('Resume bullet suggestions ready!', 'success');
    } catch (error) {
        results.innerHTML = isQuotaExhaustedError(error.message)
            ? renderQuotaErrorCard(error.message, 'improve')
            : `<div class="result-block" style="border-color:var(--c-rose);"><p style="color:var(--c-rose);">${escapeHTML(error.message)}</p></div>`;
        showToast(error.message, 'error');
    } finally {
        button.disabled = false;
    }
}

/* =====================================================================
   TAB 8: COVER LETTER GENERATOR
   ===================================================================== */
async function generateCoverLetter() {
    const file = document.getElementById('cover-file')?.files[0];
    const job = document.getElementById('cover-job')?.value || '';
    const div = document.getElementById('cover-results');

    if (!file || !job) {
        showToast('Please provide both resume and job description', 'error');
        return;
    }

    div.style.display = 'block';
    div.innerHTML = skeletonHTML(8);
    showToast('Crafting Tailored Cover Letter…', 'info');

    const fd = new FormData();
    fd.append('file', file);
    fd.append('job_description', job);
    fd.append('analysis_mode', currentAnalysisMode());

    try {
        const res = await fetch('/api/cover-letter', { method: 'POST', body: fd });
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        div.innerHTML = `
        <div class="result-block">
            <div class="result-block-hd">
                <div class="result-block-title">
                    <i class="fas fa-file-signature"></i>
                    ${data.generation_mode === 'template' ? 'Cover Letter Template' : 'AI-Generated Cover Letter'}
                </div>
                <button class="btn-subtle" onclick="navigator.clipboard.writeText(document.getElementById('cover-text').textContent).then(()=>showToast('Copied to clipboard!','success'))">
                    <i class="fas fa-copy"></i> Copy Letter
                </button>
            </div>
            ${data.generation_mode === 'template' ? `<p style="color:var(--c-amber); font-size:0.84rem; margin-bottom:12px;"><i class="fas fa-circle-info"></i> ${escapeHTML(data.note || 'Generated in local template mode.')}</p>` : ''}
            <div id="cover-text" style="background:var(--bg-input); padding:22px; border-radius:12px; white-space:pre-wrap; line-height:1.85; font-size:0.92rem; color:var(--text-1); border:1px solid var(--glass-border);">${escapeHTML(data.cover_letter || '')}</div>
        </div>`;
        showToast('Cover letter ready!', 'success');
    } catch (e) {
        showToast(e.message, 'error');
    }
}

/* =====================================================================
   TAB 9: ATS SIMULATOR
   ===================================================================== */
async function runATS() {
    const file = document.getElementById('ats-file')?.files[0];
    const div = document.getElementById('ats-results');
    if (!file) { showToast('Please select a resume file', 'error'); return; }

    div.style.display = 'block';
    div.innerHTML = skeletonHTML(3);
    showToast('Simulating Raw ATS Parse…', 'info');

    const fd = new FormData();
    fd.append('file', file);

    try {
        const res = await fetch('/api/ats-simulator', { method: 'POST', body: fd });
        const data = await res.json();
        if (data.error) throw new Error(data.error);

        const raw = data.raw_text || '';
        const wordCount = raw.trim().split(/\s+/).filter(Boolean).length;
        const hasEmail = /[\w.-]+@[\w.-]+\.\w+/.test(raw);
        const hasPhone = /(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}/.test(raw);
        const hasLinkedIn = /linkedin\.com/i.test(raw);
        const hasGitHub = /github\.com/i.test(raw);

        const hasExp = /(experience|work history|employment|career)/i.test(raw);
        const hasEdu = /(education|university|college|degree|bachelor|master|b\.s|b\.e|b\.tech)/i.test(raw);
        const hasSkills = /(skills|technical proficiencies|core competencies|technologies)/i.test(raw);
        const hasProjects = /(projects|key initiatives|portfolio)/i.test(raw);

        const lines = raw.split(/\r?\n/).filter(l => l.trim().length > 15);
        const metricLines = lines.filter(l => /\d+%|\$\d+|\b\d+\s*(users|clients|ms|s|x|events|req|engineers|team)/i.test(l));
        const metricPct = lines.length ? Math.round((metricLines.length / lines.length) * 100) : 0;

        let atsScore = 100;
        if (!hasEmail) atsScore -= 15;
        if (!hasPhone) atsScore -= 10;
        if (!hasExp) atsScore -= 20;
        if (!hasEdu) atsScore -= 15;
        if (!hasSkills) atsScore -= 15;
        if (wordCount < 250) atsScore -= 15;
        else if (wordCount > 1400) atsScore -= 10;
        if (metricPct < 15) atsScore -= 10;
        atsScore = Math.max(30, Math.min(100, atsScore));

        const scoreColor = atsScore >= 85 ? 'var(--c-green)' : atsScore >= 70 ? 'var(--c-cyan)' : 'var(--c-amber)';
        const contactsFound = [hasEmail, hasPhone, hasLinkedIn, hasGitHub].filter(Boolean).length;
        const sectionsFound = [hasExp, hasEdu, hasSkills, hasProjects].filter(Boolean).length;

        div.innerHTML = `
        <!-- ATS PRE-FLIGHT COMPLIANCE SCORECARD -->
        <div class="result-block" style="border-color:${scoreColor}; margin-bottom:20px;">
            <div class="result-block-hd">
                <div class="result-block-title" style="color:${scoreColor};">
                    <i class="fas fa-shield-halved"></i> ATS Parseability &amp; Pre-Flight Scorecard
                </div>
                <div style="font-size:1.45rem; font-weight:900; color:${scoreColor}; font-family:var(--font-mono);">
                    <span class="count-up" data-target="${atsScore}">0</span>/100 ATS Index
                </div>
            </div>

            <div class="ats-audit-grid">
                <div class="ats-stat-box">
                    <div class="ats-stat-val" style="color:var(--c-cyan);"><span class="count-up" data-target="${wordCount}">0</span></div>
                    <div class="ats-stat-label">Word Count (Ideal: 450-900)</div>
                </div>
                <div class="ats-stat-box">
                    <div class="ats-stat-val" style="color:var(--c-green);"><span class="count-up" data-target="${metricPct}">0</span>%</div>
                    <div class="ats-stat-label">Quantified Metric Density</div>
                </div>
                <div class="ats-stat-box">
                    <div class="ats-stat-val" style="color:var(--c-indigo);">${contactsFound}/4</div>
                    <div class="ats-stat-label">Contact Points Verified</div>
                </div>
                <div class="ats-stat-box">
                    <div class="ats-stat-val" style="color:var(--c-purple);">${sectionsFound}/4</div>
                    <div class="ats-stat-label">Standard Sections Found</div>
                </div>
            </div>

            <div class="ats-checklist-grid">
                <div class="ats-check-item">
                    <div class="ats-check-left">
                        <i class="fas ${hasEmail && hasPhone ? 'fa-circle-check' : 'fa-circle-exclamation'}" style="color:${hasEmail && hasPhone ? 'var(--c-green)' : 'var(--c-amber)'};"></i>
                        <span>Contact Info (Email &amp; Phone)</span>
                    </div>
                    <span class="badge ${hasEmail && hasPhone ? 'high' : 'medium'}">${hasEmail && hasPhone ? 'PASS' : 'INCOMPLETE'}</span>
                </div>
                <div class="ats-check-item">
                    <div class="ats-check-left">
                        <i class="fas ${hasExp ? 'fa-circle-check' : 'fa-circle-xmark'}" style="color:${hasExp ? 'var(--c-green)' : 'var(--c-rose)'};"></i>
                        <span>Work Experience Section</span>
                    </div>
                    <span class="badge ${hasExp ? 'high' : 'none'}">${hasExp ? 'DETECTED' : 'MISSING'}</span>
                </div>
                <div class="ats-check-item">
                    <div class="ats-check-left">
                        <i class="fas ${hasEdu ? 'fa-circle-check' : 'fa-circle-xmark'}" style="color:${hasEdu ? 'var(--c-green)' : 'var(--c-rose)'};"></i>
                        <span>Education &amp; Credentials</span>
                    </div>
                    <span class="badge ${hasEdu ? 'high' : 'none'}">${hasEdu ? 'DETECTED' : 'MISSING'}</span>
                </div>
                <div class="ats-check-item">
                    <div class="ats-check-left">
                        <i class="fas ${hasSkills ? 'fa-circle-check' : 'fa-circle-xmark'}" style="color:${hasSkills ? 'var(--c-green)' : 'var(--c-rose)'};"></i>
                        <span>Skills &amp; Competencies Header</span>
                    </div>
                    <span class="badge ${hasSkills ? 'high' : 'none'}">${hasSkills ? 'DETECTED' : 'MISSING'}</span>
                </div>
                <div class="ats-check-item">
                    <div class="ats-check-left">
                        <i class="fas ${metricPct >= 15 ? 'fa-circle-check' : 'fa-circle-exclamation'}" style="color:${metricPct >= 15 ? 'var(--c-green)' : 'var(--c-amber)'};"></i>
                        <span>Measurable Impact ($ / % / metrics)</span>
                    </div>
                    <span class="badge ${metricPct >= 15 ? 'high' : 'medium'}">${metricPct >= 15 ? 'OPTIMAL' : 'LOW METRICS'}</span>
                </div>
                <div class="ats-check-item">
                    <div class="ats-check-left">
                        <i class="fas ${wordCount >= 300 && wordCount <= 1200 ? 'fa-circle-check' : 'fa-circle-exclamation'}" style="color:${wordCount >= 300 && wordCount <= 1200 ? 'var(--c-green)' : 'var(--c-amber)'};"></i>
                        <span>Optimal Text Volume</span>
                    </div>
                    <span class="badge ${wordCount >= 300 && wordCount <= 1200 ? 'high' : 'medium'}">${wordCount >= 300 && wordCount <= 1200 ? 'GOOD LENGTH' : 'ADJUST LENGTH'}</span>
                </div>
            </div>
        </div>

        <!-- RAW ATS TELEMETRY TERMINAL -->
        <div class="result-block ats-terminal-container" style="border-color:rgba(16, 185, 129, 0.4);">
            <div class="result-block-hd">
                <div class="result-block-title" style="color:var(--c-green);">
                    <i class="fas fa-terminal"></i> Raw ATS Telemetry Parser (Scanner View)
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="chip success" style="font-size:0.75rem;"><i class="fas fa-circle-dot"></i> PARSED SUCCESSFULLY</span>
                </div>
            </div>
            <p style="font-size:0.86rem; color:var(--text-2); margin-bottom:12px;">
                This represents exactly how traditional Applicant Tracking Systems (Workday, Greenhouse, Taleo) extract and tokenize your resume content.
            </p>
            <div class="ats-terminal">
                <div class="ats-terminal-header">
                    <div class="ats-terminal-dots">
                        <span class="ats-terminal-dot ats-dot-red"></span>
                        <span class="ats-terminal-dot ats-dot-yellow"></span>
                        <span class="ats-terminal-dot ats-dot-green"></span>
                    </div>
                    <div class="ats-terminal-title"><i class="fas fa-microchip"></i> ATS-PARSER-ENGINE // RAW TOKEN DUMP</div>
                    <div style="font-size:0.72rem; color:#94a3b8; font-family:var(--font-mono);">${escapeHTML(file.name)}</div>
                </div>
                <div class="ats-terminal-body">${escapeHTML(data.raw_text || '')}<span class="ats-blink-cursor"></span></div>
            </div>
        </div>`;
        showToast('ATS Simulation & Pre-Flight Scorecard Complete!', 'success');
    } catch (e) {
        showToast(e.message, 'error');
    }
}

/* =====================================================================
   TAB 10: MOCK INTERVIEW CHAT
   ===================================================================== */
let interviewHistory = [];

function appendInterviewMsg(role, text, mode = '') {
    const box = document.getElementById('chat-box');
    if (!box) return;
    const isUser = role === 'user';
    if (box.children.length === 1 && (box.children[0].textContent.includes('Start') || box.children[0].textContent.includes('Connecting') || box.children[0].textContent.includes('cleared'))) {
        box.innerHTML = '';
    }
    const msg = document.createElement('div');
    msg.className = `chat-msg ${isUser ? 'user' : 'ai'}`;
    const badgeHtml = mode === 'local_heuristic'
        ? ' <span style="font-size:0.65rem; background:rgba(16,185,129,0.15); color:var(--c-green); border:1px solid rgba(16,185,129,0.3); padding:1px 6px; border-radius:4px; font-weight:700;">Local Deterministic Mode</span>'
        : '';
    msg.innerHTML = `
        <div class="chat-sender">${isUser ? 'You' : 'Technical Recruiter'}${badgeHtml}</div>
        <div class="chat-bubble">${escapeHTML(text)}</div>`;
    box.appendChild(msg);
    box.scrollTop = box.scrollHeight;
}

function clearInterview() {
    interviewHistory = [];
    const box = document.getElementById('chat-box');
    if (box) box.innerHTML = `<div style="color:var(--text-3); text-align:center; font-size:0.9rem; margin:auto 0;">Interview cleared. Click "Start Interview" when ready!</div>`;
    showToast('Interview chat cleared', 'info');
}

async function startMockInterview() {
    interviewHistory = [];
    const box = document.getElementById('chat-box');
    if (box) box.innerHTML = `<div style="color:var(--text-3); text-align:center;"><i class="fas fa-spinner fa-spin"></i> Initializing technical recruiter interview session…</div>`;
    await callInterviewAPI('Hello, I am ready to begin the interview.');
}

async function sendInterviewMessage() {
    const input = document.getElementById('mock-input');
    const text = input ? input.value.trim() : '';
    if (!text) return;

    appendInterviewMsg('user', text);
    interviewHistory.push({ role: 'user', content: text });
    input.value = '';

    const box = document.getElementById('chat-box');
    const typing = document.createElement('div');
    typing.id = 'typing-indicator';
    typing.className = 'chat-msg ai';
    typing.innerHTML = `<div class="chat-sender">Technical Recruiter</div><div class="chat-bubble"><span class="typing-dots"><span>●</span><span>●</span><span>●</span></span></div>`;
    box.appendChild(typing);
    box.scrollTop = box.scrollHeight;

    await callInterviewAPI();
}

async function callInterviewAPI(initMsg = null) {
    const resume = document.getElementById('mock-resume')?.value || '';
    const job = document.getElementById('mock-job')?.value || '';

    if (!resume.trim() || !job.trim()) {
        showToast('Please provide both resume and job description (or click "Load Sample Profile")', 'error');
        const t = document.getElementById('typing-indicator');
        if (t) t.remove();
        return;
    }

    if (initMsg) interviewHistory.push({ role: 'user', content: initMsg });

    try {
        const res = await fetch('/api/interview-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ resume_text: resume, job_description: job, history: interviewHistory, analysis_mode: currentAnalysisMode() })
        });
        const data = await res.json();
        const t = document.getElementById('typing-indicator');
        if (t) t.remove();

        if (data.error && !data.reply) throw new Error(data.error);
        appendInterviewMsg('assistant', data.reply, data.generation_mode);
        interviewHistory.push({ role: 'assistant', content: data.reply });
    } catch (e) {
        showToast(e.message, 'error');
    }
}

/* =====================================================================
   TAB 11: CAREER PATH RECOMMENDATIONS
   ===================================================================== */
async function runCareerPaths() {
    const file = document.getElementById('career-file')?.files[0];
    const job = document.getElementById('career-job')?.value || '';
    const div = document.getElementById('career-results');

    if (!file) { showToast('Please upload your resume', 'error'); return; }

    div.style.display = 'block';
    div.innerHTML = skeletonHTML(6);
    showToast('Calculating Career Trajectories…', 'info');

    const fd = new FormData();
    fd.append('file', file);
    fd.append('job_description', job);
    fd.append('analysis_mode', currentAnalysisMode());

    try {
        const res = await fetch('/api/career-paths', { method: 'POST', body: fd });
        const data = await res.json();

        if (data.error && !data.paths) throw new Error(data.error);

        const paths = data.paths || [];
        const COLORS = ['var(--c-cyan)', 'var(--c-indigo)', 'var(--c-violet)'];
        const OUTLOOK_ICONS = { 'High': 'fas fa-arrow-trend-up', 'Very High': 'fas fa-rocket', 'Stable': 'fas fa-equals' };

        let html = `
        <div class="result-block">
            <div class="result-block-hd"><div class="result-block-title"><i class="fas fa-route"></i> Your Personalized Career Trajectories</div></div>
            <div class="career-grid">`;
        paths.forEach((p, i) => {
            const color = COLORS[i % COLORS.length];
            const icon = OUTLOOK_ICONS[p.growth_outlook] || 'fas fa-chart-line';
            html += `
            <div class="career-card" style="border-top:3px solid ${color};">
                <div class="career-match count-up" data-target="${p.match_pct || 0}" data-suffix="%" style="color:${color}; font-family:var(--font-mono);">0%</div>
                <div class="career-title">${escapeHTML(p.title)}</div>
                <div class="career-meta">
                    <span class="chip info"><i class="fas fa-clock"></i> ${escapeHTML(p.timeline)}</span>
                    <span class="chip"><i class="${icon}"></i> ${escapeHTML(p.growth_outlook)}</span>
                </div>
                <div style="background:var(--bg-card); border-radius:10px; padding:10px 14px; margin-bottom:12px; border-left:3px solid ${color};">
                    <div style="font-size:0.72rem; font-weight:800; color:var(--text-3); text-transform:uppercase; letter-spacing:0.06em;">Avg. Salary</div>
                    <div style="font-size:1.15rem; font-weight:900; color:${color}; font-family:var(--font-mono);">${escapeHTML(p.avg_salary)}</div>
                </div>
                ${p.key_skill ? `<div style="margin-bottom:12px;"><span class="chip ai"><i class="fas fa-star"></i> Core: ${escapeHTML(p.key_skill)}</span></div>` : ''}
                <div style="font-size:0.78rem; font-weight:800; color:var(--text-3); text-transform:uppercase; margin-bottom:8px;">Execution Steps</div>
                <ul class="career-steps">
                    ${(p.steps || []).map(s => `<li>${escapeHTML(s)}</li>`).join('')}
                </ul>
            </div>`;
        });
        html += `</div></div>`;
        div.innerHTML = html;
        animateRings();
        showToast('Career Paths Generated!', 'success');
    } catch (e) {
        if (isQuotaExhaustedError(e.message)) {
            div.innerHTML = renderQuotaErrorCard(e.message, 'career');
        } else {
            div.innerHTML = `<div class="result-block" style="border-color:var(--c-rose);"><p style="color:var(--c-rose);">${escapeHTML(e.message)}</p></div>`;
        }
        showToast(e.message, 'error');
    }
}

/* =====================================================================
   TAB 12: SALARY ESTIMATOR
   ===================================================================== */
async function runSalaryEstimate() {
    const file = document.getElementById('salary-file')?.files[0];
    const job = document.getElementById('salary-job')?.value || '';
    const div = document.getElementById('salary-results');

    if (!file) { showToast('Please upload your resume', 'error'); return; }
    if (!job) { showToast('Please enter a target job description', 'error'); return; }

    div.style.display = 'block';
    div.innerHTML = skeletonHTML(5);
    showToast('Benchmarking Market Compensation…', 'info');

    const fd = new FormData();
    fd.append('file', file);
    fd.append('job_description', job);
    fd.append('analysis_mode', currentAnalysisMode());

    try {
        const res = await fetch('/api/salary-estimate', { method: 'POST', body: fd });
        const data = await res.json();
        if (data.error && !data.estimated_range) throw new Error(data.error);

        const posClass = data.positioning === 'Above Market' ? 'above' : data.positioning === 'Below Market' ? 'below' : 'at-market';
        const posIcon = data.positioning === 'Above Market' ? 'fas fa-arrow-trend-up' : data.positioning === 'Below Market' ? 'fas fa-arrow-trend-down' : 'fas fa-equals';

        div.innerHTML = `
        <div class="result-block" style="border-color:rgba(16, 185, 129, 0.4);">
            <div class="result-block-hd"><div class="result-block-title" style="color:var(--c-green);"><i class="fas fa-coins"></i> Market Salary Intelligence</div></div>
            <div class="salary-hero">
                <div class="salary-range">${escapeHTML(data.estimated_range || 'N/A')}</div>
                <div style="color:var(--text-3); font-size:0.86rem; margin-bottom:10px;">Median Baseline: <strong style="color:var(--c-green);">${escapeHTML(data.median || 'N/A')}</strong></div>
                <span class="salary-pos ${posClass}"><i class="${posIcon}"></i> ${escapeHTML(data.positioning || 'At Market')}</span>
                ${data.experience_premium_pct ? `<div style="margin-top:10px; font-size:0.84rem; color:var(--text-3);">Experience Premium: <strong style="color:var(--c-cyan);">+<span class="count-up" data-target="${data.experience_premium_pct}">0</span>% above baseline</strong></div>` : ''}
            </div>

            <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:16px; margin-bottom:18px;">
                <div style="background:var(--bg-input); border-radius:12px; padding:16px; border:1px solid var(--glass-border);">
                    <div style="font-weight:800; color:var(--c-green); margin-bottom:10px; font-size:0.9rem;"><i class="fas fa-chart-bar"></i> Salary Drivers</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                        ${(data.salary_drivers || []).map(d => `<li style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:var(--text-2);"><i class="fas fa-check" style="color:var(--c-green); font-size:0.75rem;"></i>${escapeHTML(d)}</li>`).join('')}
                    </ul>
                </div>
                <div style="background:var(--bg-input); border-radius:12px; padding:16px; border:1px solid var(--glass-border);">
                    <div style="font-weight:800; color:var(--c-cyan); margin-bottom:10px; font-size:0.9rem;"><i class="fas fa-handshake"></i> Negotiation Leverage</div>
                    <ul style="list-style:none; display:flex; flex-direction:column; gap:8px;">
                        ${(data.negotiation_tips || []).map(t => `<li style="display:flex; align-items:flex-start; gap:8px; font-size:0.85rem; color:var(--text-2);"><i class="fas fa-lightbulb" style="color:var(--c-cyan); font-size:0.75rem; margin-top:3px; flex-shrink:0;"></i>${escapeHTML(t)}</li>`).join('')}
                    </ul>
                </div>
            </div>

            ${data.geographic_note ? `<div style="background:var(--bg-input); border-radius:10px; padding:12px 16px; border-left:3px solid var(--c-blue); border:1px solid var(--glass-border); border-left-width:3px;">
                <div style="font-size:0.8rem; font-weight:800; color:var(--text-3); margin-bottom:4px;"><i class="fas fa-location-dot"></i> Geographic Adjustment Note</div>
                <div style="font-size:0.88rem; color:var(--text-2);">${escapeHTML(data.geographic_note)}</div>
            </div>` : ''}
        </div>`;
        animateRings();
        showToast('Salary Estimate Ready!', 'success');
    } catch (e) {
        if (isQuotaExhaustedError(e.message)) {
            div.innerHTML = renderQuotaErrorCard(e.message, 'salary');
        } else {
            div.innerHTML = `<div class="result-block" style="border-color:var(--c-rose);"><p style="color:var(--c-rose);">${escapeHTML(e.message)}</p></div>`;
        }
        showToast(e.message, 'error');
    }
}

/* =====================================================================
   DOCUMENT INITIALIZATION & EVENT WIRING
   ===================================================================== */
document.addEventListener('DOMContentLoaded', () => {
    ThemeManager.init();
    TabSystem.init();
    updateAIStatus();
    updateHistoryBadge();

    // Setup all file dropzones
    setupDropzone('single-dz', 'single-file', 'single-doc-card', 'single-file-name');
    setupDropzone('batch-dz', 'batch-files');
    setupDropzone('improve-dz', 'improve-file');
    setupDropzone('cover-dz', 'cover-file');
    setupDropzone('ats-dz', 'ats-file');
    setupDropzone('career-dz', 'career-file');
    setupDropzone('salary-dz', 'salary-file');

    // Single remove button
    const singleRemove = document.getElementById('single-remove');
    if (singleRemove) {
        singleRemove.addEventListener('click', () => {
            const fileInput = document.getElementById('single-file');
            if (fileInput) fileInput.value = '';
            const docCard = document.getElementById('single-doc-card');
            if (docCard) docCard.style.display = 'none';
            AppState.activeResumeFile = null;
            AppState.activeResumeText = '';
            checkWorkspaceSyncBar(document.querySelector('.tab-btn.active')?.getAttribute('data-tab'));
        });
    }

    // Analysis mode switch notes
    const modeSelect = document.getElementById('analysis-mode');
    if (modeSelect) {
        modeSelect.addEventListener('change', e => {
            const isLocal = e.target.value === 'local';
            const noteEl = document.getElementById('analysis-mode-note');
            if (noteEl) {
                noteEl.textContent = isLocal
                    ? 'Local mode processes resumes deterministically on this machine without paid external LLMs. Cover letters use structured templates, and tips are rule-based.'
                    : 'AI-assisted mode leverages OpenAI GPT-4/3.5 models for deep qualitative rewrites, dynamic interviews, career trajectories, and salary benchmarking.';
            }
            updateAssistantModeBadge();
            showToast(`Switched to ${isLocal ? 'Local Deterministic' : 'AI-Assisted (OpenAI)'} mode`, 'info');
        });
    }

    // Mock interview Enter key
    const mockInput = document.getElementById('mock-input');
    if (mockInput) {
        mockInput.addEventListener('keydown', e => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendInterviewMessage();
            }
        });
    }

    // Floating Back to Top button
    const btt = document.getElementById('back-to-top');
    if (btt) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) btt.classList.add('show');
            else btt.classList.remove('show');
        });
        btt.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    // Character counter updates on textareas
    document.querySelectorAll('.form-textarea').forEach(tx => {
        const counter = document.getElementById(`${tx.id}-count`);
        if (counter) {
            tx.addEventListener('input', () => {
                counter.textContent = `${tx.value.length} chars`;
            });
        }
    });

    // Initialize Auth Welcome Pop-up and Navbar User State
    initAuthWelcomeModal();
    renderNavbarUserState();
    updateAssistantModeBadge();

    // Global keyboard shortcuts (ESC closes modals/assistant)
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
            closeAuthWelcomeModal();
            closeHistoryModal();
            const panel = document.getElementById('assistant-chat-panel');
            if (panel && panel.classList.contains('open')) {
                toggleAssistantWidget();
            }
        }
    });
});

/* =====================================================================
   AUTH POP-UP MODAL & NAVBAR USER ENGINE
   ===================================================================== */
function initAuthWelcomeModal() {
    const urlParams = new URLSearchParams(window.location.search);
    const authQuery = urlParams.get('auth');
    const nameQuery = urlParams.get('name');

    let storedEvent = null;
    try {
        const raw = localStorage.getItem('resumeai_auth_event');
        if (raw) storedEvent = JSON.parse(raw);
    } catch (e) {
        storedEvent = null;
    }

    const authType = authQuery || storedEvent?.type;
    if (!authType) return;

    let userName = nameQuery || storedEvent?.name || '';
    if (!userName || userName.trim() === '') {
        userName = 'Valued Member';
    }

    const modalBackdrop = document.getElementById('auth-welcome-modal-backdrop');
    const titleEl = document.getElementById('auth-welcome-title');
    const subEl = document.getElementById('auth-welcome-sub');
    const badgeEl = document.getElementById('auth-welcome-badge');
    const iconEl = document.getElementById('auth-welcome-icon');

    if (authType === 'signup') {
        if (titleEl) {
            titleEl.innerHTML = `Welcome, <span class="user-highlight">${escapeHtml(userName)}</span>!`;
        }
        if (subEl) {
            subEl.innerHTML = `Welcome to your new user account! Your account has been created successfully. Explore our 12 AI and deterministic analysis modules.`;
        }
        if (badgeEl) {
            badgeEl.innerHTML = `<i class="fas fa-sparkles"></i> New User Account Created`;
        }
        if (iconEl) {
            iconEl.innerHTML = `<i class="fas fa-crown"></i>`;
        }
    } else {
        // Login event
        if (titleEl) {
            titleEl.innerHTML = `Welcome back, <span class="user-highlight">${escapeHtml(userName)}</span>!`;
        }
        if (subEl) {
            subEl.innerHTML = `Great to see you again! Your intelligence workspace is ready to evaluate candidate resumes, run recruiter simulations, and optimize ATS scores.`;
        }
        if (badgeEl) {
            badgeEl.innerHTML = `<i class="fas fa-circle-check"></i> Authenticated Session`;
        }
        if (iconEl) {
            iconEl.innerHTML = `<i class="fas fa-user-check"></i>`;
        }
    }

    // Save active user profile if not already saved
    try {
        const existing = localStorage.getItem('resumeai_logged_in_user');
        if (!existing) {
            localStorage.setItem('resumeai_logged_in_user', JSON.stringify({
                name: userName,
                email: storedEvent?.email || ''
            }));
        }
    } catch (e) {
        console.error('Failed to save user in localStorage', e);
    }

    // Clear one-time auth event
    try {
        localStorage.removeItem('resumeai_auth_event');
    } catch (e) {}

    // Clean URL bar query parameters smoothly without reloading
    if (window.history && window.history.replaceState) {
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    // Show modal
    if (modalBackdrop) {
        modalBackdrop.classList.add('show');
    }
}

function closeAuthWelcomeModal() {
    const modalBackdrop = document.getElementById('auth-welcome-modal-backdrop');
    if (modalBackdrop) {
        modalBackdrop.classList.remove('show');
    }
}

function renderNavbarUserState() {
    const navUserContainer = document.getElementById('nav-user-container');
    if (!navUserContainer) return;

    let user = null;
    try {
        const raw = localStorage.getItem('resumeai_logged_in_user');
        if (raw) user = JSON.parse(raw);
    } catch (e) {
        user = null;
    }

    if (user && user.name) {
        const initials = user.name
            .split(' ')
            .filter(Boolean)
            .map(w => w[0])
            .join('')
            .slice(0, 2)
            .toUpperCase() || 'U';

        navUserContainer.innerHTML = `
            <div class="user-pill" title="Logged in as ${escapeHtml(user.name)}">
                <div class="user-avatar">${initials}</div>
                <span class="user-name">${escapeHtml(user.name)}</span>
                <button class="logout-btn" onclick="logoutUser()" title="Log out" aria-label="Log out">
                    <i class="fas fa-arrow-right-from-bracket"></i>
                </button>
            </div>
        `;
    } else {
        navUserContainer.innerHTML = `
            <a href="/login" class="nav-link" id="nav-signin-link">Sign In</a>
            <a href="/signup" class="nav-cta" id="nav-signup-link">Get Started <i class="fas fa-arrow-right"></i></a>
        `;
    }
}

function logoutUser() {
    try {
        localStorage.removeItem('resumeai_logged_in_user');
    } catch (e) {}
    renderNavbarUserState();
    showToast('You have been logged out successfully.', 'info');
}

/* =====================================================================
   AI ASSISTANT COPILOT ENGINE (100% Offline / Local Mode Ready)
   ===================================================================== */
const AssistantState = {
    isOpen: false,
    history: [],
    isSending: false
};

function toggleAssistantWidget() {
    const panel = document.getElementById('assistant-chat-panel');
    if (!panel) return;

    AssistantState.isOpen = !AssistantState.isOpen;
    if (AssistantState.isOpen) {
        panel.classList.add('open');
        updateAssistantModeBadge();
        const input = document.getElementById('assistant-input');
        if (input) {
            setTimeout(() => input.focus(), 150);
        }
        scrollAssistantToBottom();
    } else {
        panel.classList.remove('open');
    }
}

function updateAssistantModeBadge() {
    const mode = document.getElementById('analysis-mode')?.value || 'local';
    const badgeEl = document.getElementById('assistant-header-badge');
    const indicatorEl = document.getElementById('assistant-mode-indicator');
    const statusDot = document.getElementById('assistant-status-dot');

    if (badgeEl) {
        badgeEl.innerHTML = mode === 'local'
            ? '<span class="dot"></span> Local Mode (Offline Ready)'
            : '<span class="dot" style="background:#6366f1;"></span> AI Mode (OpenAI)';
    }
    if (indicatorEl) {
        indicatorEl.textContent = mode === 'local' ? 'Mode: Local Engine (Offline)' : 'Mode: OpenAI GPT';
    }
    if (statusDot) {
        statusDot.style.background = mode === 'local' ? '#10b981' : '#6366f1';
        statusDot.style.boxShadow = mode === 'local' ? '0 0 6px #10b981' : '0 0 6px #6366f1';
    }
}

function askQuickPrompt(text) {
    const panel = document.getElementById('assistant-chat-panel');
    if (panel && !panel.classList.contains('open')) {
        toggleAssistantWidget();
    }
    sendAssistantMessage(text);
}

function escapeHtml(text) {
    if (!text) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

function formatAssistantMessage(text) {
    if (!text) return '';
    let escaped = escapeHtml(text);

    // Code blocks
    escaped = escaped.replace(/```([\s\S]*?)```/g, '<pre style="background:rgba(0,0,0,0.45); padding:8px 12px; border-radius:8px; overflow-x:auto; margin:6px 0; font-family:var(--font-mono); font-size:0.8rem; border:1px solid rgba(148,163,184,0.15);">$1</pre>');
    // Inline code
    escaped = escaped.replace(/`([^`]+)`/g, '<code style="background:rgba(0,0,0,0.3); padding:2px 6px; border-radius:4px; font-family:var(--font-mono); font-size:0.85em; color:var(--c-cyan);">$1</code>');
    // Bold
    escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italic
    escaped = escaped.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    // Bullet points: lines starting with "- " or "* "
    escaped = escaped.replace(/^[\*\-]\s+(.*)$/gm, '<div style="display:flex; gap:6px; margin:3px 0;"><span style="color:var(--c-cyan);">•</span><span>$1</span></div>');
    // Numbered lists: lines starting with "1. ", "2. ", etc.
    escaped = escaped.replace(/^(\d+)\.\s+(.*)$/gm, '<div style="display:flex; gap:6px; margin:3px 0;"><strong style="color:var(--c-cyan); min-width:18px;">$1.</strong><span>$2</span></div>');
    // Double newlines
    escaped = escaped.replace(/\n\n/g, '<div style="height:8px;"></div>');
    // Single newlines
    escaped = escaped.replace(/\n/g, '<br>');

    return escaped;
}

async function sendAssistantMessage(presetMessage) {
    if (AssistantState.isSending) return;
    const input = document.getElementById('assistant-input');
    const userText = (presetMessage || input?.value || '').trim();
    if (!userText) return;

    if (!presetMessage && input) {
        input.value = '';
    }

    const messagesContainer = document.getElementById('assistant-messages');
    if (!messagesContainer) return;

    // Append User message
    const userMsgEl = document.createElement('div');
    userMsgEl.className = 'assistant-msg user';
    userMsgEl.textContent = userText;
    messagesContainer.appendChild(userMsgEl);

    // Append Typing indicator
    const typingEl = document.createElement('div');
    typingEl.className = 'assistant-msg bot assistant-typing';
    typingEl.id = 'assistant-typing-indicator';
    typingEl.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Consulting intelligence engine…';
    messagesContainer.appendChild(typingEl);
    scrollAssistantToBottom();

    AssistantState.isSending = true;
    const currentMode = document.getElementById('analysis-mode')?.value || 'local';

    try {
        const response = await fetch('/api/assistant-chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: userText,
                history: AssistantState.history.slice(-6),
                resume_context: AppState.activeResumeText || '',
                analysis_mode: currentMode
            })
        });

        const data = await response.json();
        typingEl.remove();

        const botReply = data.reply || "I'm sorry, I couldn't generate a response. Please try again.";
        const modeTag = data.mode === 'local' ? 'Local Engine · 100% Offline' : 'OpenAI Model';
        const botMsgEl = document.createElement('div');
        botMsgEl.className = 'assistant-msg bot';
        botMsgEl.innerHTML = `
            <div class="bot-mode-tag"><i class="fas fa-microchip"></i> ${modeTag}</div>
            <div>${formatAssistantMessage(botReply)}</div>
        `;
        messagesContainer.appendChild(botMsgEl);

        AssistantState.history.push({ role: 'user', content: userText });
        AssistantState.history.push({ role: 'assistant', content: botReply });
        scrollAssistantToBottom();
    } catch (err) {
        console.error('Assistant chat error:', err);
        typingEl.remove();
        const errEl = document.createElement('div');
        errEl.className = 'assistant-msg bot';
        errEl.innerHTML = `
            <div class="bot-mode-tag" style="color:var(--c-rose);"><i class="fas fa-triangle-exclamation"></i> Offline Fallback</div>
            <div>I encountered a network issue communicating with the local server. Please ensure the ResumeAI server is running.</div>
        `;
        messagesContainer.appendChild(errEl);
        scrollAssistantToBottom();
    } finally {
        AssistantState.isSending = false;
    }
}

function clearAssistantChat() {
    const messagesContainer = document.getElementById('assistant-messages');
    if (messagesContainer) {
        messagesContainer.innerHTML = `
            <div class="assistant-msg bot">
                <div class="bot-mode-tag"><i class="fas fa-microchip"></i> Local Copilot</div>
                <div>
                    👋 <strong>Conversation cleared.</strong><br>
                    How else can I assist your resume optimization, interview prep, or scoring review today?
                </div>
            </div>
        `;
    }
    AssistantState.history = [];
    showToast('Assistant conversation reset', 'info');
}

function scrollAssistantToBottom() {
    const body = document.getElementById('assistant-messages');
    if (body) {
        body.scrollTop = body.scrollHeight;
    }
}

/* =====================================================================
   GITHUB LIVE CODE EVIDENCE VERIFIER ENGINE
   ===================================================================== */
function loadGitHubDemo(username) {
    const userInput = document.getElementById('github-username-input');
    const resumeInput = document.getElementById('github-resume-input');
    if (userInput) userInput.value = username;

    if (username === 'alexchen-dev' && resumeInput && DemoProfiles.fullstack) {
        resumeInput.value = DemoProfiles.fullstack.content;
    } else if (username === 'torvalds' && resumeInput) {
        resumeInput.value = "Linus Torvalds\nCreator of Linux and Git\nCore Skills: C, Linux, Git, Operating Systems, Kernel Architecture, Low-level Systems.";
    }

    runGitHubVerification();
}

async function runGitHubVerification() {
    const userInput = document.getElementById('github-username-input');
    const resumeInput = document.getElementById('github-resume-input');
    const btn = document.getElementById('github-verify-btn');
    const resultsContainer = document.getElementById('github-results-container');

    const username = (userInput?.value || '').trim();
    if (!username) {
        showToast('Please enter a GitHub username or profile URL.', 'warning');
        if (userInput) userInput.focus();
        return;
    }

    const resumeText = (resumeInput?.value || AppState.activeResumeText || '').trim();

    const originalBtnHtml = btn ? btn.innerHTML : '';
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Verifying Code Repositories…';
    }

    try {
        const response = await fetch('/api/github-verify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: username,
                resume_text: resumeText
            })
        });

        const data = await response.json();

        if (!response.ok || data.error) {
            showToast(data.error || 'Failed to verify GitHub profile', 'error');
            return;
        }

        renderGitHubResults(data);
        if (resultsContainer) {
            resultsContainer.style.display = 'block';
            resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        showToast(`Code evidence verified for @${data.username} (${data.evidence_score}% score)!`, 'success');
    } catch (err) {
        console.error('GitHub verification error:', err);
        showToast('Error connecting to GitHub verification service.', 'error');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalBtnHtml;
        }
    }
}

function renderGitHubResults(data) {
    // 1. Hero Card
    const heroCard = document.getElementById('github-hero-card');
    if (heroCard) {
        heroCard.innerHTML = `
            <div class="github-hero-avatar-wrap">
                <img src="${escapeHtml(data.avatar_url || 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')}" alt="${escapeHtml(data.name)}" class="github-avatar" onerror="this.src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'">
            </div>
            <div>
                <div class="github-hero-name">
                    <span>${escapeHtml(data.name || data.username)}</span>
                    <a href="${escapeHtml(data.profile_url || 'https://github.com/' + data.username)}" target="_blank" rel="noopener" class="github-hero-handle">
                        @${escapeHtml(data.username)} <i class="fas fa-arrow-up-right-from-square"></i>
                    </a>
                </div>
                <div class="github-hero-bio">${escapeHtml(data.bio || 'Public software developer profile.')}</div>
                <div class="github-hero-stats">
                    <span class="github-hero-stat-pill"><i class="fas fa-code-branch" style="color:var(--c-cyan);"></i> <strong>${data.public_repos_count || 0}</strong> Repositories</span>
                    <span class="github-hero-stat-pill"><i class="fas fa-star" style="color:var(--c-amber);"></i> <strong>${data.total_stars || 0}</strong> Stars</span>
                    <span class="github-hero-stat-pill"><i class="fas fa-code-fork" style="color:var(--c-indigo);"></i> <strong>${data.total_forks || 0}</strong> Forks</span>
                    <span class="github-hero-stat-pill"><i class="fas fa-users" style="color:var(--c-emerald);"></i> <strong>${data.followers || 0}</strong> Followers</span>
                    <span class="github-hero-stat-pill"><i class="fas fa-location-dot"></i> ${escapeHtml(data.location || 'Global')}</span>
                </div>
            </div>
            <div class="github-hero-score-box">
                <div style="font-size:0.75rem; text-transform:uppercase; color:var(--text-3); font-weight:800; letter-spacing:0.06em; margin-bottom:4px;">
                    Code Evidence
                </div>
                <div class="github-hero-score-num" style="color:${data.tier_color || '#00f2fe'};">
                    ${data.evidence_score || 0}%
                </div>
                <div class="github-hero-tier-badge" style="background:${data.tier_color || '#00f2fe'}20; color:${data.tier_color || '#00f2fe'}; border:1px solid ${data.tier_color || '#00f2fe'}40;">
                    ${escapeHtml(data.tier_badge || 'VERIFIED')}
                </div>
            </div>
        `;
    }

    // 2. Verified Skills
    const verifiedList = document.getElementById('github-verified-skills-list');
    const verifiedBadge = document.getElementById('github-verified-count-badge');
    if (verifiedBadge) verifiedBadge.textContent = `${(data.verified_skills || []).length} Verified`;
    if (verifiedList) {
        if (!data.verified_skills || data.verified_skills.length === 0) {
            verifiedList.innerHTML = `<div style="color:var(--text-3); font-size:0.85rem; padding:10px 0;">No matching code artifacts found for listed resume skills.</div>`;
        } else {
            verifiedList.innerHTML = data.verified_skills.map(s => `
                <div class="github-skill-item">
                    <span class="github-skill-name">
                        <i class="fas fa-circle-check" style="color:var(--c-emerald);"></i>
                        ${escapeHtml(s.skill)}
                    </span>
                    <div class="github-skill-meta">
                        <span style="color:var(--c-amber);"><i class="fas fa-star"></i> ${s.stars || 0}</span>
                        <a href="${escapeHtml(s.top_repo_url)}" target="_blank" rel="noopener" class="github-skill-link" title="View proof repository">
                            <i class="fab fa-github"></i> ${escapeHtml(s.top_repo)} <i class="fas fa-arrow-up-right-from-square" style="font-size:0.65rem;"></i>
                        </a>
                    </div>
                </div>
            `).join('');
        }
    }

    // 3. Self-Reported (Unverified on GitHub)
    const selfList = document.getElementById('github-self-reported-list');
    const selfBadge = document.getElementById('github-self-reported-badge');
    if (selfBadge) selfBadge.textContent = `${(data.self_reported_skills || []).length} Unverified`;
    if (selfList) {
        if (!data.self_reported_skills || data.self_reported_skills.length === 0) {
            selfList.innerHTML = `<div style="color:var(--text-3); font-size:0.85rem; padding:10px 0;">All claimed technical skills have public code proof!</div>`;
        } else {
            selfList.innerHTML = data.self_reported_skills.map(s => `
                <div class="github-skill-item">
                    <span class="github-skill-name" style="color:var(--text-2);">
                        <i class="fas fa-circle-info" style="color:var(--c-amber);"></i>
                        ${escapeHtml(s.skill)}
                    </span>
                    <span style="font-size:0.75rem; color:var(--text-3); font-style:italic;">Self-reported</span>
                </div>
            `).join('');
        }
    }

    // 4. Discovered Hidden Strengths
    const hiddenList = document.getElementById('github-hidden-skills-list');
    const hiddenBadge = document.getElementById('github-hidden-badge');
    if (hiddenBadge) hiddenBadge.textContent = `${(data.discovered_hidden_skills || []).length} Discovered`;
    if (hiddenList) {
        if (!data.discovered_hidden_skills || data.discovered_hidden_skills.length === 0) {
            hiddenList.innerHTML = `<div style="color:var(--text-3); font-size:0.85rem; padding:10px 0;">All GitHub technologies are already represented on your resume!</div>`;
        } else {
            hiddenList.innerHTML = data.discovered_hidden_skills.map(h => `
                <div class="github-skill-item" style="border-color:rgba(0,242,254,0.25);">
                    <div>
                        <span class="github-skill-name" style="color:var(--c-cyan);">
                            <i class="fas fa-sparkles"></i>
                            ${escapeHtml(h.skill)}
                        </span>
                        <div style="font-size:0.72rem; color:var(--text-3); margin-top:2px;">${escapeHtml(h.recommendation)}</div>
                    </div>
                    <span class="github-lang-pill" style="font-size:0.7rem;">+${h.repo_count} repos</span>
                </div>
            `).join('');
        }
    }

    // 5. Language Distribution Bars
    const langBars = document.getElementById('github-lang-bars');
    if (langBars) {
        if (!data.language_distribution || data.language_distribution.length === 0) {
            langBars.innerHTML = `<div style="color:var(--text-3); font-size:0.85rem;">No primary language detected.</div>`;
        } else {
            langBars.innerHTML = data.language_distribution.slice(0, 5).map(l => `
                <div class="github-lang-row">
                    <div class="github-lang-header">
                        <span>${escapeHtml(l.language)}</span>
                        <span style="color:var(--c-cyan); font-family:var(--font-mono); font-weight:700;">${l.percentage}%</span>
                    </div>
                    <div class="github-lang-bar-wrap">
                        <div class="github-lang-bar-fill" style="width:${l.percentage}%;"></div>
                    </div>
                </div>
            `).join('');
        }
    }

    // 6. Recruiter Note
    const recruiterNote = document.getElementById('github-recruiter-note');
    if (recruiterNote) {
        recruiterNote.innerHTML = formatAssistantMessage(data.recruiter_summary || '');
    }

    // 7. Repositories Grid
    const reposGrid = document.getElementById('github-repos-grid');
    const repoBadge = document.getElementById('github-repo-count-badge');
    if (repoBadge) repoBadge.textContent = `${(data.highlighted_projects || []).length} Repositories`;
    if (reposGrid) {
        if (!data.highlighted_projects || data.highlighted_projects.length === 0) {
            reposGrid.innerHTML = `<div style="color:var(--text-3); font-size:0.85rem;">No public repositories available.</div>`;
        } else {
            reposGrid.innerHTML = data.highlighted_projects.map(r => `
                <div class="github-repo-card">
                    <div>
                        <div class="github-repo-top">
                            <a href="${escapeHtml(r.url)}" target="_blank" rel="noopener" class="github-repo-title">
                                <i class="fab fa-github"></i> ${escapeHtml(r.name)}
                            </a>
                            <span class="github-lang-pill">${escapeHtml(r.language)}</span>
                        </div>
                        <p class="github-repo-desc">${escapeHtml(r.description)}</p>
                    </div>
                    <div class="github-repo-bottom">
                        <div style="display:flex; gap:10px;">
                            <span><i class="fas fa-star" style="color:var(--c-amber);"></i> ${r.stars}</span>
                            <span><i class="fas fa-code-fork" style="color:var(--c-indigo);"></i> ${r.forks}</span>
                        </div>
                        <a href="${escapeHtml(r.url)}" target="_blank" rel="noopener" class="btn-subtle" style="padding:3px 8px; font-size:0.75rem; text-decoration:none;">
                            View Source <i class="fas fa-arrow-up-right-from-square" style="font-size:0.65rem;"></i>
                        </a>
                    </div>
                </div>
            `).join('');
        }
    }
}

/* =====================================================================
   ATS ERROR AUDIT & RESUME REBUILDER ENGINE
   ===================================================================== */
function loadSampleIntoRebuilder() {
    if (DemoProfiles.fullstack) {
        AppState.activeResumeText = DemoProfiles.fullstack.content;
        const jobInput = document.getElementById('improve-job');
        if (jobInput && DemoProfiles.fullstack.jobDescription) {
            jobInput.value = DemoProfiles.fullstack.jobDescription;
        }
        showToast('Loaded sample profile into ATS Rebuilder. Auditing errors now…', 'info');
        runAtsResumeRebuild();
    }
}

async function runAtsResumeRebuild() {
    const fileInput = document.getElementById('improve-file');
    const jobInput = document.getElementById('improve-job');
    const btn = document.getElementById('rebuild-ats-resume-btn');
    const container = document.getElementById('rebuild-resume-results');

    const file = fileInput?.files[0] || AppState.activeResumeFile;
    const resumeText = AppState.activeResumeText;
    const jobDescription = (jobInput?.value || AppState.activeJobDescription || '').trim();
    const mode = document.getElementById('analysis-mode')?.value || 'local';

    if (!file && !resumeText) {
        showToast('Please upload a resume file or load a sample resume first.', 'warning');
        return;
    }

    const originalBtnHtml = btn ? btn.innerHTML : '';
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Auditing Errors &amp; Rebuilding ATS Resume…';
    }

    try {
        let response;
        if (file) {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('job_description', jobDescription);
            formData.append('analysis_mode', mode);
            response = await fetch('/api/ats-rebuild-resume', { method: 'POST', body: formData });
        } else {
            response = await fetch('/api/ats-rebuild-resume', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    resume_text: resumeText,
                    job_description: jobDescription,
                    analysis_mode: mode
                })
            });
        }

        const data = await response.json();
        if (!response.ok || data.error) {
            showToast(data.error || 'Failed to rebuild ATS resume', 'error');
            return;
        }

        AppState.lastRebuiltResume = data;
        // Auto-sync the polished resume into AppState so all other tools benefit from the new resume
        AppState.activeResumeText = data.rebuilt_plain_text;

        renderAtsRebuildResults(data);
        if (container) {
            container.style.display = 'block';
            container.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        showToast(`ATS resume reconstructed! Score jumped from ${data.ats_score_before}% to ${data.ats_score_after}%.`, 'success');
    } catch (err) {
        console.error('ATS Rebuild Error:', err);
        showToast('Network error during ATS resume rebuilding.', 'error');
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalBtnHtml;
        }
    }
}

function renderAtsRebuildResults(data) {
    const container = document.getElementById('rebuild-resume-results');
    if (!container) return;

    // Convert markdown into rich semantic HTML for the ATS resume sheet
    const lines = (data.rebuilt_markdown || '').split('\n');
    let sheetHtml = '';

    sheetHtml += `<div class="ats-sheet-name">${escapeHtml(data.candidate_name || 'Candidate Name')}</div>`;
    sheetHtml += `<div class="ats-sheet-title">${escapeHtml(data.professional_title || 'Software Engineer')}</div>`;
    sheetHtml += `<div class="ats-sheet-contact">${escapeHtml(data.sections?.header || '')}</div>`;

    // Professional Summary
    sheetHtml += `<div class="ats-sheet-section-title">Professional Summary</div>`;
    sheetHtml += `<p style="margin:6px 0 14px; font-size:0.9rem; line-height:1.55; color:#1e293b;">${escapeHtml(data.sections?.summary || '')}</p>`;

    // Technical Skills
    sheetHtml += `<div class="ats-sheet-section-title">Core Competencies &amp; Technical Skills</div>`;
    const skillsLines = (data.sections?.skills || '').split('\n');
    sheetHtml += `<div style="font-size:0.88rem; line-height:1.6; margin-bottom:14px; color:#1e293b;">`;
    skillsLines.forEach(l => {
        if (l.trim()) {
            const parts = l.split(':');
            const cat = parts[0].replace(/\*\*/g, '').trim();
            const rest = parts.slice(1).join(':').trim();
            sheetHtml += `<div><strong>${escapeHtml(cat)}:</strong> ${escapeHtml(rest)}</div>`;
        }
    });
    sheetHtml += `</div>`;

    // Experience
    sheetHtml += `<div class="ats-sheet-section-title">Professional Experience</div>`;
    const expBlocks = (data.sections?.experience || '').split('\n\n');
    expBlocks.forEach(b => {
        const bLines = b.split('\n');
        if (bLines.length >= 2) {
            const headerLine = bLines[0].replace('### ', '').replace(/\*\*/g, '').trim();
            const dateLine = bLines[1].replace(/\*/g, '').trim();
            sheetHtml += `
                <div class="ats-sheet-role-header">
                    <strong>${escapeHtml(headerLine)}</strong>
                    <span>${escapeHtml(dateLine)}</span>
                </div>
                <ul class="ats-sheet-bullets">
            `;
            for (let i = 2; i < bLines.length; i++) {
                const bullet = bLines[i].replace(/^-\s*/, '').trim();
                if (bullet) {
                    sheetHtml += `<li>${escapeHtml(bullet)}</li>`;
                }
            }
            sheetHtml += `</ul>`;
        }
    });

    // Projects
    sheetHtml += `<div class="ats-sheet-section-title">Key Projects &amp; Open Source</div>`;
    const projBlocks = (data.sections?.projects || '').split('\n\n');
    projBlocks.forEach(b => {
        const pLines = b.split('\n');
        if (pLines.length >= 1) {
            const pTitle = pLines[0].replace('### ', '').trim();
            sheetHtml += `<div style="font-weight:700; font-size:0.92rem; margin-top:8px; color:#0f172a;">${escapeHtml(pTitle)}</div><ul class="ats-sheet-bullets">`;
            for (let i = 1; i < pLines.length; i++) {
                const bullet = pLines[i].replace(/^-\s*/, '').trim();
                if (bullet) {
                    sheetHtml += `<li>${escapeHtml(bullet)}</li>`;
                }
            }
            sheetHtml += `</ul>`;
        }
    });

    // Education
    sheetHtml += `<div class="ats-sheet-section-title">Education &amp; Credentials</div>`;
    const eduLines = (data.sections?.education || '').split('\n');
    if (eduLines.length >= 1) {
        const deg = eduLines[0].replace('### ', '').trim();
        const school = eduLines.length > 1 ? eduLines[1].replace(/\*/g, '').trim() : '';
        sheetHtml += `
            <div class="ats-sheet-role-header">
                <strong>${escapeHtml(deg)}</strong>
                <span>${escapeHtml(school)}</span>
            </div>
        `;
    }

    // Build the Complete DOM structure
    container.innerHTML = `
        <!-- Score Jump & Improvements Banner -->
        <div class="ats-rebuilder-score-banner">
            <div>
                <span class="badge-optional" style="background:rgba(16,185,129,0.2); color:#34d399; margin-bottom:8px; display:inline-block;">
                    <i class="fas fa-sparkles"></i> ATS Repair Audit Complete
                </span>
                <h3 style="font-size:1.35rem; font-weight:800; color:#ffffff; margin:0 0 6px;">
                    Resume Repaired &amp; Rebuilt into ATS-Friendly Format
                </h3>
                <p style="font-size:0.88rem; color:var(--text-2); max-width:650px; line-height:1.5; margin:0;">
                    ${escapeHtml(data.improvements_summary)}
                </p>
            </div>
            <div class="ats-score-meter-wrap">
                <div class="ats-score-badge-before">
                    <span style="font-size:0.72rem; text-transform:uppercase; font-weight:700;">Before</span>
                    <span class="score-val">${data.ats_score_before}%</span>
                </div>
                <div class="ats-score-arrow"><i class="fas fa-arrow-right"></i></div>
                <div class="ats-score-badge-after">
                    <span style="font-size:0.72rem; text-transform:uppercase; font-weight:800;">Rebuilt ATS</span>
                    <span class="score-val">${data.ats_score_after}%</span>
                </div>
            </div>
        </div>

        <!-- Errors Audited & Repaired Accordion/List -->
        <div class="result-block" style="border-color: rgba(0, 242, 254, 0.35); margin-bottom:20px;">
            <div class="metric-header">
                <span class="metric-title"><i class="fas fa-bug-slash" style="color:var(--c-cyan);"></i> Diagnosed &amp; Repaired Weaknesses (${data.errors_count || 0})</span>
                <span class="metric-badge" style="background:rgba(16,185,129,0.15); color:#34d399; border:1px solid rgba(16,185,129,0.3);">
                    100% Repaired
                </span>
            </div>
            <div class="ats-errors-summary-list" style="margin-top:14px;">
                ${(data.errors_fixed || []).map(err => `
                    <div class="ats-error-card-item">
                        <div class="ats-error-top-row">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <span class="ats-error-category-pill ${err.severity}">${err.severity}</span>
                                <strong style="color:#ffffff; font-size:0.9rem;">${escapeHtml(err.title)}</strong>
                            </div>
                            <span class="ats-error-fix-pill">
                                <i class="fas fa-circle-check"></i> ${escapeHtml(err.fix_applied)}
                            </span>
                        </div>
                        <div style="font-size:0.82rem; color:var(--text-2); line-height:1.45;">
                            ${escapeHtml(err.description)}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>

        <!-- The Rebuilt ATS Resume Document Card -->
        <div class="ats-resume-sheet-container">
            <div class="ats-resume-toolbar">
                <div style="display:flex; align-items:center; gap:10px;">
                    <span style="font-weight:700; color:#ffffff; font-size:0.95rem;">
                        <i class="fas fa-file-shield" style="color:var(--c-cyan);"></i> Rebuilt ATS-Standard Resume
                    </span>
                    <span class="badge-optional" style="background:rgba(16,185,129,0.18); color:#34d399;">Single-Column Guaranteed ATS Compatible</span>
                </div>
                <div style="display:flex; gap:8px; flex-wrap:wrap;">
                    <button class="btn-subtle" onclick="downloadAtsResumePdf()">
                        <i class="fas fa-file-pdf" style="color:var(--c-rose);"></i> Download PDF
                    </button>
                    <button class="btn-subtle" onclick="downloadAtsResumeTxt()">
                        <i class="fas fa-file-arrow-down" style="color:var(--c-cyan);"></i> Download TXT
                    </button>
                    <button class="btn-subtle" onclick="copyAtsResumeText()">
                        <i class="fas fa-copy"></i> Copy Resume
                    </button>
                    <button class="btn-subtle" onclick="syncRebuiltResumeToWorkspace()">
                        <i class="fas fa-link"></i> Sync to Workspace
                    </button>
                </div>
            </div>

            <!-- The Rendered White Sheet Preview -->
            <div class="ats-resume-sheet" id="ats-resume-sheet-view">
                ${sheetHtml}
            </div>
        </div>
    `;
}

function downloadAtsResumePdf() {
    window.print();
}

function downloadAtsResumeTxt() {
    const data = AppState.lastRebuiltResume;
    if (!data || !data.rebuilt_plain_text) {
        showToast('No rebuilt resume data found.', 'warning');
        return;
    }
    const filename = `${(data.candidate_name || 'ats_resume').toLowerCase().replace(/\s+/g, '_')}_ats_rebuilt.txt`;
    const blob = new Blob([data.rebuilt_plain_text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast(`Downloaded ${filename}!`, 'success');
}

function copyAtsResumeText() {
    const data = AppState.lastRebuiltResume;
    if (!data || !data.rebuilt_plain_text) {
        showToast('No rebuilt resume data found.', 'warning');
        return;
    }
    navigator.clipboard.writeText(data.rebuilt_plain_text)
        .then(() => showToast('Full ATS-friendly resume copied to clipboard!', 'success'))
        .catch(() => showToast('Failed to copy to clipboard', 'error'));
}

function syncRebuiltResumeToWorkspace() {
    const data = AppState.lastRebuiltResume;
    if (!data || !data.rebuilt_plain_text) return;
    AppState.activeResumeText = data.rebuilt_plain_text;
    showToast('Rebuilt ATS resume synchronized across all 13 tools!', 'success');
}
