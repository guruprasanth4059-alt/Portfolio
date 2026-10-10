/**
 * Guruprasanth — Portfolio Scripts
 * Handles interactions: Theme toggle, navigation, modals, and notifications
 */

document.addEventListener('DOMContentLoaded', () => {
  // Project Details Data
  const projectsData = {
    manas: {
      title: 'Manas Suraksha',
      subtitle: 'AI-Powered Mental Health Monitoring & Distress Prediction System',
      badgeClass: 'project-card-pink',
      image: 'assets/project-manas.png',
      tags: ['AI/ML', 'Full-Stack', 'Mobile', 'FastAPI', 'PyTorch', 'SMS/IVRS'],
      overview: 'Manas Suraksha is an AI-assisted mental well-being monitoring platform designed to provide accessible, empathetic, and continuous psychological support to survivors navigating difficult reporting and recovery journeys. It integrates ethical distress prediction algorithms with offline SMS and IVRS fallback for uninterrupted rural accessibility.',
      keyFeatures: [
        'Ethical distress signal detection using natural language processing',
        'Hybrid online web experience with offline SMS and IVRS support for low-bandwidth regions',
        'Multilingual interface supporting regional vernacular languages',
        'End-to-end encryption preserving user privacy and anonymity'
      ]
    },
    cashflow: {
      title: 'Cashflow',
      subtitle: '30-Day Cash Flow Forecasting for Small Businesses',
      badgeClass: 'project-card-teal',
      image: 'assets/project-cashflow.png',
      tags: ['React', 'Node.js', 'Supabase', 'Time Series ML', 'Tailwind CSS'],
      overview: 'Cashflow is an intelligent financial analytics and predictive forecasting workspace crafted for small and medium enterprises. It aggregates revenue streams, recurring expenditures, and pending invoices to provide rolling 30-day liquidity projections with automated risk alerts.',
      keyFeatures: [
        'Interactive 30-day forward liquidity forecast charts',
        'Scenario simulation: model impact of delayed receivables or emergency expenses',
        'Automated early warning anomaly detection for pending cash crunches',
        'Integrated real-time database synchronization with Supabase'
      ]
    },
    eco: {
      title: 'Eco Verzz AI',
      subtitle: 'AI-Powered Environmental Monitoring & Detection',
      badgeClass: 'project-card-green',
      image: 'assets/project-eco.png',
      tags: ['AI/ML', 'Python', 'FastAPI', 'Express', 'Supabase', 'Computer Vision'],
      overview: 'Eco Verzz AI pairs computer vision models with geospatial analysis to detect deforestation, pollution hotspots, and urban green cover variations. It helps researchers and environmental initiatives monitor ecological changes and make data-driven sustainability decisions.',
      keyFeatures: [
        'Computer vision pipelines detecting canopy loss and vegetation stress',
        'FastAPI backend for high-throughput model inference',
        'Interactive geospatial map overlays illustrating environmental shifts',
        'Automated metric reporting and carbon footprint estimation tools'
      ]
    },
    fundfit: {
      title: 'FundFit AI',
      subtitle: 'Mutual Fund Evaluation & Investment Advisory',
      badgeClass: 'project-card-purple',
      image: 'assets/project-fundfit.png',
      tags: ['Next.js', 'Python', 'Supabase', 'Quantitative Finance', 'Explainable AI'],
      overview: 'FundFit AI is a quantitative advisory tool that evaluates mutual funds based on dynamic market conditions and personalized investor risk appetites. Utilizing explainable AI metrics, it translates complex alpha, beta, and Sharpe ratios into clear, actionable portfolio recommendations.',
      keyFeatures: [
        'Personalized risk-profile questionnaire and portfolio alignment score',
        'Adaptive benchmarks comparing funds across varying market cycles',
        'Explainable AI breakdowns clarifying the reasoning behind fund ratings',
        'Responsive dashboard developed with Next.js and Supabase'
      ]
    }
  };

  // 1. Theme Management (Dark / Light)
  const themeToggle = document.getElementById('themeToggle');
  const body = document.body;

  const savedTheme = localStorage.getItem('guru_theme') || 'dark';
  body.setAttribute('data-theme', savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = body.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      body.setAttribute('data-theme', newTheme);
      localStorage.setItem('guru_theme', newTheme);
      showToast(`Switched to ${newTheme} theme`);
    });
  }

  // 2. Mobile Menu Toggle
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const sidebar = document.getElementById('sidebar');
  const sidebarBackdrop = document.getElementById('sidebarBackdrop');

  function openSidebar() {
    sidebar.classList.add('open');
    sidebarBackdrop.classList.add('active');
  }

  function closeSidebar() {
    sidebar.classList.remove('open');
    sidebarBackdrop.classList.remove('active');
  }

  if (mobileMenuBtn && sidebar && sidebarBackdrop) {
    mobileMenuBtn.addEventListener('click', () => {
      if (sidebar.classList.contains('open')) {
        closeSidebar();
      } else {
        openSidebar();
      }
    });

    sidebarBackdrop.addEventListener('click', closeSidebar);
  }

  // Close sidebar on link click on mobile
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', () => {
      if (window.innerWidth <= 960) {
        closeSidebar();
      }
    });
  });

  // 3. Scrollspy for Active Navigation Link
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY + 200;

    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      const id = sec.getAttribute('id');

      if (scrollPosition >= top && scrollPosition < top + height) {
        navItems.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('data-section') === id) {
            link.classList.add('active');
          }
        });
      }
    });
  });

  // 4. Project Modal
  const projectModal = document.getElementById('projectModal');
  const modalContent = document.getElementById('modalProjectContent');
  const closeProjectModal = document.getElementById('closeProjectModal');

  document.querySelectorAll('.project-details-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const projectId = btn.getAttribute('data-project');
      const data = projectsData[projectId];

      if (data && projectModal && modalContent) {
        modalContent.innerHTML = `
          <div style="border-radius: 12px; overflow: hidden; margin-bottom: 20px; border: 1px solid var(--border-subtle);">
            <img src="${data.image}" alt="${data.title}" style="width: 100%; height: 160px; object-fit: cover;">
          </div>
          <h2 style="font-size: 24px; font-weight: 800; margin-bottom: 4px; color: var(--text-primary);">${data.title}</h2>
          <p style="font-size: 13.5px; font-weight: 600; color: var(--accent-pink); margin-bottom: 16px;">${data.subtitle}</p>
          <p style="font-size: 14px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 20px;">${data.overview}</p>
          
          <h4 style="font-size: 14px; font-weight: 700; margin-bottom: 10px; color: var(--text-primary);">Key Architectural Features:</h4>
          <ul style="padding-left: 20px; font-size: 13.5px; color: var(--text-secondary); line-height: 1.7; margin-bottom: 24px;">
            ${data.keyFeatures.map(f => `<li>${f}</li>`).join('')}
          </ul>

          <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 24px;">
            ${data.tags.map(t => `<span class="badge" style="padding: 4px 10px;">${t}</span>`).join('')}
          </div>

          <div style="display: flex; gap: 12px;">
            <a href="#contact" class="btn btn-primary" onclick="document.getElementById('projectModal').classList.remove('active');">
              <span>Discuss Project</span>
              <span class="arrow">→</span>
            </a>
          </div>
        `;

        projectModal.classList.add('active');
        projectModal.setAttribute('aria-hidden', 'false');
      }
    });
  });

  if (closeProjectModal && projectModal) {
    closeProjectModal.addEventListener('click', () => {
      projectModal.classList.remove('active');
      projectModal.setAttribute('aria-hidden', 'true');
    });

    projectModal.addEventListener('click', (e) => {
      if (e.target === projectModal) {
        projectModal.classList.remove('active');
        projectModal.setAttribute('aria-hidden', 'true');
      }
    });
  }

  // 5. Send Message Modal
  const contactModal = document.getElementById('contactModal');
  const openMessageModalBtn = document.getElementById('openMessageModalBtn');
  const closeContactModal = document.getElementById('closeContactModal');
  const contactForm = document.getElementById('contactForm');

  if (openMessageModalBtn && contactModal) {
    openMessageModalBtn.addEventListener('click', () => {
      contactModal.classList.add('active');
      contactModal.setAttribute('aria-hidden', 'false');
    });
  }

  if (closeContactModal && contactModal) {
    closeContactModal.addEventListener('click', () => {
      contactModal.classList.remove('active');
      contactModal.setAttribute('aria-hidden', 'true');
    });

    contactModal.addEventListener('click', (e) => {
      if (e.target === contactModal) {
        contactModal.classList.remove('active');
        contactModal.setAttribute('aria-hidden', 'true');
      }
    });
  }

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      contactModal.classList.remove('active');
      contactModal.setAttribute('aria-hidden', 'true');
      contactForm.reset();
      showToast('Message sent successfully! Guruprasanth will connect with you soon.');
    });
  }

  // 6. Email Channel Card Copy Action
  const contactEmailBtn = document.getElementById('contactEmailBtn');
  if (contactEmailBtn) {
    contactEmailBtn.addEventListener('click', (e) => {
      const email = 'guruprasanth4059@gmail.com';
      if (navigator.clipboard) {
        navigator.clipboard.writeText(email).then(() => {
          showToast('Email address copied to clipboard!');
        }).catch(() => {
          // fallback to default mailto behavior
        });
      }
    });
  }

  // 7. Back to Top Button
  const backToTopBtn = document.getElementById('backToTopBtn');
  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }

  // 8. Toast Notification Utility
  const toastNotification = document.getElementById('toastNotification');
  let toastTimeout;

  function showToast(message) {
    if (!toastNotification) return;
    toastNotification.textContent = message;
    toastNotification.classList.add('show');

    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
      toastNotification.classList.remove('show');
    }, 3200);
  }
});
