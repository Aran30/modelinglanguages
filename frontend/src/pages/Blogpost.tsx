import React from "react";
import "./Blogpost.css";

// Content curated from modeling-languages.com to keep the experience grounded in real articles.
const featuredArticle = {
  title: "Modeling skills for AI agents thanks to MCP support",
  excerpt:
    "The MCP connector lets AI agents navigate the BESSER low-code platform, generate diagrams, and keep models synchronized with their prompts.",
  author: "Gwendal Jouneaux",
  date: "Dec 19, 2025",
  readingTime: "6 min read",
  categories: ["(meta)modeling", "tools"],
  link: "https://modeling-languages.com/mcp-for-agentic-lowcode/",
};

const curatedPosts = [
  {
    title: "The B-UML Dataset Has Arrived",
    excerpt:
      "A 5k-model corpus curated for benchmarking UML tooling, meta-model discovery, and AI-assisted modeling prompts.",
    author: "Fitash Ul-Haq",
    date: "Jan 20, 2026",
    categories: ["empirical studies", "UML & OCL"],
    link: "https://modeling-languages.com/b-uml-dataset/",
  },
  {
    title: "An open-source No-Code GUI Editor for BESSER",
    excerpt:
      "Drag-and-drop dashboards land inside the same model repository, so UI experiments never drift away from their DSL definitions.",
    author: "Ivan Alfonso",
    date: "Nov 15, 2025",
    categories: ["DSLs", "code generation"],
    link: "https://modeling-languages.com/no-code-gui-editor/",
  },
  {
    title: "Ask Safely! Query LLMs Without Leaking KG Data",
    excerpt:
      "Masking sensitive knowledge-graph slices before prompt time is becoming a must-have practice for regulated digital twins.",
    author: "Mauro Dalle Lucca Tosi",
    date: "Dec 7, 2025",
    categories: ["AI", "data privacy"],
    link: "https://modeling-languages.com/privacy-queyr-knowledge-graph/",
  },
];

const deepDiveSeries = [
  {
    title: "ModelFed: a federated protocol for cross-platform modeling",
    description:
      "ActivityPub-inspired federation for exchanging model deltas among heterogeneous repositories.",
    link: "https://modeling-languages.com/modelfed-federated-protocol-collaborative-crossplatform-modeling/",
  },
  {
    title: "Towards Sustainability Model Cards",
    description:
      "A DSL that captures energy budgets and carbon intensity metrics for ML pipelines right next to their requirements.",
    link: "https://modeling-languages.com/sustainability-model-cards-dsl/",
  },
  {
    title: "Modeling Human-Agent Collaborative Workflows",
    description:
      "Extending BPMN with agent swimlanes to choreograph hybrid teams and automated assistants.",
    link: "https://modeling-languages.com/modeling-human-agent-collaborative-workflows-extending-bpmn/",
  },
];

const timelineUpdates = [
  { label: "Dataset releases", value: "+2", detail: "new public corpora since Sept" },
  { label: "Tool launches", value: "5", detail: "major OSS drops in 90 days" },
  { label: "Gov & policy", value: "3", detail: "guidelines covering AI safety" },
];

const resourceSpotlights = [
  {
    title: "Low-code handbook",
    summary: "A field guide to teaching modeling-first thinking to delivery teams.",
    link: "https://modeling-languages.com/tag/low-code/",
  },
  {
    title: "Model-driven AI Starter Kits",
    summary: "Pragmatic bundles mixing DSL templates, MCP scripts, and CLI recipes.",
    link: "https://modeling-languages.com/category/topic/ai/",
  },
  {
    title: "Community office hours",
    summary: "Monthly live session hosted by Jordi Cabot. Bring your DSL headaches.",
    link: "https://modeling-languages.com/page/2/?et_blog",
  },
];

const tagCloud = [
  "UML",
  "DSLs",
  "Model-Driven AI",
  "BESSER",
  "Governance",
  "Education",
  "Sustainability",
  "Agentic workflows",
];

const newsletterPoints = [
  "Fresh posts every Wednesday with opinionated summaries",
  "Hand-picked modeling meetups and CFP deadlines",
  "Downloadable cheat-sheets for teaching modeling fundamentals",
];

