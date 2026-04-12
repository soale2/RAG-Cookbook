import React from 'react';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import { useColorMode } from '@docusaurus/theme-common';
import styles from './index.module.css';

// ─── Data ────────────────────────────────────────────────────────────────────

const FOUNDATIONS = [
  {
    num: '00',
    title: 'Setup',
    desc: 'Install Ollama, pull nomic-embed-text and llama3.2, verify everything works.',
  },
  {
    num: '01',
    title: 'Embeddings',
    desc: 'Vector spaces, cosine similarity, and why L2 normalization matters.',
  },
  {
    num: '02',
    title: 'Chunking',
    desc: 'Document loading strategies, overlap, and how chunk size affects retrieval quality.',
  },
  {
    num: '03',
    title: 'Vector Stores',
    desc: 'FAISS vs ChromaDB, flat vs approximate indexing, when each makes sense.',
  },
];

const TRACKS = [
  {
    id: 'naive-rag',
    title: 'Naive RAG',
    desc: 'The foundational pipeline. Retrieve the most relevant chunks from a vector store, pass them to an LLM, get grounded answers.',
    modules: ['01 — Retrieval', '02 — Generation', '03 — Cloud Models'],
    status: 'active',
    href: '/naive-rag/01-retrieval',
  },
  {
    id: 'advanced-rag',
    title: 'Advanced RAG',
    desc: 'Query rewriting, hybrid search, reranking, and evaluation. Go beyond the naive baseline.',
    modules: [],
    status: 'soon',
  },
  {
    id: 'agentic-rag',
    title: 'Agentic RAG',
    desc: 'LLM-driven retrieval — the model decides what to retrieve, when, and how to combine sources.',
    modules: [],
    status: 'soon',
  },
  {
    id: 'graph-rag',
    title: 'Graph RAG',
    desc: 'Retrieval over knowledge graphs. Captures entity relationships that chunk-based search misses.',
    modules: [],
    status: 'soon',
  },
];

// ─── Curriculum diagram ───────────────────────────────────────────────────────

