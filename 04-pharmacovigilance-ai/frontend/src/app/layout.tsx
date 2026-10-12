import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Pharmacovigilance & Safety Signal Intelligence Platform',
  description: 'Enterprise drug safety signal detection, entity extraction, and clinical review platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#060913] text-slate-100 antialiased">
        {children}
      </body>
    </html>
  );
}