const Blogpost: React.FC = () => {
  return (
    <div className="blog-shell" id="blogpost">
      <aside className="blog-nav">
        <p className="nav-kicker">Since 2010</p>
        <h1 className="nav-title">Modeling Languages Dispatch</h1>
        <p className="nav-subheading">
          Signals, essays, and datasets curated from
          <span> modeling-languages.com</span>
        </p>
        <div className="nav-divider" />
        <ul className="nav-metrics">
          <li>
            <strong>220+</strong>
            <span>Deep dives</span>
          </li>
          <li>
            <strong>35</strong>
            <span>Contributors</span>
          </li>
          <li>
            <strong>48k</strong>
            <span>Monthly readers</span>
          </li>
        </ul>
        <a className="nav-link" href="/home">
          Back to Home
        </a>
        <p className="nav-note">
          Content references belong to their original authors. We simply distill the highlights for experimentation and research teams.
        </p>
      </aside>
      <main className="blog-main">
        <section className="hero">
          <p className="eyebrow">Field Report • Winter 2026</p>
          <h2>{featuredArticle.title}</h2>
          <p className="hero-excerpt">{featuredArticle.excerpt}</p>
          <div className="hero-meta">
            <span>
              {featuredArticle.author} · {featuredArticle.date}
            </span>
            <span>{featuredArticle.readingTime}</span>
            <div className="hero-tags">
              {featuredArticle.categories.map((tag) => (
                <span key={tag}>{tag}</span>
              ))}
            </div>
          </div>
          <div className="hero-actions">
            <a href={featuredArticle.link} target="_blank" rel="noreferrer" className="primary-action">
              Read on modeling-languages.com
            </a>
            <button className="ghost-action" type="button">
              Save briefing
            </button>
          </div>
        </section>

        <section className="feature-grid">
          <article className="feature-card">
            <h3>What we are tracking</h3>
            <p>
              MCP endpoints are becoming the lingua franca for model-aware copilots. The latest post shows how structural
              validations, diagram renders, and deployment scripts now live in the same low-code workspace.
            </p>
            <ul>
              <li>Agent testing with executable DSL snippets</li>
              <li>Diagram diffs surfaced directly inside prompts</li>
              <li>Governance hooks so regulated teams can audit AI edits</li>
            </ul>
          </article>
          <div className="feature-panel">
            <h4>Release cadence</h4>
            <p>Key signals spotted across the site during the last quarter:</p>
            <div className="panel-stats">
              {timelineUpdates.map((item) => (
                <div key={item.label}>
                  <strong>{item.value}</strong>
                  <span>{item.label}</span>
                  <p>{item.detail}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="posts-grid" aria-label="curated posts">
          {curatedPosts.map((post) => (
            <article className="post-card" key={post.title}>
              <p className="card-eyebrow">Latest on the blog</p>
              <h3>{post.title}</h3>
              <p>{post.excerpt}</p>
              <div className="card-meta">
                <span>
                  {post.author} · {post.date}
                </span>
                <div className="card-tags">
                  {post.categories.map((category) => (
                    <span key={category}>{category}</span>
                  ))}
                </div>
              </div>
              <a href={post.link} target="_blank" rel="noreferrer" className="text-link">
                Open article ↗
              </a>
            </article>
          ))}
        </section>

        <section className="deep-dive" aria-label="deep dive series">
          <div>
            <p className="eyebrow">Deep-dive series</p>
            <h3>Where modeling meets AI operations</h3>
            <p>
              These long-form pieces from the community dig into interoperability, sustainability, and socio-technical governance. Keep
              them bookmarked for team discussions.
            </p>
            <ul className="timeline">
              {deepDiveSeries.map((entry) => (
                <li key={entry.title}>
                  <a href={entry.link} target="_blank" rel="noreferrer">
                    <strong>{entry.title}</strong>
                    <span>{entry.description}</span>
                  </a>
                </li>
              ))}
            </ul>
          </div>
          <div className="tag-stack">
            <h4>Topics dominating the inbox</h4>
            <div className="chips">
              {tagCloud.map((tag) => (
                <span key={tag}>{tag}</span>
              ))}
            </div>
            <h4>Upcoming investigations</h4>
            <ol>
              <li>Agent-first diagram reviews inside MCP consoles</li>
              <li>Curricula that blend UML, DSLs, and prompt engineering</li>
              <li>Lifecycle carbon budgets for AI-enhanced modeling</li>
            </ol>
          </div>
        </section>

        <section className="newsletter" aria-label="newsletter">
          <div>
            <p className="eyebrow">Newsletter</p>
            <h3>Modeling Languages Dispatch</h3>
            <p>
              A weekly note that stitches together research-grade modeling practices with the pragmatic workflows teams are adopting right now.
            </p>
            <ul>
              {newsletterPoints.map((point) => (
                <li key={point}>{point}</li>
              ))}
            </ul>
          </div>
          <form className="newsletter-form">
            <label htmlFor="newsletter-email">Stay in the loop</label>
            <input id="newsletter-email" name="email" type="email" placeholder="you@studio.dev" />
            <button type="submit">Subscribe</button>
            <small>No spam. Only modeling intel.</small>
          </form>
        </section>

        <section className="resource-gallery" aria-label="resources">
          {resourceSpotlights.map((resource) => (
            <article key={resource.title} className="resource-card">
              <h4>{resource.title}</h4>
              <p>{resource.summary}</p>
              <a href={resource.link} target="_blank" rel="noreferrer" className="text-link">
                Explore resource ↗
              </a>
            </article>
          ))}
        </section>
      </main>
    </div>
  );
};

export default Blogpost;