function CurriculumDiagram() {
  const { colorMode } = useColorMode();
  const isDark = colorMode === 'dark';

  const green       = isDark ? '#504945' : '#1e5c3e';
  const greenBg     = isDark ? '#3c3836' : '#164730';
  const muted       = isDark ? '#665c54' : '#b8c4bc';
  const lineSolid   = isDark ? '#8ec07c' : '#6b9e83';
  const lineFaint   = isDark ? '#504945' : '#c4cfc8';
  const textOnGreen = isDark ? '#ebdbb2' : '#f0f5f2';
  const textFaint   = isDark ? '#a89984' : '#8aaa92';

  return (
    <svg
      viewBox="0 0 340 210"
      className={styles.diagram}
      aria-label="Curriculum structure: Foundations leads to four tracks"
      role="img"
    >
      {/* ── Foundations box ── */}
      <rect x="30" y="12" width="280" height="62" rx="5" fill={greenBg} />
      <text
        x="170" y="37"
        textAnchor="middle"
        fill={textOnGreen}
        fontSize="10.5" fontWeight="700"
        fontFamily="DM Sans, system-ui, sans-serif"
        letterSpacing="2.5"
      >
        FOUNDATIONS
      </text>
      <text
        x="170" y="56"
        textAnchor="middle"
        fill={textOnGreen}
        fontSize="9" opacity="0.68"
        fontFamily="DM Sans, system-ui, sans-serif"
      >
        Setup · Embeddings · Chunking · Vectors
      </text>

      {/* ── Trunk ── */}
      <line x1="170" y1="74" x2="170" y2="104" stroke={lineSolid} strokeWidth="1.5" />

      {/* ── Branch ── */}
      <line x1="52" y1="104" x2="288" y2="104" stroke={lineSolid} strokeWidth="1.5" />

      {/* ── Drop lines ── */}
      <line x1="52"  y1="104" x2="52"  y2="126" stroke={lineSolid} strokeWidth="1.5" />
      <line x1="130" y1="104" x2="130" y2="126" stroke={lineFaint} strokeWidth="1"   strokeDasharray="3 3" />
      <line x1="210" y1="104" x2="210" y2="126" stroke={lineFaint} strokeWidth="1"   strokeDasharray="3 3" />
      <line x1="288" y1="104" x2="288" y2="126" stroke={lineFaint} strokeWidth="1"   strokeDasharray="3 3" />

      {/* ── Track boxes ── */}
      {/* Naive RAG — active */}
      <rect x="16"  y="126" width="72" height="58" rx="4" fill={green} />
      {/* Advanced */}
      <rect x="94"  y="126" width="72" height="58" rx="4" fill="none" stroke={muted} strokeWidth="1.5" />
      {/* Agentic */}
      <rect x="174" y="126" width="72" height="58" rx="4" fill="none" stroke={muted} strokeWidth="1.5" />
      {/* Graph */}
      <rect x="252" y="126" width="72" height="58" rx="4" fill="none" stroke={muted} strokeWidth="1.5" />

      {/* ── Track labels ── */}
      <text x="52"  y="151" textAnchor="middle" fill={textOnGreen} fontSize="9.5" fontWeight="600" fontFamily="DM Sans, system-ui, sans-serif">Naive</text>
      <text x="52"  y="166" textAnchor="middle" fill={textOnGreen} fontSize="9.5" fontWeight="600" fontFamily="DM Sans, system-ui, sans-serif">RAG</text>

      <text x="130" y="151" textAnchor="middle" fill={textFaint} fontSize="9.5" fontWeight="500" fontFamily="DM Sans, system-ui, sans-serif">Advanced</text>
      <text x="130" y="166" textAnchor="middle" fill={textFaint} fontSize="9"   fontFamily="DM Sans, system-ui, sans-serif">RAG</text>

      <text x="210" y="151" textAnchor="middle" fill={textFaint} fontSize="9.5" fontWeight="500" fontFamily="DM Sans, system-ui, sans-serif">Agentic</text>
      <text x="210" y="166" textAnchor="middle" fill={textFaint} fontSize="9"   fontFamily="DM Sans, system-ui, sans-serif">RAG</text>

      <text x="288" y="151" textAnchor="middle" fill={textFaint} fontSize="9.5" fontWeight="500" fontFamily="DM Sans, system-ui, sans-serif">Graph</text>
      <text x="288" y="166" textAnchor="middle" fill={textFaint} fontSize="9"   fontFamily="DM Sans, system-ui, sans-serif">RAG</text>

    </svg>
  );
}

// ─── Hero ─────────────────────────────────────────────────────────────────────

function Hero() {
  return (
    <section className={styles.hero}>
      <div className={styles.heroInner}>
        <div className={styles.heroText}>
          <div className={styles.pills}>
            <span className={styles.pill}>Python</span>
            <span className={styles.pillDivider} aria-hidden="true">·</span>
            <span className={styles.pill}>Local-first</span>
            <span className={styles.pillDivider} aria-hidden="true">·</span>
            <span className={styles.pill}>Ollama + Gemini</span>
          </div>

          <h1 className={styles.heroHeading}>
            <span className={styles.ragWord}>RAG</span>
            <span className={styles.heroSub}>Complete Study Guide</span>
          </h1>

          <p className={styles.heroBody}>
            A structured curriculum for Python developers. Build Retrieval-Augmented
            Generation systems from first principles — across multiple architectures,
            from naive pipelines to agentic and graph-based retrieval.
          </p>

          <div className={styles.heroCtas}>
            <Link to="/foundations/00-setup" className={styles.btnPrimary}>
              Start with Foundations
            </Link>
            <a
              href="https://github.com/soale2/RAG-Cookbook"
              className={styles.btnGhost}
              target="_blank"
              rel="noopener noreferrer"
            >
              View on GitHub ↗
            </a>
          </div>
        </div>

        <div className={styles.heroVisual}>
          <CurriculumDiagram />
        </div>
      </div>
    </section>
  );
}

// ─── Foundations ─────────────────────────────────────────────────────────────

