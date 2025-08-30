import type { Metadata } from 'next';
import './../styles/globals.css'; // Assuming globals.css is in src/styles

export const metadata: Metadata = {
  title: 'SARDIN-AI',
  description: 'Autonomous Maritime Intelligence Platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
