import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "CareerCards",
  description: "Five openings. Apply or skip.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
