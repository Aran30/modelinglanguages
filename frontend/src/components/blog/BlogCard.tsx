import React, { useMemo, useState } from "react";
import { BlogPost } from "../../types/blog";
import "./BlogCard.css";

interface BlogCardProps {
  post: BlogPost;
}

const FALLBACK_IMAGE =
  "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=1200&q=80";

const formatDate = (timestamp: string): string => {
  const parsed = new Date(timestamp);
  if (Number.isNaN(parsed.getTime())) {
    return timestamp;
  }
  return parsed.toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

export const BlogCard: React.FC<BlogCardProps> = ({ post }) => {
  const [expanded, setExpanded] = useState(false);
  const coverImage = useMemo(() => (post.image && post.image.trim().length ? post.image : FALLBACK_IMAGE), [post.image]);
  const snippet = useMemo(() => post.content.trim(), [post.content]);

  return (
    <article className="blog-card">
      <div className="blog-card__media" style={{ backgroundImage: `url(${coverImage})` }} aria-label={post.title} />
      <div className="blog-card__body">
        <p className="blog-card__eyebrow">{formatDate(post.timestamp)}</p>
        <h3>{post.title}</h3>
        <p className={`blog-card__content ${expanded ? "expanded" : "collapsed"}`}>{snippet}</p>
      </div>
      <div className="blog-card__footer">
        <div>
          <span className="blog-card__author">{post.authorName}</span>
          {Array.isArray(post.hasComments) && (
            <span className="blog-card__meta">{post.hasComments.length} comments</span>
          )}
        </div>
        <button type="button" onClick={() => setExpanded((state) => !state)} className="blog-card__toggle">
          {expanded ? "Show less" : "Read more"}
        </button>
      </div>
    </article>
  );
};
