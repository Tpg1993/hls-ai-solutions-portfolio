import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Clinical Trial Intelligence & Patient-Trial Matching Platform',
  description: 'Explainable patient screening, deterministic criteria verification, and predictive ML site risk forecasting powered by Sarvam AI.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-[#070b14] text-slate-100 antialiased selection:bg-emerald-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
