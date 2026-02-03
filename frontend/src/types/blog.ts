export interface BlogPost {
  id: number;
  title: string;
  content: string;
  image?: string;
  timestamp: string;
  authorName: string;
  hasComments?: Array<unknown> | null;
}
