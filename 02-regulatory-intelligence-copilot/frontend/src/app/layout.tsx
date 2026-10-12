import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Regulatory Intelligence Copilot | FDA, EMA, ICH Multi-Agent Platform',
  description: 'Evidence-backed regulatory research, automated cross-version diff analysis, and pipeline submission impact tracking powered by Sarvam AI.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#070b14] text-slate-100 antialiased selection:bg-indigo-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