function FoundationsSection() {
  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <span className={styles.eyebrow}>Start here</span>
          <h2 className={styles.sectionTitle}>Foundations</h2>
          <p className={styles.sectionSubtitle}>
            Core concepts shared across every RAG variant. Work through these before picking a track.
          </p>
        </div>

        <div className={styles.foundationsGrid}>
          {FOUNDATIONS.map((mod) => (
            <div key={mod.num} className={styles.foundationCell}>
              <span className={styles.modNum}>{mod.num}</span>
              <h3 className={styles.modTitle}>{mod.title}</h3>
              <p className={styles.modDesc}>{mod.desc}</p>
            </div>
          ))}
        </div>

        <div className={styles.sectionCta}>
          <Link to="/foundations/00-setup" className={styles.btnPrimary}>
            Begin Foundations →
          </Link>
        </div>
      </div>
    </section>
  );
}

// ─── Tracks ───────────────────────────────────────────────────────────────────

function TracksSection() {
  return (
    <section className={`${styles.section} ${styles.sectionShaded}`}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <span className={styles.eyebrow}>After foundations</span>
          <h2 className={styles.sectionTitle}>Choose Your Track</h2>
          <p className={styles.sectionSubtitle}>
            Projects are cumulative within each track — by the final module you have a complete, working system.
          </p>
        </div>

        <div className={styles.tracksGrid}>
          {TRACKS.map((track) => (
            <div
              key={track.id}
              className={`${styles.trackCard} ${track.status === 'soon' ? styles.trackCardSoon : ''}`}
            >
              <div className={styles.trackTop}>
                <h3 className={styles.trackTitle}>{track.title}</h3>
                {track.status === 'active'
                  ? <span className={styles.badgeActive}>Active</span>
                  : <span className={styles.badgeSoon}>Coming soon</span>
                }
              </div>
              <p className={styles.trackDesc}>{track.desc}</p>
              {track.modules.length > 0 && (
                <ul className={styles.trackModules}>
                  {track.modules.map((m) => <li key={m}>{m}</li>)}
                </ul>
              )}
              {track.status === 'active' && track.href && (
                <Link to={track.href} className={styles.trackCta}>
                  Start this track →
                </Link>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── How it works ─────────────────────────────────────────────────────────────

function HowItWorksSection() {
  const steps = [
    {
      n: '01',
      label: 'Theory',
      body: 'Each module opens with a focused explanation — the why and how, not just the what. Concepts are kept tight and precise.',
    },
    {
      n: '02',
      label: 'Exercises',
      body: 'Small, targeted coding tasks that isolate one idea at a time. Build intuition before taking on complexity.',
    },
    {
      n: '03',
      label: 'Project',
      body: 'A cumulative build that extends across the whole track. The final module produces a complete, working system.',
    },
  ];

  return (
    <section className={styles.section}>
      <div className={styles.container}>
        <div className={styles.sectionHeader}>
          <span className={styles.eyebrow}>Structure</span>
          <h2 className={styles.sectionTitle}>Each module includes</h2>
        </div>

        <div className={styles.stepsGrid}>
          {steps.map((step, i) => (
            <div key={step.n} className={styles.step}>
              {i < steps.length - 1 && <div className={styles.stepConnector} aria-hidden="true" />}
              <div className={styles.stepNumWrap}>
                <span className={styles.stepNum}>{step.n}</span>
              </div>
              <h3 className={styles.stepLabel}>{step.label}</h3>
              <p className={styles.stepBody}>{step.body}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// ─── Get started ──────────────────────────────────────────────────────────────

function GetStartedSection() {
  return (
    <section className={`${styles.section} ${styles.getStarted}`}>
      <div className={styles.container}>
        <p className={styles.getStartedEyebrow}>Prerequisites</p>
        <h2 className={styles.getStartedTitle}>Ready to build?</h2>
        <p className={styles.getStartedBody}>
          You need Python 3.10+, ~8 GB of free disk space for Ollama model weights, and about 30 minutes
          to complete the setup module. Everything else is explained as you go.
        </p>
        <Link to="/foundations/00-setup" className={styles.btnPrimary}>
          Go to Setup →
        </Link>
      </div>
    </section>
  );
}

// ─── Page ─────────────────────────────────────────────────────────────────────

export default function Home() {
  return (
    <Layout
      title="RAG Complete Study Guide"
      description="A structured curriculum for Python developers building Retrieval-Augmented Generation systems from first principles."
    >
      <Hero />
      <main>
        <FoundationsSection />
        <TracksSection />
        <HowItWorksSection />
        <GetStartedSection />
      </main>
    </Layout>
  );
}
