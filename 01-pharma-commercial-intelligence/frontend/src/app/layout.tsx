import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Pharma Commercial Intelligence & Next-Best-Action Platform',
  description: 'Enterprise AI commercial co-pilot for HCP prioritization, prescription dynamics, and grounded briefing generation.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-background text-foreground min-h-screen antialiased">
        {children}
      </body>
    </html>
  );
}
