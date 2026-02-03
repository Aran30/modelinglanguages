import React, { useCallback, useEffect, useMemo, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { BlogPost } from "../types/blog";
import { BlogCard } from "../components/blog/BlogCard";
import "./Home.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const Home: React.FC = () => {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const loadPosts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get<BlogPost[]>(`${API_BASE}/blogpost/?detailed=true`);
      setPosts(Array.isArray(response.data) ? response.data : []);
    } catch (err) {
      console.error("Failed to load blog posts", err);
      setError("Unable to load the blog feed right now. Please try again.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadPosts();
  }, [loadPosts]);

  const sortedPosts = useMemo(() => {
    return [...posts].sort((a, b) => {
      const left = new Date(a.timestamp).getTime();
      const right = new Date(b.timestamp).getTime();
      return right - left;
    });
  }, [posts]);

  const handleAddBlog = () => {
    navigate("/blog/create");
  };

  return (
    <div className="home-shell">
      <section className="home-hero">
        <p className="eyebrow">All-hands Dispatch</p>
        <h1>Modeling Languages Blogpad</h1>
        <p>
          Capture every modeling insight, low-code discovery, and research drop on a living canvas. Your posts land inside the same
          repository powering the blog homepage.
        </p>
        <div className="hero-actions">
          <button className="primary-action" type="button" onClick={handleAddBlog}>
            Add Blog
          </button>
                <button className="ghost-action" type="button" onClick={loadPosts} disabled={loading}>
                  {loading ? "Refreshing..." : "Refresh feed"}
          </button>
        </div>
      </section>

      <section className="home-stream" aria-live="polite">
              {loading && <div className="home-state">Loading community entries...</div>}
        {!loading && error && <div className="home-state error">{error}</div>}
        {!loading && !error && sortedPosts.length === 0 && (
          <div className="home-state">No blog posts yet. Be the first to announce a modeling story.</div>
        )}
        {!loading && !error && sortedPosts.length > 0 && (
          <div className="cards-grid">
            {sortedPosts.map((post) => (
              <BlogCard key={post.id} post={post} />
            ))}
          </div>
        )}
      </section>

      <button className="add-blog-floating" type="button" onClick={handleAddBlog}>
        + Add Blog
      </button>
    </div>
  );
};

export default Home;
