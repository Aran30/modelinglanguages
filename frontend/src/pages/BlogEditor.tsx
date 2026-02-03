import React, { FormEvent, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./BlogEditor.css";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";
const DEFAULT_IMAGE = "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=1200&q=80";

interface BlogEditorState {
  title: string;
  authorName: string;
  content: string;
  image: string;
}

const BlogEditor: React.FC = () => {
  const [formValues, setFormValues] = useState<BlogEditorState>({
    title: "",
    authorName: "",
    content: "",
    image: "",
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormValues((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!formValues.title.trim() || !formValues.authorName.trim() || !formValues.content.trim()) {
      setError("Please complete the title, author, and content fields.");
      return;
    }

    setSubmitting(true);
    setError(null);

    const payload = {
      title: formValues.title.trim(),
      authorName: formValues.authorName.trim(),
      content: formValues.content.trim(),
      image: formValues.image.trim() || DEFAULT_IMAGE,
      timestamp: new Date().toISOString().split("T")[0],
      hasComments: [],
    };

    try {
      await axios.post(`${API_BASE}/blogpost/`, payload);
      setSuccess("Blog post published.");
      setFormValues({ title: "", authorName: "", content: "", image: "" });
      window.setTimeout(() => navigate("/home"), 800);
    } catch (err) {
      if (axios.isAxiosError(err) && err.response) {
        const detail = (err.response.data as { detail?: string }).detail;
        setError(detail || "The server rejected this post. Please try again.");
      } else {
        setError("Unable to publish right now. Check your connection and try again.");
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="editor-shell">
      <form className="editor-panel" onSubmit={handleSubmit}>
        <p className="eyebrow">New entry</p>
        <h2>Create a modeling blog post</h2>
        <p className="editor-subtitle">Timestamp is captured automatically when you publish.</p>
        <label htmlFor="title">Title</label>
        <input
          id="title"
          name="title"
          type="text"
          placeholder="e.g., Modeling skills for AI agents"
          value={formValues.title}
          onChange={handleChange}
          required
        />
        <label htmlFor="authorName">Author</label>
        <input
          id="authorName"
          name="authorName"
          type="text"
          placeholder="Your name or team"
          value={formValues.authorName}
          onChange={handleChange}
          required
        />
        <label htmlFor="image">Cover image URL</label>
        <input
          id="image"
          name="image"
          type="url"
          placeholder="https://"
          value={formValues.image}
          onChange={handleChange}
        />
        <label htmlFor="content">Content</label>
        <textarea
          id="content"
          name="content"
          rows={8}
          placeholder="Share your findings, diagrams, datasets, or progress updates..."
          value={formValues.content}
          onChange={handleChange}
          required
        />
        {error && (
          <div className="editor-alert error" role="alert">
            {error}
          </div>
        )}
        {success && (
          <div className="editor-alert success" role="status">
            {success}
          </div>
        )}
        <div className="editor-actions">
          <button type="button" className="ghost-action" onClick={() => navigate("/home")} disabled={submitting}>
            Cancel
          </button>
          <button type="submit" className="primary-action" disabled={submitting}>
            {submitting ? "Publishing..." : "Publish"}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BlogEditor;
